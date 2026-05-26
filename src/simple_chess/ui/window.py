"""Pygame window and main event loop for simple-chess-python."""

import sys

import pygame

from simple_chess.ui.board_renderer import draw_board
from simple_chess.ui.config import FPS, WINDOW_HEIGHT, WINDOW_TITLE, WINDOW_WIDTH


def run() -> None:
    """Initialize Pygame, open the game window, and run the main event loop.

    The window is proportional to the 8x8 board (640x640 by default).
    The loop processes events and exits cleanly when the window is closed
    or a QUIT event is received.
    """
    pygame.init()

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw_board(screen)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit(0)
