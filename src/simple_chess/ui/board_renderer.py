"""Board renderer for the simple-chess-python UI."""

import pygame

from simple_chess.ui.config import (
    BOARD_SIZE,
    DARK_SQUARE_COLOR,
    LIGHT_SQUARE_COLOR,
    SQUARE_SIZE,
)


def draw_board(screen: pygame.Surface) -> None:
    """Render the 8x8 chess board onto *screen*.

    Squares alternate between LIGHT_SQUARE_COLOR and DARK_SQUARE_COLOR
    following the standard chess convention: top-left corner (col=0, row=0)
    is a light square, matching the a8 position in chess notation.

    This function is synchronous and proportional (64 rectangles), with no
    I/O or heavy operations, and does not block the event loop.

    Args:
        screen: Pygame surface to draw on.  Must be at least
            BOARD_SIZE * SQUARE_SIZE pixels in both dimensions.
    """
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            color = LIGHT_SQUARE_COLOR if (row + col) % 2 == 0 else DARK_SQUARE_COLOR
            rect = pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(screen, color, rect)
