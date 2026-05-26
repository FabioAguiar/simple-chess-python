"""Turn controller for chess game coordination (M4-02, M6-02).

Coordinates turn identification and movement intent reception for the
application layer.

The turn controller receives the current game session and is responsible for:
- Identifying which side and player type is active on the current turn.
- Accepting a movement intent (UCI string) from the interface layer and
  storing it as pending state for later validation by M4-03.
- Explicitly checking that a move intent is compatible with the current turn
  before storing it (M6-02).

It does not validate or apply moves — those responsibilities belong to M4-03.
It does not call the AI — that belongs to M4-04.
It does not depend on Pygame — that belongs to M5.
It does not import python-chess (``chess``) directly (ADR-004).

Example usage::

    from simple_chess.domain.match import MatchState
    from simple_chess.app.session import GameMode, GameSession
    from simple_chess.app.turn_controller import TurnController

    match = MatchState()
    session = GameSession(mode=GameMode.PVP, match=match)
    controller = TurnController(session=session)

    controller.current_side()                  # "white"
    controller.current_player_type()           # PlayerType.HUMAN
    controller.is_turn_compatible("e2e4")      # True  (white pawn, white's turn)
    controller.is_turn_compatible("e7e5")      # False (black pawn, white's turn)
    controller.receive_move_intent("e2e4")
    controller.pending_intent                  # "e2e4"
    controller.clear_intent()
    controller.pending_intent                  # None
"""
from __future__ import annotations

from simple_chess.app.session import GameSession, PlayerType


class TurnController:
    """Coordinates turn identification and movement intent reception.

    Wraps a :class:`~simple_chess.app.session.GameSession` to expose turn
    information and accept movement intents from the interface layer.

    Responsibilities:
    - Report which side (white or black) holds the current turn.
    - Report which player type (human or computer) is active.
    - Explicitly check whether a move intent is compatible with the current
      turn before accepting it (M6-02).
    - Accept a movement intent (UCI string) from the interface layer and
      store it as pending state when turn-compatible.
    - Expose the pending intent for use by M4-03 (validation and application).

    Non-responsibilities (explicit scope boundaries):
    - Does **not** validate full move legality — delegates to the domain
      (M4-03) via :class:`~simple_chess.app.move_processor.MoveProcessor`.
    - Does **not** apply moves — delegates to the domain (M4-03).
    - Does **not** call the AI — that is M4-04.
    - Does **not** depend on Pygame.
    - Does **not** import ``python-chess`` (``chess``) directly (ADR-004).
    - Does **not** maintain its own turn counter or flag — delegates to the
      domain via :meth:`~simple_chess.app.session.GameSession.match`.

    Args:
        session: The active :class:`~simple_chess.app.session.GameSession`,
            injected to allow replacement in tests without real session state.
    """

    def __init__(self, session: GameSession) -> None:
        self._session = session
        self._pending_intent: str | None = None

    # ------------------------------------------------------------------
    # Turn identification
    # ------------------------------------------------------------------

    def current_side(self) -> str:
        """Return the side (``"white"`` or ``"black"``) currently to move.

        Delegates to the domain via the session's
        :class:`~simple_chess.domain.match.MatchState`.

        Returns:
            ``"white"`` or ``"black"``.
        """
        return self._session.match.current_turn()

    def current_player_type(self) -> PlayerType:
        """Return the :class:`~simple_chess.app.session.PlayerType` active now.

        Delegates to
        :meth:`~simple_chess.app.session.GameSession.current_player_type`.

        Returns:
            :attr:`~simple_chess.app.session.PlayerType.HUMAN` or
            :attr:`~simple_chess.app.session.PlayerType.COMPUTER`.
        """
        return self._session.current_player_type()

    # ------------------------------------------------------------------
    # Movement intent reception
    # ------------------------------------------------------------------

    def is_turn_compatible(self, uci: str) -> bool:
        """Return whether a move intent is compatible with the current turn.

        Checks whether the piece at the source square named in *uci* belongs
        to the side currently to move, using only the domain's public
        interface (:meth:`~simple_chess.domain.match.MatchState.board_map`
        and :meth:`~simple_chess.domain.match.MatchState.current_turn`).
        No chess-rule logic is reimplemented here (ADR-004).

        This is the Application layer's explicit turn-compatibility gate
        (M6-02).  A move that originates from a piece of the wrong colour,
        from an empty square, or from a syntactically invalid source square
        is considered turn-incompatible and will not be stored by
        :meth:`receive_move_intent`.

        Args:
            uci: A candidate move string in UCI notation.  Only the first
                two characters (source square) are inspected.

        Returns:
            ``True`` if the piece at the source square belongs to the side
            currently to move according to the domain.
            ``False`` if the UCI string is shorter than two characters, no
            piece occupies the source square, or the piece belongs to the
            opposing side.
        """
        if len(uci) < 2:  # noqa: PLR2004
            return False
        source_square = uci[:2]
        board = self._session.match.board_map()
        piece = board.get(source_square)
        if piece is None:
            return False
        current = self._session.match.current_turn()
        # Uppercase symbols are White pieces; lowercase are Black (ADR-004,
        # board_map contract).  White pieces are valid only on white's turn
        # and vice-versa.
        return (current == "white") == piece.isupper()

    def receive_move_intent(self, uci: str) -> None:
        """Accept and store a movement intent if compatible with the current turn.

        Explicitly checks turn compatibility via :meth:`is_turn_compatible`
        before storing the intent.  Intents from the wrong side are silently
        rejected — the pending intent is not modified when the source piece
        does not belong to the current player (M6-02).

        Full move-legality validation (path, pins, check constraints) is
        still delegated to the domain via
        :class:`~simple_chess.app.move_processor.MoveProcessor` (M4-03).

        Args:
            uci: A movement string in UCI notation (e.g. ``"e2e4"``).
        """
        if self.is_turn_compatible(uci):
            self._pending_intent = uci

    @property
    def pending_intent(self) -> str | None:
        """The movement intent currently waiting to be validated.

        Returns:
            The stored UCI string, or ``None`` if no intent is pending.
        """
        return self._pending_intent

    def clear_intent(self) -> None:
        """Clear the pending movement intent.

        Called by M4-03 after the intent has been validated and applied
        (or rejected).  Resets the pending state to ``None``.
        """
        self._pending_intent = None
