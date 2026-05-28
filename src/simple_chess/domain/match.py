"""Central match state for the chess game domain (M3-01).

This module defines :class:`MatchState`, the single source of truth for a
chess match at runtime.  The ``chess`` library (python-chess) is imported
exclusively here so that external layers — application, AI, and interface —
never depend on chess library types directly.
"""
from __future__ import annotations

import chess


class MatchState:
    """Represents the central, testable state of a chess match.

    Responsibilities (per ``docs/architecture.md``):
    - Represent the board and piece positions.
    - Report the current turn.
    - Validate legal moves and reject illegal ones.
    - Apply valid moves.
    - Report game-over states (check, checkmate, stalemate, draws).
    - Encapsulate ``python-chess``; no chess library type is exposed publicly.

    Usage example::

        match = MatchState()          # standard starting position
        match.current_turn()          # "white"
        match.legal_move_ucis()       # ["a2a3", "a2a4", ..., "h2h4"]
        match.push_uci("e2e4")
        match.current_turn()          # "black"
    """

    def __init__(self) -> None:
        """Initialise a new match from the standard chess starting position."""
        self._board: chess.Board = chess.Board()

    # ------------------------------------------------------------------
    # Turn
    # ------------------------------------------------------------------

    def current_turn(self) -> str:
        """Return whose turn it is to move.

        Returns:
            ``"white"`` when it is White's turn, ``"black"`` when it is
            Black's turn.
        """
        return "white" if self._board.turn == chess.WHITE else "black"

    # ------------------------------------------------------------------
    # Basic state exposure
    # ------------------------------------------------------------------

    def is_game_over(self) -> bool:
        """Return whether the game has ended by any standard termination.

        Returns:
            ``True`` if the game is over (checkmate, stalemate, or any draw
            condition), ``False`` otherwise.
        """
        return self._board.is_game_over()

    def is_check(self) -> bool:
        """Return whether the side to move is currently in check.

        Returns:
            ``True`` if the side to move is in check, ``False`` otherwise.
        """
        return self._board.is_check()

    def outcome(self) -> str | None:
        """Return the game outcome, or ``None`` if the game is still ongoing.

        Returns:
            A lowercase string naming the termination reason when the game is
            over — one of ``"checkmate"``, ``"stalemate"``,
            ``"insufficient_material"``, ``"seventyfive_moves"``,
            ``"fivefold_repetition"``, ``"fifty_moves"``,
            ``"threefold_repetition"`` — or ``None`` if the game has not ended.
        """
        if not self._board.is_game_over():
            return None
        result = self._board.outcome()
        if result is None:
            return None
        return result.termination.name.lower()

    def legal_move_ucis(self) -> list[str]:
        """Return all legal moves for the current position in UCI notation.

        Returns:
            A list of UCI strings such as ``["e2e4", "d2d4", ...]``.
            Returns an empty list when the game is over.
        """
        return [move.uci() for move in self._board.legal_moves]

    def is_legal_move(self, uci: str) -> bool:
        """Return whether a move is legal in the current position.

        This is a check-only operation: the board state is **not** modified
        regardless of the result.  Use :meth:`push_uci` to apply a move
        after confirming it is legal.

        Args:
            uci: A candidate move in UCI notation, e.g. ``"e2e4"`` or
                 ``"e7e8q"`` (promotion).

        Returns:
            ``True`` if the move is syntactically valid UCI and legal in the
            current position.  ``False`` for any invalid or illegal move,
            including malformed UCI strings.
        """
        try:
            move = chess.Move.from_uci(uci)
        except (chess.InvalidMoveError, ValueError):
            return False
        return move in self._board.legal_moves

    def board_map(self) -> dict[str, str]:
        """Return the current piece positions as a plain Python mapping.

        Maps each occupied square to its piece symbol using standard
        algebraic notation.  No ``python-chess`` types are exposed in
        the return value, in compliance with ADR-004.

        Returns:
            A ``dict[str, str]`` where each key is a square name
            (``"a1"`` through ``"h8"``) and each value is the
            one-character piece symbol for the occupying piece:
            upper-case for White (``K``, ``Q``, ``R``, ``B``, ``N``,
            ``P``), lower-case for Black (``k``, ``q``, ``r``, ``b``,
            ``n``, ``p``).  Squares with no piece are omitted.
        """
        result: dict[str, str] = {}
        for square in chess.SQUARES:
            piece = self._board.piece_at(square)
            if piece is not None:
                result[chess.square_name(square)] = piece.symbol()
        return result

    def last_move_uci(self) -> str | None:
        """Return the UCI string of the last applied move, or ``None``.

        Returns:
            The UCI string of the most recently applied move (e.g.
            ``"e7e5"``), or ``None`` if no move has been applied yet.
        """
        if self._board.move_stack:
            return self._board.peek().uci()
        return None

    # ------------------------------------------------------------------
    # Mutation
    # ------------------------------------------------------------------

    def push_uci(self, uci: str) -> None:
        """Apply a move given in UCI notation, updating the match state.

        Args:
            uci: A move in UCI notation, e.g. ``"e2e4"`` or ``"e7e8q"``
                 (promotion).

        Raises:
            ValueError: If *uci* is syntactically invalid or the resulting
                move is not legal in the current position.
        """
        try:
            move = chess.Move.from_uci(uci)
        except (chess.InvalidMoveError, ValueError) as exc:
            raise ValueError(f"Invalid UCI string: {uci!r}") from exc

        if move not in self._board.legal_moves:
            raise ValueError(f"Illegal move in current position: {uci!r}")

        self._board.push(move)
