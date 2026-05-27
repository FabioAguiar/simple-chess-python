"""AI layer for computer move selection.

The AI package owns move-selection strategies only. It consumes plain legal
move strings provided by the application/domain boundary and returns a
candidate move for the application to apply through the domain.
"""

from simple_chess.ai.random_strategy import RandomMoveSelector, choose_random_move

__all__ = ["RandomMoveSelector", "choose_random_move"]
