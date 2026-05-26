"""Application facade for local chess game flows."""
from __future__ import annotations

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

    def submit_move_intent(self, uci: str) -> bool:
        """Receive a UI movement intent and return whether it was applied."""
        self._turn_controller.receive_move_intent(uci)
        return self._move_processor.process_pending_intent()

    def game_state_snapshot(self) -> dict[str, object]:
        """Return the current game state as plain Python values for the UI."""
        return self._session.game_state_snapshot()
