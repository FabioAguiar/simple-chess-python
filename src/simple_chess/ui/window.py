"""Pygame window and main event loop for simple-chess-python."""

import sys

import pygame

from simple_chess.app.session import GameMode, GameSession
from simple_chess.app.turn_controller import TurnController
from simple_chess.domain.match import MatchState
from simple_chess.ui.board_renderer import draw_board
from simple_chess.ui.config import FPS, WINDOW_HEIGHT, WINDOW_TITLE, WINDOW_WIDTH
from simple_chess.ui.input_handler import InputHandler


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

        draw_board(screen)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit(0)
