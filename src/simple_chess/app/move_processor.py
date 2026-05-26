"""Move processor for chess game coordination (M4-03, M6-02).

Processes pending movement intents from the :class:`TurnController` by
delegating validation and application to the domain (:class:`MatchState`).

The move processor consumes the pending intent stored by
:class:`TurnController`, validates it via the domain's public interface,
applies it if legal, and clears the intent regardless of the outcome.

M6-02 adds an explicit Application-layer turn-compatibility gate before
domain validation: intents incompatible with the current turn are rejected
early via :meth:`~simple_chess.app.turn_controller.TurnController.is_turn_compatible`,
keeping the source of truth in the Application/Domain and providing
an explicit rejection path for wrong-turn intents.

It does not implement chess rules — those belong to the domain.
It does not import ``python-chess`` (``chess``) directly (ADR-004).
It does not depend on Pygame — that belongs to the interface layer (M5).

Example usage::

    from simple_chess.domain.match import MatchState
    from simple_chess.app.session import GameMode, GameSession
    from simple_chess.app.turn_controller import TurnController
    from simple_chess.app.move_processor import MoveProcessor

    match = MatchState()
    session = GameSession(mode=GameMode.PVP, match=match)
    controller = TurnController(session=session)
    processor = MoveProcessor(match=match, controller=controller)

    controller.receive_move_intent("e2e4")
    applied = processor.process_pending_intent()  # True — valid and applied
    controller.pending_intent                     # None — cleared by processor
"""
from __future__ import annotations

from simple_chess.app.turn_controller import TurnController
from simple_chess.domain.match import MatchState


class MoveProcessor:
    """Processes pending movement intents from the application layer.

    Coordinates between the :class:`TurnController`'s pending intent and the
    domain (:class:`MatchState`) for validation and application of chess moves.

    Responsibilities:
    - Read the pending move intent from the :class:`TurnController`.
    - Validate the move via the domain's public interface
      (:meth:`~simple_chess.domain.match.MatchState.is_legal_move`).
    - Apply the move via the domain if valid
      (:meth:`~simple_chess.domain.match.MatchState.push_uci`).
    - Clear the pending intent via
      :meth:`~simple_chess.app.turn_controller.TurnController.clear_intent`
      after processing, regardless of the outcome.
    - Return whether the move was valid and applied.

    Non-responsibilities (explicit scope boundaries):
    - Does **not** implement chess rules — delegates to the domain.
    - Does **not** import or depend on ``python-chess`` (``chess``) directly
      (ADR-004).
    - Does **not** depend on Pygame.
    - Does **not** receive movement intents — that is
      :meth:`~simple_chess.app.turn_controller.TurnController.receive_move_intent`.
    - Does **not** call the AI — that belongs to M4-04.

    Args:
        match: The domain :class:`~simple_chess.domain.match.MatchState`,
            used to validate and apply moves via its public interface.
        controller: The :class:`~simple_chess.app.turn_controller.TurnController`,
            used to read the pending intent and clear it after processing.
    """

    def __init__(self, match: MatchState, controller: TurnController) -> None:
        self._match = match
        self._controller = controller

    def process_pending_intent(self) -> bool:
        """Validate and apply the pending movement intent, then clear it.

        Reads the pending intent from the :class:`TurnController` and applies
        two sequential gates before touching the match state:

        1. **Turn-compatibility gate** (M6-02): the intent is checked against
           the current turn via
           :meth:`~simple_chess.app.turn_controller.TurnController.is_turn_compatible`.
           Intents from the wrong side are rejected at the Application layer
           without consulting the domain for full legality.  This is the
           explicit turn-enforcement contract of M6-02.

        2. **Legality gate**: if the intent is turn-compatible, move legality
           is validated via the domain's public interface
           (:meth:`~simple_chess.domain.match.MatchState.is_legal_move`).
           The domain remains the single source of truth for chess rules
           (ADR-004).

        The pending intent is always cleared via
        :meth:`~simple_chess.app.turn_controller.TurnController.clear_intent`
        regardless of the outcome, ensuring
        :attr:`~simple_chess.app.turn_controller.TurnController.pending_intent`
        is never left in an inconsistent state after processing.

        Returns:
            ``True`` if a pending intent existed, was turn-compatible, was a
            legal move, and was applied to the match state.  ``False`` if no
            intent was pending, the intent was turn-incompatible, or the move
            was illegal — the match state is not modified in any of these cases.
        """
        uci = self._controller.pending_intent

        if uci is None:
            return False

        # M6-02: explicit Application-layer turn-compatibility gate.
        # Intents from the wrong side are rejected before domain validation,
        # keeping the source of truth in the Application/Domain layer.
        if not self._controller.is_turn_compatible(uci):
            self._controller.clear_intent()
            return False

        is_valid = self._match.is_legal_move(uci)

        if is_valid:
            self._match.push_uci(uci)

        self._controller.clear_intent()
        return is_valid
