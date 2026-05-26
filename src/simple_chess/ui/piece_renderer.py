"""Piece renderer for the simple-chess-python UI (M5-03).

Renders chess piece symbols over the 8×8 board grid using the ``board``
mapping provided by the Application layer
(``GameSession.game_state_snapshot()["board"]``).

Piece state is consumed exclusively from the Application-layer snapshot;
this module never imports from ``simple_chess.domain`` or ``chess``
directly, in compliance with ADR-004.

Usage example (called from the main window loop after draw_board)::

    from simple_chess.app import LocalGame
    from simple_chess.ui.piece_renderer import draw_pieces, make_piece_font

    local_game = LocalGame.new_pvp()
    font = make_piece_font(size=56)

    # Inside the Pygame event loop:
    state = local_game.game_state_snapshot()
    draw_pieces(screen, state["board"], font)
"""
from __future__ import annotations

import pygame

from simple_chess.ui.config import SQUARE_SIZE

# ---------------------------------------------------------------------------
# Piece symbol mapping
# ---------------------------------------------------------------------------

#: Unicode chess piece symbols keyed by one-character piece identifier.
#: Upper-case = White pieces, lower-case = Black pieces.
PIECE_UNICODE: dict[str, str] = {
    "K": "♔",  # ♔ White King
    "Q": "♕",  # ♕ White Queen
    "R": "♖",  # ♖ White Rook
    "B": "♗",  # ♗ White Bishop
    "N": "♘",  # ♘ White Knight
    "P": "♙",  # ♙ White Pawn
    "k": "♚",  # ♚ Black King
    "q": "♛",  # ♛ Black Queen
    "r": "♜",  # ♜ Black Rook
    "b": "♝",  # ♝ Black Bishop
    "n": "♞",  # ♞ Black Knight
    "p": "♟",  # ♟ Black Pawn
}

# ---------------------------------------------------------------------------
# Piece colours
# ---------------------------------------------------------------------------

#: Fill colour for White pieces (rendered on the board surface).
WHITE_PIECE_COLOR: tuple[int, int, int] = (255, 255, 255)

#: Fill colour for Black pieces (rendered on the board surface).
BLACK_PIECE_COLOR: tuple[int, int, int] = (20, 20, 20)

#: Outline colour applied around every piece symbol for contrast.
PIECE_OUTLINE_COLOR: tuple[int, int, int] = (0, 0, 0)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def make_piece_font(size: int = 56) -> pygame.font.Font:
    """Return a system font suitable for rendering Unicode piece symbols.

    Tries to locate a font that includes Unicode chess codepoints.  Falls
    back to the Pygame default font when no suitable system font is found.

    Args:
        size: Font size in points.  Defaults to ``56``, which fits
            comfortably in a 80 × 80 pixel square with margin.

    Returns:
        A :class:`pygame.font.Font` instance ready for use with
        :func:`draw_pieces`.
    """
    candidates = [
        "dejavusans",
        "freesans",
        "unifont",
        "notosans",
        "segoeuisymbol",
        "symbola",
    ]
    for name in candidates:
        font = pygame.font.SysFont(name, size)
        if font is not None:
            return font
    return pygame.font.Font(None, size)


def draw_pieces(
    screen: pygame.Surface,
    board_map: dict[str, str],
    font: pygame.font.Font,
) -> None:
    """Render chess pieces onto *screen* from an Application-layer board map.

    Iterates over every entry in *board_map* and renders the corresponding
    Unicode piece symbol centred inside its square.  An outline pass is
    rendered first (shifted by one pixel in each cardinal direction) to
    provide contrast against any board colour.

    Coordinate mapping (matches :mod:`simple_chess.ui.board_renderer`)::

        col = ord(square[0]) - ord('a')   # 0 = 'a' … 7 = 'h'
        row = 8 - int(square[1])          # 0 = rank 8 … 7 = rank 1

    Args:
        screen: Pygame surface to draw on.  Must match the board dimensions
            (at least ``BOARD_SIZE × SQUARE_SIZE`` in both axes).
        board_map: Mapping from square names (``"a1"``–``"h8"``) to
            one-character piece symbols (``"K"``, ``"k"``, etc.) as
            returned by ``GameSession.game_state_snapshot()["board"]``.
            Squares with no piece should be absent from the mapping.
        font: Pygame font for rendering piece symbols.  Use
            :func:`make_piece_font` to obtain a suitable font, or supply
            any :class:`pygame.font.Font` that covers the Unicode chess
            block (U+2654–U+265F).
    """
    for square, piece_id in board_map.items():
        symbol = PIECE_UNICODE.get(piece_id, piece_id)
        col = ord(square[0]) - ord("a")
        row = 8 - int(square[1])
        center_x = col * SQUARE_SIZE + SQUARE_SIZE // 2
        center_y = row * SQUARE_SIZE + SQUARE_SIZE // 2

        # Determine piece colour: upper-case = White, lower-case = Black.
        fill_color = WHITE_PIECE_COLOR if piece_id.isupper() else BLACK_PIECE_COLOR

        # Outline pass — render in outline colour at four offsets.
        outline_surface = font.render(symbol, True, PIECE_OUTLINE_COLOR)
        outline_rect = outline_surface.get_rect(center=(center_x, center_y))
        for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            screen.blit(outline_surface, outline_rect.move(dx, dy))

        # Fill pass — render in piece colour at the exact centre.
        fill_surface = font.render(symbol, True, fill_color)
        fill_rect = fill_surface.get_rect(center=(center_x, center_y))
        screen.blit(fill_surface, fill_rect)
