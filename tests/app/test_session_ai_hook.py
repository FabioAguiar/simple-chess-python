"""Tests for GameSession AI hook and state exposure (M4-04).

Covers the acceptance criteria of issue M4-04:

- is_computer_turn() returns True only when the current player is COMPUTER.
- is_computer_turn() is always False in PvP mode.
- request_ai_move() delegates to the provided callable without own AI logic.
- request_ai_move() passes the list of legal moves to the callable.
- request_ai_move() returns exactly what the callable returns.
- game_state_snapshot() exposes turn, mode, is_game_over, is_check, outcome,
  and legal_moves as plain Python types.
- game_state_snapshot() contains no python-chess types (ADR-004).
- session.py does not import python-chess directly (ADR-004).
"""
from __future__ import annotations

import importlib
import sys

import pytest

from simple_chess.app.session import GameMode, GameSession, PlayerType
from simple_chess.domain.match import MatchState


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def pvc_session() -> GameSession:
    """PvC session at the standard starting position (white=HUMAN, black=COMPUTER)."""
    match = MatchState()
    return GameSession(mode=GameMode.PVC, match=match)


@pytest.fixture()
def pvp_session() -> GameSession:
    """PvP session at the standard starting position (both sides HUMAN)."""
    match = MatchState()
    return GameSession(mode=GameMode.PVP, match=match)


def _make_session_after_one_move() -> GameSession:
    """PvC session where white (HUMAN) has already played e2e4.

    After e2e4 it is black's turn, which is COMPUTER in PvC mode.
    """
    match = MatchState()
    match.push_uci("e2e4")
    return GameSession(mode=GameMode.PVC, match=match)


# ---------------------------------------------------------------------------
# is_computer_turn — PvC mode
# ---------------------------------------------------------------------------


class TestIsComputerTurnPvC:
    def test_white_human_turn_is_not_computer(
        self, pvc_session: GameSession
    ) -> None:
        """At the start of a PvC game, white (HUMAN) plays first."""
        assert pvc_session.is_computer_turn() is False

    def test_black_computer_turn_is_computer(self) -> None:
        """After white's first move, it is black's (COMPUTER) turn."""
        session = _make_session_after_one_move()
        assert session.is_computer_turn() is True

    def test_is_computer_turn_consistent_with_current_player_type(
        self, pvc_session: GameSession
    ) -> None:
        """is_computer_turn() must agree with current_player_type()."""
        is_computer = pvc_session.current_player_type() == PlayerType.COMPUTER
        assert pvc_session.is_computer_turn() is is_computer


# ---------------------------------------------------------------------------
# is_computer_turn — PvP mode
# ---------------------------------------------------------------------------


class TestIsComputerTurnPvP:
    def test_pvp_white_turn_is_not_computer(
        self, pvp_session: GameSession
    ) -> None:
        assert pvp_session.is_computer_turn() is False

    def test_pvp_black_turn_is_not_computer(self) -> None:
        """Even after white moves, black is HUMAN in PvP."""
        match = MatchState()
        match.push_uci("e2e4")
        session = GameSession(mode=GameMode.PVP, match=match)
        assert session.is_computer_turn() is False


# ---------------------------------------------------------------------------
# request_ai_move
# ---------------------------------------------------------------------------


class TestRequestAiMove:
    def test_ai_fn_receives_legal_moves_list(
        self, pvc_session: GameSession
    ) -> None:
        """The callable receives the list of legal UCI moves."""
        received: list[list[str]] = []

        def capture_fn(legal_moves: list[str]) -> str:
            received.append(legal_moves)
            return legal_moves[0]

        pvc_session.request_ai_move(capture_fn)
        assert len(received) == 1
        assert isinstance(received[0], list)
        assert all(isinstance(m, str) for m in received[0])

    def test_ai_fn_receives_non_empty_legal_moves(
        self, pvc_session: GameSession
    ) -> None:
        """At the start of the game, legal moves list is non-empty."""
        received: list[list[str]] = []

        def capture_fn(legal_moves: list[str]) -> str:
            received.append(legal_moves)
            return legal_moves[0]

        pvc_session.request_ai_move(capture_fn)
        assert len(received[0]) > 0

    def test_returns_what_callable_returns(
        self, pvc_session: GameSession
    ) -> None:
        """request_ai_move returns exactly what the callable returns."""
        def fixed_fn(legal_moves: list[str]) -> str:
            return "e2e4"

        result = pvc_session.request_ai_move(fixed_fn)
        assert result == "e2e4"

    def test_callable_is_called_exactly_once(
        self, pvc_session: GameSession
    ) -> None:
        """The AI callable is invoked exactly once per request."""
        call_count: list[int] = [0]

        def counting_fn(legal_moves: list[str]) -> str:
            call_count[0] += 1
            return legal_moves[0]

        pvc_session.request_ai_move(counting_fn)
        assert call_count[0] == 1

    def test_no_ai_logic_in_session(
        self, pvc_session: GameSession
    ) -> None:
        """The session applies no move logic of its own — callable controls choice."""
        choices: list[str] = []

        def record_and_pick_last(legal_moves: list[str]) -> str:
            choices.extend(legal_moves)
            return legal_moves[-1]

        result = pvc_session.request_ai_move(record_and_pick_last)
        # The session must return whatever the callable returned, not a
        # modified or independently selected move.
        assert result == choices[-1]


# ---------------------------------------------------------------------------
# game_state_snapshot
# ---------------------------------------------------------------------------


class TestGameStateSnapshot:
    def test_snapshot_has_all_required_keys(
        self, pvc_session: GameSession
    ) -> None:
        snap = pvc_session.game_state_snapshot()
        assert set(snap.keys()) == {
            "turn",
            "mode",
            "is_game_over",
            "is_check",
            "outcome",
            "legal_moves",
            "board"
        }

    def test_turn_is_white_at_start(
        self, pvc_session: GameSession
    ) -> None:
        snap = pvc_session.game_state_snapshot()
        assert snap["turn"] == "white"

    def test_turn_is_black_after_white_moves(self) -> None:
        session = _make_session_after_one_move()
        snap = session.game_state_snapshot()
        assert snap["turn"] == "black"

    def test_mode_pvc(self, pvc_session: GameSession) -> None:
        snap = pvc_session.game_state_snapshot()
        assert snap["mode"] == "pvc"

    def test_mode_pvp(self, pvp_session: GameSession) -> None:
        snap = pvp_session.game_state_snapshot()
        assert snap["mode"] == "pvp"

    def test_is_game_over_false_at_start(
        self, pvc_session: GameSession
    ) -> None:
        snap = pvc_session.game_state_snapshot()
        assert snap["is_game_over"] is False

    def test_is_check_false_at_start(
        self, pvc_session: GameSession
    ) -> None:
        snap = pvc_session.game_state_snapshot()
        assert snap["is_check"] is False

    def test_outcome_none_at_start(
        self, pvc_session: GameSession
    ) -> None:
        snap = pvc_session.game_state_snapshot()
        assert snap["outcome"] is None

    def test_legal_moves_is_list_of_strings(
        self, pvc_session: GameSession
    ) -> None:
        snap = pvc_session.game_state_snapshot()
        assert isinstance(snap["legal_moves"], list)
        assert all(isinstance(m, str) for m in snap["legal_moves"])

    def test_legal_moves_non_empty_at_start(
        self, pvc_session: GameSession
    ) -> None:
        snap = pvc_session.game_state_snapshot()
        assert len(snap["legal_moves"]) > 0

    def test_snapshot_values_are_plain_python_types(
        self, pvc_session: GameSession
    ) -> None:
        """No python-chess types appear in the snapshot (ADR-004)."""
        snap = pvc_session.game_state_snapshot()
        for key, value in snap.items():
            if value is None:
                continue
            if isinstance(value, list):
                for item in value:
                    assert type(item).__module__ in ("builtins",), (
                        f"snapshot['{key}'] list item has unexpected type "
                        f"{type(item)} from module {type(item).__module__}"
                    )
            else:
                assert type(value).__module__ in ("builtins",), (
                    f"snapshot['{key}'] has unexpected type "
                    f"{type(value)} from module {type(value).__module__}"
                )

    def test_turn_is_string(self, pvc_session: GameSession) -> None:
        snap = pvc_session.game_state_snapshot()
        assert isinstance(snap["turn"], str)

    def test_mode_is_string(self, pvc_session: GameSession) -> None:
        snap = pvc_session.game_state_snapshot()
        assert isinstance(snap["mode"], str)

    def test_is_game_over_is_bool(self, pvc_session: GameSession) -> None:
        snap = pvc_session.game_state_snapshot()
        assert isinstance(snap["is_game_over"], bool)

    def test_is_check_is_bool(self, pvc_session: GameSession) -> None:
        snap = pvc_session.game_state_snapshot()
        assert isinstance(snap["is_check"], bool)


# ---------------------------------------------------------------------------
# ADR-004: no direct python-chess import in session
# ---------------------------------------------------------------------------


class TestNoPythonChessDirectImport:
    def test_session_module_does_not_expose_chess(self) -> None:
        """Verify session.py does not import python-chess directly (ADR-004)."""
        module_name = "simple_chess.app.session"
        mod = sys.modules.get(module_name) or importlib.import_module(module_name)
        assert not hasattr(mod, "chess"), (
            "session must not import python-chess directly (ADR-004)"
        )

    def test_app_init_does_not_expose_chess(self) -> None:
        """Verify the app __init__ does not expose python-chess (ADR-004)."""
        import simple_chess.app as app_pkg
        assert not hasattr(app_pkg, "chess"), (
            "simple_chess.app must not expose python-chess directly (ADR-004)"
        )
