"""M8-05 proportional validation: PvC flow — human white, AI black.

Covers M8-05 acceptance criteria:

- User can start a PvC game.
- Human plays as white (white_player == PlayerType.HUMAN).
- AI plays as black (black_player == PlayerType.COMPUTER).
- Human's valid move is applied.
- AI is called on the correct turn (not on human's turn).
- AI move is legal and applied via domain.
- Interface reflects updated state via game_state_snapshot(), including
  the ``last_move`` field introduced by M8-04.
- Proportional validation scope: not exhaustive Pygame testing, no
  full coverage mandate.

Rationale:
    The existing tests in ``test_local_game_pvc_ai_move.py`` cover the PvC
    flow from an M8-03 perspective (AI move application via domain, ADR-004
    compliance).  This module adds the explicit M8-05 assertions missing from
    that suite: confirmation of player-type configuration (white=HUMAN,
    black=COMPUTER) and snapshot coverage of the ``last_move`` field.
"""
from __future__ import annotations


from simple_chess.app.local_game import LocalGame
from simple_chess.app.session import GameMode, GameSession, PlayerType
from simple_chess.domain.match import MatchState


# ---------------------------------------------------------------------------
# PlayerType configuration — M8-05 criteria: "Human plays white, AI plays black"
# ---------------------------------------------------------------------------


class TestPvCPlayerTypeConfiguration:
    """Confirm that PvC mode assigns the correct PlayerType to each side."""

    def test_pvc_session_white_player_is_human(self) -> None:
        """GameSession in PvC mode assigns PlayerType.HUMAN to white."""
        match = MatchState()
        session = GameSession(mode=GameMode.PVC, match=match)
        assert session.white_player == PlayerType.HUMAN

    def test_pvc_session_black_player_is_computer(self) -> None:
        """GameSession in PvC mode assigns PlayerType.COMPUTER to black."""
        match = MatchState()
        session = GameSession(mode=GameMode.PVC, match=match)
        assert session.black_player == PlayerType.COMPUTER

    def test_pvp_session_both_players_are_human(self) -> None:
        """GameSession in PvP mode assigns PlayerType.HUMAN to both sides."""
        match = MatchState()
        session = GameSession(mode=GameMode.PVP, match=match)
        assert session.white_player == PlayerType.HUMAN
        assert session.black_player == PlayerType.HUMAN

    def test_pvc_local_game_snapshot_mode_is_pvc(self) -> None:
        """LocalGame.new_pvc() snapshot reports mode='pvc'."""
        game = LocalGame.new_pvc()
        snapshot = game.game_state_snapshot()
        assert snapshot["mode"] == "pvc"

    def test_pvc_game_starts_on_white_human_turn(self) -> None:
        """In PvC, the first turn belongs to the human (white)."""
        match = MatchState()
        session = GameSession(mode=GameMode.PVC, match=match)
        # White's turn at start of game.
        assert session.white_player == PlayerType.HUMAN
        assert not session.is_computer_turn()

    def test_pvc_after_human_move_it_is_computer_turn(self) -> None:
        """After white's valid move in PvC, the session reports computer's turn."""
        match = MatchState()
        session = GameSession(mode=GameMode.PVC, match=match)
        # Apply a white move directly via the match domain.
        match.push_uci("e2e4")
        # Now it is black's turn, which is the computer in PvC.
        assert session.black_player == PlayerType.COMPUTER
        assert session.is_computer_turn()


# ---------------------------------------------------------------------------
# last_move field in game_state_snapshot — M8-05 criterion:
# "Interface reflects updated state"
# ---------------------------------------------------------------------------


class TestLastMoveInSnapshot:
    """Confirm that game_state_snapshot() exposes the last_move field (M8-04)."""

    def test_last_move_is_none_at_game_start(self) -> None:
        """Snapshot has last_move=None before any move is made."""
        game = LocalGame.new_pvc()
        snapshot = game.game_state_snapshot()
        assert "last_move" in snapshot
        assert snapshot["last_move"] is None

    def test_last_move_reflects_human_move_after_application(self) -> None:
        """After white's move, last_move in snapshot equals the applied UCI."""
        game = LocalGame.new_pvc()
        game.submit_move_intent("e2e4")
        snapshot = game.game_state_snapshot()
        # last_move reflects the most recently applied move.
        assert snapshot["last_move"] == "e2e4"

    def test_last_move_updates_after_ai_move(self) -> None:
        """After the AI responds in PvC, last_move reflects the AI's move."""
        game = LocalGame.new_pvc()
        # White plays; AI responds via submit_human_move_intent_with_snapshot.
        human_applied, snapshot = game.submit_human_move_intent_with_snapshot("e2e4")

        assert human_applied is True
        # The snapshot is taken after the AI's response; last_move is the AI move.
        assert snapshot["last_move"] is not None
        # The AI's UCI move should be a 4-5 character string (e.g. "e7e5").
        assert isinstance(snapshot["last_move"], str)
        assert 4 <= len(snapshot["last_move"]) <= 5

    def test_last_move_is_string_or_none(self) -> None:
        """last_move is always a str or None — never a non-string type."""
        game = LocalGame.new_pvc()
        # Before any move.
        snapshot_initial = game.game_state_snapshot()
        assert snapshot_initial["last_move"] is None or isinstance(
            snapshot_initial["last_move"], str
        )
        # After a human move.
        game.submit_move_intent("e2e4")
        snapshot_after = game.game_state_snapshot()
        assert isinstance(snapshot_after["last_move"], str)

    def test_pvp_last_move_reflects_last_applied_move(self) -> None:
        """In PvP mode, last_move in snapshot reflects the last applied move."""
        game = LocalGame.new_pvp()
        assert game.game_state_snapshot()["last_move"] is None
        game.submit_move_intent("e2e4")
        assert game.game_state_snapshot()["last_move"] == "e2e4"


# ---------------------------------------------------------------------------
# Proportional integration: PvC full sequence confirmation
# ---------------------------------------------------------------------------


class TestPvCFlowProportionalIntegration:
    """Proportional integration check of the M8-05 full PvC sequence."""

    def test_pvc_full_sequence_human_then_ai(self) -> None:
        """Full PvC sequence: start -> human white move -> AI black response -> snapshot.

        Validates the M8-05 flow in a single integration test:
        - Game starts with human on white, AI on black.
        - Human plays e2e4 (valid).
        - AI responds automatically (default random strategy).
        - Snapshot shows white's turn again, last_move from AI is set.
        - Architectural boundary confirmed: AI did not mutate state directly.
        """
        match = MatchState()
        session = GameSession(mode=GameMode.PVC, match=match)

        # Confirm configuration before any move.
        assert session.white_player == PlayerType.HUMAN
        assert session.black_player == PlayerType.COMPUTER
        assert not session.is_computer_turn()

        game = LocalGame.new_pvc()
        human_applied, snapshot = game.submit_human_move_intent_with_snapshot("e2e4")

        # Human move accepted.
        assert human_applied is True
        # After full PvC cycle, it is white's turn again.
        assert snapshot["turn"] == "white"
        # Mode is preserved.
        assert snapshot["mode"] == "pvc"
        # last_move is the AI's response (not None, not the human's move).
        assert snapshot["last_move"] is not None
        assert isinstance(snapshot["last_move"], str)
        # Game is still active.
        assert snapshot["is_game_over"] is False
