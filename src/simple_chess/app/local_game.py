"""Application facade for local chess game flows."""
from __future__ import annotations

from collections.abc import Callable

from simple_chess.ai import choose_random_move
from simple_chess.app.move_processor import MoveProcessor
from simple_chess.app.session import GameMode, GameSession
from simple_chess.app.turn_controller import TurnController
from simple_chess.domain.match import MatchState


class LocalGame:
    """Coordinate a local game session for the UI layer.

    The UI sends movement intents to this facade and receives snapshots back.
    Domain state and rule validation remain behind the Application layer.
    """

    def __init__(
        self,
        session: GameSession,
        turn_controller: TurnController,
        move_processor: MoveProcessor,
    ) -> None:
        self._session = session
        self._turn_controller = turn_controller
        self._move_processor = move_processor

    @classmethod
    def new(cls, mode: GameMode = GameMode.PVP) -> "LocalGame":
        """Create a local game for the selected mode."""
        if mode == GameMode.PVP:
            return cls.new_pvp()
        if mode == GameMode.PVC:
            return cls.new_pvc()
        raise ValueError(f"Unsupported game mode: {mode!r}")

    @classmethod
    def new_pvp(cls) -> "LocalGame":
        """Create a local player-vs-player game for two human players."""
        match = MatchState()
        session = GameSession(mode=GameMode.PVP, match=match)
        turn_controller = TurnController(session=session)
        move_processor = MoveProcessor(match=match, controller=turn_controller)
        return cls(
            session=session,
            turn_controller=turn_controller,
            move_processor=move_processor,
        )

    @classmethod
    def new_pvc(cls) -> "LocalGame":
        """Create a local player-vs-computer game (white human, black AI).

        The session is configured with :attr:`~simple_chess.app.session.GameMode.PVC`
        so that :meth:`~simple_chess.app.session.GameSession.is_computer_turn`
        returns ``True`` on black's turn. The AI callable is injected at call
        time via :meth:`request_and_apply_ai_move`, keeping the AI layer
        decoupled from the Application layer.
        """
        match = MatchState()
        session = GameSession(mode=GameMode.PVC, match=match)
        turn_controller = TurnController(session=session)
        move_processor = MoveProcessor(match=match, controller=turn_controller)
        return cls(
            session=session,
            turn_controller=turn_controller,
            move_processor=move_processor,
        )

    def submit_move_intent(self, uci: str) -> bool:
        """Receive a UI movement intent and return whether it was applied."""
        self._turn_controller.receive_move_intent(uci)
        return self._move_processor.process_pending_intent()

    def submit_move_intent_with_snapshot(
        self,
        uci: str,
    ) -> tuple[bool, dict[str, object]]:
        """Apply a UI movement intent and return the refreshed game state.

        The UI can use this to redraw from the Application-layer snapshot
        immediately after each accepted move, including captures and all
        piece position updates, without accessing the domain directly.
        """
        move_applied = self.submit_move_intent(uci)
        return move_applied, self.game_state_snapshot()

    def submit_human_move_intent_with_snapshot(
        self,
        uci: str,
        ai_fn: Callable[[list[str]], str] = choose_random_move,
    ) -> tuple[bool, dict[str, object]]:
        """Apply a human move and continue the PvC turn when appropriate.

        The human move is always processed first through the same
        Application/Domain path used by regular move intents.  Only after a
        valid human move updates domain state does the application inspect
        the refreshed turn.  If the session is PvC, the game is still active,
        and the refreshed turn belongs to the computer, the AI is asked for a
        candidate move and that move is applied through the domain as well.

        Args:
            uci: Human move intent in UCI notation.
            ai_fn: AI selector callable.  Defaults to the random strategy.

        Returns:
            A tuple with whether the human move was applied and the game
            snapshot after any eligible AI response.
        """
        human_move_applied = self.submit_move_intent(uci)

        if human_move_applied and self._should_request_ai_move():
            self.request_and_apply_ai_move(ai_fn)

        return human_move_applied, self.game_state_snapshot()

    def _should_request_ai_move(self) -> bool:
        """Return whether the app should request a PvC AI response now."""
        return (
            self._session.mode == GameMode.PVC
            and self._session.is_computer_turn()
            and not self._session.match.is_game_over()
            and bool(self._session.match.legal_move_ucis())
        )

    def request_and_apply_ai_move(
        self, ai_fn: Callable[[list[str]], str]
    ) -> bool:
        """Request a move from an AI callable and apply it via the domain.

        Should be called only when the session reports it is the computer's
        turn (:meth:`~simple_chess.app.session.GameSession.is_computer_turn`
        returns ``True``).  The AI callable selects a move from the available
        legal moves supplied by the domain; the result is routed through
        :class:`~simple_chess.app.turn_controller.TurnController` and applied
        via :class:`~simple_chess.app.move_processor.MoveProcessor`, preserving
        the AI/Application/Domain boundary: the AI returns only a UCI
        candidate, the application applies it through the domain.

        Compatible AI callables include
        :func:`~simple_chess.ai.choose_random_move` and
        :meth:`~simple_chess.ai.RandomMoveSelector.select_move`.

        Args:
            ai_fn: A callable that receives a list of legal UCI move strings
                and returns one chosen UCI move string.

        Returns:
            ``True`` if the AI's chosen move was accepted as turn-compatible,
            passed domain-level legality validation, and was applied to the
            match state.  ``False`` otherwise.

        Raises:
            RuntimeError: If called when it is not the computer's turn,
                preventing the AI from acting during a human player's turn.
        """
        if not self._session.is_computer_turn():
            raise RuntimeError(
                "request_and_apply_ai_move called when it is not the computer's turn."
            )
        uci = self._session.request_ai_move(ai_fn)
        return self.submit_move_intent(uci)

    def game_state_snapshot(self) -> dict[str, object]:
        """Return the current game state as plain Python values for the UI."""
        return self._session.game_state_snapshot()
