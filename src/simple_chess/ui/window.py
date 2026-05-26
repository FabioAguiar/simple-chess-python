"""Pygame window and main event loop for simple-chess-python."""

import sys

import pygame

from simple_chess.app.move_processor import MoveProcessor
from simple_chess.app.session import GameMode, GameSession
from simple_chess.app.turn_controller import TurnController
from simple_chess.domain.match import MatchState
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
    lines = [_format_turn(state.get("turn"))]
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


def run() -> None:
    """Initialize Pygame, open the game window, and run the main event loop.

    The window is proportional to the 8x8 board (640x640 by default).
    The loop processes events and exits cleanly when the window is closed
    or a QUIT event is received.

    Mouse click events (MOUSEBUTTONDOWN) are captured, converted to
    algebraic square coordinates via :class:`~simple_chess.ui.input_handler.InputHandler`,
    and forwarded as UCI move intents to
    :meth:`~simple_chess.app.turn_controller.TurnController.receive_move_intent`
    when a two-click sequence is complete.

    The UI does **not** validate move legality; that responsibility belongs
    to the domain via the Application layer (ADR-004).
    """
    pygame.init()

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)
    clock = pygame.time.Clock()

    # --- Application layer setup (M5-04) ---
    match = MatchState()
    session = GameSession(mode=GameMode.PVP, match=match)
    turn_controller = TurnController(session=session)
    input_handler = InputHandler()

    # --- UI/Application integration (M5-05) ---
    move_processor = MoveProcessor(match=match, controller=turn_controller)
    font = make_piece_font()
    hud_font = pygame.font.Font(None, 24)
    invalid_move_timer = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Left-button click only (button 1).
                if event.button == 1:
                    mouse_x, mouse_y = event.pos
                    uci = input_handler.handle_click(mouse_x, mouse_y)
                    if uci is not None:
                        turn_controller.receive_move_intent(uci)
                        move_applied = move_processor.process_pending_intent()
                        invalid_move_timer = (
                            0 if move_applied else INVALID_MOVE_MESSAGE_FRAMES
                        )

        state = session.game_state_snapshot()
        draw_board(screen, input_handler.selected_square)
        draw_pieces(screen, state["board"], font)
        _draw_hud(screen, hud_font, state, invalid_move_timer)
        pygame.display.flip()

        if invalid_move_timer > 0:
            invalid_move_timer -= 1

        clock.tick(FPS)

    pygame.quit()
    sys.exit(0)
