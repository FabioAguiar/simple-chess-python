"""Board renderer for the simple-chess-python UI."""

import pygame

from simple_chess.ui.config import (
    BOARD_SIZE,
    DARK_SQUARE_COLOR,
    LIGHT_SQUARE_COLOR,
    SQUARE_SIZE,
)

SELECTED_SQUARE_FILL_COLOR: tuple[int, int, int, int] = (255, 235, 59, 90)
SELECTED_SQUARE_BORDER_COLOR: tuple[int, int, int] = (255, 230, 0)
SELECTED_SQUARE_BORDER_WIDTH: int = 4


def _square_rect(square: str) -> pygame.Rect | None:
    """Return the board rectangle for an algebraic square name."""
    if len(square) != 2:
        return None

    file_name, rank_name = square[0], square[1]
    if (
        file_name < "a"
        or file_name > "h"
        or rank_name < "1"
        or rank_name > "8"
    ):
        return None

    col = ord(file_name) - ord("a")
    row = BOARD_SIZE - int(rank_name)
    return pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)


def draw_board(screen: pygame.Surface, selected_square: str | None = None) -> None:
    """Render the 8x8 chess board onto *screen*.

    Squares alternate between LIGHT_SQUARE_COLOR and DARK_SQUARE_COLOR
    following the standard chess convention: top-left corner (col=0, row=0)
    is a light square, matching the a8 position in chess notation.

    This function is synchronous and proportional (64 rectangles), with no
    I/O or heavy operations, and does not block the event loop.

    Args:
        screen: Pygame surface to draw on.  Must be at least
            BOARD_SIZE * SQUARE_SIZE pixels in both dimensions.
        selected_square: Optional algebraic square name to highlight as the
            active UI selection.  This is UI state, not game-rule state.
    """
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            color = LIGHT_SQUARE_COLOR if (row + col) % 2 == 0 else DARK_SQUARE_COLOR
            rect = pygame.Rect(
                col * SQUARE_SIZE,
                row * SQUARE_SIZE,
                SQUARE_SIZE,
                SQUARE_SIZE,
            )
            pygame.draw.rect(screen, color, rect)

    if selected_square is None:
        return

    selected_rect = _square_rect(selected_square)
    if selected_rect is None:
        return

    overlay = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
    overlay.fill(SELECTED_SQUARE_FILL_COLOR)
    screen.blit(overlay, selected_rect)
    pygame.draw.rect(
        screen,
        SELECTED_SQUARE_BORDER_COLOR,
        selected_rect,
        SELECTED_SQUARE_BORDER_WIDTH,
    )
