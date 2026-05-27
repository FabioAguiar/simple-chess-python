"""Random move-selection strategy for the AI layer.

This module deliberately depends only on Python standard-library types. The
application supplies legal moves as plain UCI strings, and the AI returns one
candidate UCI string without applying it to the match state.
"""
from __future__ import annotations

from collections.abc import Sequence
import random


class RandomMoveSelector:
    """Select a random legal move candidate without mutating game state.

    Args:
        rng: Optional random-number generator compatible with
            :class:`random.Random`. Supplying one makes the selector
            deterministic in tests while keeping the runtime strategy random.
    """

    def __init__(self, rng: random.Random | None = None) -> None:
        self._rng = rng if rng is not None else random.Random()

    def select_move(self, legal_moves: Sequence[str]) -> str:
        """Return one random candidate from the available legal moves.

        Args:
            legal_moves: Legal moves in UCI notation supplied by the
                application/domain boundary.

        Returns:
            One UCI move string from *legal_moves*.

        Raises:
            ValueError: If no legal moves are available.
        """
        if not legal_moves:
            raise ValueError("Cannot choose an AI move without legal moves.")

        return self._rng.choice(list(legal_moves))


def choose_random_move(
    legal_moves: Sequence[str],
    rng: random.Random | None = None,
) -> str:
    """Return a random legal move candidate using the default selector."""
    return RandomMoveSelector(rng=rng).select_move(legal_moves)
