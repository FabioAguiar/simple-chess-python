"""Pygame window and main event loop for simple-chess-python."""

import sys

import pygame

from simple_chess.app import GameMode, LocalGame
from simple_chess.ui.board_renderer import draw_board
from simple_chess.ui.config import FPS, WINDOW_HEIGHT, WINDOW_TITLE, WINDOW_WIDTH
from simple_chess.ui.input_handler import InputHandler
from simple_chess.ui.piece_renderer import draw_pieces, make_piece_font

INVALID_MOVE_MESSAGE_FRAMES: int = FPS * 3
HUD_TEXT_COLOR: tuple[int, int, int] = (255, 255, 255)
HUD_SHADOW_COLOR: tuple[int, int, int] = (0, 0, 0)
HUD_PANEL_COLOR: tuple[int, int, int, int] = (0, 0, 0, 145)
HUD_MARGIN: int = 10
HUD_PADDING: int = 8
HUD_LINE_GAP: int = 4
MODE_SELECTION_BG_COLOR: tuple[int, int, int] = (34, 38, 43)
MODE_BUTTON_COLOR: tuple[int, int, int] = (72, 84, 96)
MODE_BUTTON_BORDER_COLOR: tuple[int, int, int] = (210, 216, 222)
MODE_BUTTON_WIDTH: int = 240
MODE_BUTTON_HEIGHT: int = 54
MODE_BUTTON_GAP: int = 18


def _mode_button_rects() -> dict[GameMode, pygame.Rect]:
    left = (WINDOW_WIDTH - MODE_BUTTON_WIDTH) // 2
    top = (WINDOW_HEIGHT - (MODE_BUTTON_HEIGHT * 2 + MODE_BUTTON_GAP)) // 2
    return {
        GameMode.PVP: pygame.Rect(left, top, MODE_BUTTON_WIDTH, MODE_BUTTON_HEIGHT),
        GameMode.PVC: pygame.Rect(
            left,
            top + MODE_BUTTON_HEIGHT + MODE_BUTTON_GAP,
            MODE_BUTTON_WIDTH,
            MODE_BUTTON_HEIGHT,
        ),
    }


def _mode_from_key(key: int) -> GameMode | None:
    if key in (pygame.K_1, pygame.K_p):
        return GameMode.PVP
    if key in (pygame.K_2, pygame.K_c):
        return GameMode.PVC
    return None


def _mode_from_click(position: tuple[int, int]) -> GameMode | None:
    for mode, rect in _mode_button_rects().items():
        if rect.collidepoint(position):
            return mode
    return None


def _start_local_game(
    mode: GameMode,
) -> tuple[LocalGame, InputHandler, dict[str, object]]:
    local_game = LocalGame.new(mode)
    input_handler = InputHandler()
    return local_game, input_handler, local_game.game_state_snapshot()


def _format_turn(turn: object) -> str:
    if turn == "white":
        return "Turn: White"
    if turn == "black":
        return "Turn: Black"
    return f"Turn: {turn}"


def _format_outcome(outcome: object) -> str:
    labels = {
        "checkmate": "Checkmate",
        "stalemate": "Draw: stalemate",
        "insufficient_material": "Draw: insufficient material",
        "seventyfive_moves": "Draw: seventy-five moves",
        "fivefold_repetition": "Draw: fivefold repetition",
        "fifty_moves": "Draw: fifty moves",
        "threefold_repetition": "Draw: threefold repetition",
    }
    if isinstance(outcome, str):
        return labels.get(outcome, f"Game over: {outcome.replace('_', ' ')}")
    return "Game over"


def _format_mode(mode: object) -> str:
    if mode == "pvp":
        return "Mode: PvP"
    if mode == "pvc":
        return "Mode: PvC"
    return f"Mode: {mode}"


def _status_message(state: dict[str, object], invalid_move_timer: int) -> str | None:
    if state.get("is_game_over"):
        return _format_outcome(state.get("outcome"))
    if invalid_move_timer > 0:
        return "Invalid move"
    if state.get("is_check"):
        return "Check"
    return None


def _render_text_with_shadow(
    screen: pygame.Surface,
    font: pygame.font.Font,
    text: str,
    position: tuple[int, int],
) -> pygame.Rect:
    shadow_surface = font.render(text, True, HUD_SHADOW_COLOR)
    text_surface = font.render(text, True, HUD_TEXT_COLOR)
    shadow_rect = shadow_surface.get_rect(topleft=(position[0] + 1, position[1] + 1))
    text_rect = text_surface.get_rect(topleft=position)
    screen.blit(shadow_surface, shadow_rect)
    screen.blit(text_surface, text_rect)
    return text_rect


def _draw_hud(
    screen: pygame.Surface,
    font: pygame.font.Font,
    state: dict[str, object],
    invalid_move_timer: int,
) -> None:
    lines = [_format_mode(state.get("mode")), _format_turn(state.get("turn"))]
    status_message = _status_message(state, invalid_move_timer)
    if status_message is not None:
        lines.append(status_message)

    rendered_lines = [font.render(line, True, HUD_TEXT_COLOR) for line in lines]
    panel_width = max(surface.get_width() for surface in rendered_lines) + HUD_PADDING * 2
    panel_height = (
        sum(surface.get_height() for surface in rendered_lines)
        + HUD_LINE_GAP * (len(rendered_lines) - 1)
        + HUD_PADDING * 2
    )

    panel = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
    panel.fill(HUD_PANEL_COLOR)
    screen.blit(panel, (HUD_MARGIN, HUD_MARGIN))

    y = HUD_MARGIN + HUD_PADDING
    for line in lines:
        rect = _render_text_with_shadow(
            screen,
            font,
            line,
            (HUD_MARGIN + HUD_PADDING, y),
        )
        y += rect.height + HUD_LINE_GAP


def _draw_mode_selection(screen: pygame.Surface, font: pygame.font.Font) -> None:
    screen.fill(MODE_SELECTION_BG_COLOR)
    title = font.render("Select game mode", True, HUD_TEXT_COLOR)
    title_rect = title.get_rect(
        center=(
            WINDOW_WIDTH // 2,
            _mode_button_rects()[GameMode.PVP].top - MODE_BUTTON_GAP * 2,
        )
    )
    screen.blit(title, title_rect)

    labels = {
        GameMode.PVP: "PvP local",
        GameMode.PVC: "PvC local",
    }
    shortcuts = {
        GameMode.PVP: "1 / P",
        GameMode.PVC: "2 / C",
    }
    for mode, rect in _mode_button_rects().items():
        pygame.draw.rect(screen, MODE_BUTTON_COLOR, rect)
        pygame.draw.rect(screen, MODE_BUTTON_BORDER_COLOR, rect, width=2)

        label = font.render(labels[mode], True, HUD_TEXT_COLOR)
        label_rect = label.get_rect(center=(rect.centerx, rect.centery - 8))
        screen.blit(label, label_rect)

        shortcut = font.render(shortcuts[mode], True, HUD_TEXT_COLOR)
        shortcut_rect = shortcut.get_rect(center=(rect.centerx, rect.centery + 14))
        screen.blit(shortcut, shortcut_rect)


def run() -> None:
    """Initialize Pygame, open the game window, and run the main event loop.

    The window is proportional to the 8x8 board (640x640 by default).
    The loop processes events and exits cleanly when the window is closed
    or a QUIT event is received.

    Mouse click events (MOUSEBUTTONDOWN) are captured, converted to
    algebraic square coordinates via :class:`~simple_chess.ui.input_handler.InputHandler`,
    and forwarded as UCI move intents to the Application layer when a
    two-click sequence is complete.

    The UI does **not** validate move legality; that responsibility belongs
    to the domain via the Application layer (ADR-004).
    """
    pygame.init()

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)
    clock = pygame.time.Clock()

    # --- Application layer setup ---
    local_game: LocalGame | None = None
    input_handler: InputHandler | None = None

    font = make_piece_font()
    hud_font = pygame.font.Font(None, 24)
    invalid_move_timer = 0
    state: dict[str, object] | None = None

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN and local_game is None:
                selected_mode = _mode_from_key(event.key)
                if selected_mode is not None:
                    local_game, input_handler, state = _start_local_game(selected_mode)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and local_game is None:
                    selected_mode = _mode_from_click(event.pos)
                    if selected_mode is not None:
                        local_game, input_handler, state = _start_local_game(
                            selected_mode
                        )
                        invalid_move_timer = 0

                # Left-button click only (button 1) after mode selection.
                elif (
                    event.button == 1
                    and input_handler is not None
                    and state is not None
                ):
                    mouse_x, mouse_y = event.pos
                    uci = input_handler.handle_click(mouse_x, mouse_y)
                    if uci is not None:
                        if local_game is None:
                            continue
                        move_applied, state = (
                            local_game.submit_human_move_intent_with_snapshot(uci)
                        )
                        invalid_move_timer = (
                            0 if move_applied else INVALID_MOVE_MESSAGE_FRAMES
                        )

        if local_game is None or input_handler is None or state is None:
            _draw_mode_selection(screen, hud_font)
        else:
            draw_board(screen, input_handler.selected_square)
            draw_pieces(screen, state["board"], font)
            _draw_hud(screen, hud_font, state, invalid_move_timer)
        pygame.display.flip()

        if invalid_move_timer > 0:
            invalid_move_timer -= 1

        clock.tick(FPS)

    pygame.quit()
    sys.exit(0)
