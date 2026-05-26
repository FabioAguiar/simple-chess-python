"""Input handler for the Pygame UI layer (M5-04).

Converts mouse pixel positions to algebraic chess square coordinates
and manages two-click selection state.

Responsibilities:
- Convert pixel coordinates to algebraic square notation (e.g. ``"e2"``).
- Maintain selection state: first click stores the origin square, second
  click forms the UCI string and signals a move intent.
- Enforce board bounds: clicks outside the 8x8 grid return ``None``.

Non-responsibilities:
- Does **not** validate move legality — that belongs to the domain
  (ADR-004).
- Does **not** access ``python-chess`` (``chess``) directly (ADR-004).
- Does **not** render or draw anything.
- Does **not** communicate directly with the Application except by
  returning a UCI string for the caller to forward.
"""
from __future__ import annotations

from simple_chess.ui.config import BOARD_SIZE, SQUARE_SIZE


def pixel_to_square(mouse_x: int, mouse_y: int) -> str | None:
    """Convert pixel coordinates to an algebraic square name.

    Uses ``SQUARE_SIZE`` and ``BOARD_SIZE`` from :mod:`simple_chess.ui.config`
    (``SQUARE_SIZE=80``, ``BOARD_SIZE=8``) to map pixel position to
    column and rank.

    Formula::

        col  = mouse_x // SQUARE_SIZE          # 0 (a) … 7 (h)
        rank = BOARD_SIZE - (mouse_y // SQUARE_SIZE)  # 8 (rank 8) … 1 (rank 1)
        square = chr(ord('a') + col) + str(rank)

    Args:
        mouse_x: Horizontal pixel position of the click.
        mouse_y: Vertical pixel position of the click.

    Returns:
        Algebraic square name such as ``"e2"`` when the click is within the
        8×8 board grid, or ``None`` if outside bounds.

    Examples::

        pixel_to_square(0, 0)     # "a8"  (top-left corner)
        pixel_to_square(639, 639) # "h1"  (bottom-right corner)
        pixel_to_square(640, 0)   # None  (outside grid)
        pixel_to_square(-1, 0)    # None  (outside grid)
    """
    col = mouse_x // SQUARE_SIZE
    rank = BOARD_SIZE - (mouse_y // SQUARE_SIZE)
    if 0 <= col <= 7 and 1 <= rank <= 8:  # noqa: PLR2004
        return chr(ord("a") + col) + str(rank)
    return None


class InputHandler:
    """Manages two-click selection state for move intent formation (M5-04).

    Implements the two-click model described in M5-04:

    - **First valid click**: stores the origin square as ``selected_square``.
    - **Second valid click**: forms the UCI string
      ``<origin><destination>`` (e.g. ``"e2e4"``), clears ``selected_square``,
      and returns the intent for the caller to forward to the Application.
    - **Click outside the board**: resets selection silently and returns
      ``None``.

    The selection state is internal to the UI.  The caller (``window.py``)
    is responsible for forwarding the returned UCI string to
    :meth:`~simple_chess.app.turn_controller.TurnController.receive_move_intent`.

    Attributes:
        selected_square: The currently selected origin square (e.g. ``"e2"``),
            or ``None`` when no square is selected.

    Example::

        handler = InputHandler()
        handler.handle_click(80, 560)   # first click  → None, selects "b2"
        handler.handle_click(80, 400)   # second click → "b2b4"
    """

    def __init__(self) -> None:
        self.selected_square: str | None = None

    def handle_click(self, mouse_x: int, mouse_y: int) -> str | None:
        """Process a mouse click and return a UCI move intent when ready.

        Args:
            mouse_x: Horizontal pixel position of the click.
            mouse_y: Vertical pixel position of the click.

        Returns:
            A UCI move string (e.g. ``"e2e4"``) when both origin and
            destination squares have been clicked in sequence, or ``None``
            otherwise.
        """
        square = pixel_to_square(mouse_x, mouse_y)

        if square is None:
            # Click outside the board — reset selection silently.
            self.selected_square = None
            return None

        if self.selected_square is None:
            # First valid click: record origin square.
            self.selected_square = square
            return None

        # Second valid click: form UCI intent and clear selection.
        uci = self.selected_square + square
        self.selected_square = None
        return uci

    def reset(self) -> None:
        """Clear the current selection state.

        Use to reset intent formation without waiting for the next click
        cycle (e.g. on game reset or turn change).
        """
        self.selected_square = None
