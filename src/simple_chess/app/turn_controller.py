"""Turn controller for chess game coordination (M4-02).

Coordinates turn identification and movement intent reception for the
application layer.

The turn controller receives the current game session and is responsible for:
- Identifying which side and player type is active on the current turn.
- Accepting a movement intent (UCI string) from the interface layer and
  storing it as pending state for later validation by M4-03.

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

    controller.current_side()          # "white"
    controller.current_player_type()   # PlayerType.HUMAN
    controller.receive_move_intent("e2e4")
    controller.pending_intent          # "e2e4"
    controller.clear_intent()
    controller.pending_intent          # None
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
    - Accept a movement intent (UCI string) from the interface layer and
      store it as pending state.
    - Expose the pending intent for use by M4-03 (validation and application).

    Non-responsibilities (explicit scope boundaries):
    - Does **not** validate moves — delegates to the domain (M4-03).
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

    def receive_move_intent(self, uci: str) -> None:
        """Accept and store a movement intent from the interface layer.

        Stores the UCI string as pending state so that M4-03 can later
        validate and apply it via the domain.  Does not validate the move.

        The intent is stored as-is; format validation (UCI syntax) is not
        performed here.  Validation of move legality belongs to M4-03.

        Args:
            uci: A movement string in UCI notation (e.g. ``"e2e4"``).
        """
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
