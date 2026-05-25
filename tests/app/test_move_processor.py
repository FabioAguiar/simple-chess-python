"""Tests for MoveProcessor (M4-03).

Covers the acceptance criteria of issue M4-03:

- A valid move is validated via the domain (MatchState.is_legal_move).
- A valid move is applied to the domain match state (MatchState.push_uci).
- An invalid move does not alter the match state.
- A malformed UCI string does not alter the match state.
- The pending intent is always cleared after processing — valid or invalid.
- No pending intent (None) results in False with no side effects.
- The application layer does not import python-chess directly (ADR-004).
"""
from __future__ import annotations

import importlib
import sys

import pytest

from simple_chess.app.move_processor import MoveProcessor
from simple_chess.app.session import GameMode, GameSession
from simple_chess.app.turn_controller import TurnController
from simple_chess.domain.match import MatchState


@pytest.fixture()
def components() -> tuple[MatchState, TurnController, MoveProcessor]:
    """Create a standard PvP setup with match, controller, and processor."""
    match = MatchState()
    session = GameSession(mode=GameMode.PVP, match=match)
    controller = TurnController(session=session)
    processor = MoveProcessor(match=match, controller=controller)
    return match, controller, processor


# ---------------------------------------------------------------------------
# Valid move
# ---------------------------------------------------------------------------


class TestValidMove:
    def test_valid_move_returns_true(
        self, components: tuple[MatchState, TurnController, MoveProcessor]
    ) -> None:
        match, controller, processor = components
        controller.receive_move_intent("e2e4")
        result = processor.process_pending_intent()
        assert result is True

    def test_valid_move_is_applied_to_match_state(
        self, components: tuple[MatchState, TurnController, MoveProcessor]
    ) -> None:
        match, controller, processor = components
        controller.receive_move_intent("e2e4")
        processor.process_pending_intent()
        # After e2e4 it is black's turn — confirms the move was applied
        assert match.current_turn() == "black"

    def test_valid_move_clears_pending_intent(
        self, components: tuple[MatchState, TurnController, MoveProcessor]
    ) -> None:
        match, controller, processor = components
        controller.receive_move_intent("e2e4")
        processor.process_pending_intent()
        assert controller.pending_intent is None


# ---------------------------------------------------------------------------
# Invalid move
# ---------------------------------------------------------------------------


class TestInvalidMove:
    def test_illegal_move_returns_false(
        self, components: tuple[MatchState, TurnController, MoveProcessor]
    ) -> None:
        match, controller, processor = components
        controller.receive_move_intent("e2e5")  # illegal from starting position
        result = processor.process_pending_intent()
        assert result is False

    def test_illegal_move_does_not_alter_match_state(
        self, components: tuple[MatchState, TurnController, MoveProcessor]
    ) -> None:
        match, controller, processor = components
        controller.receive_move_intent("e2e5")  # illegal
        processor.process_pending_intent()
        # Board state unchanged — still white's turn
        assert match.current_turn() == "white"

    def test_malformed_uci_returns_false(
        self, components: tuple[MatchState, TurnController, MoveProcessor]
    ) -> None:
        match, controller, processor = components
        controller.receive_move_intent("not_a_uci")
        result = processor.process_pending_intent()
        assert result is False

    def test_malformed_uci_does_not_alter_match_state(
        self, components: tuple[MatchState, TurnController, MoveProcessor]
    ) -> None:
        match, controller, processor = components
        controller.receive_move_intent("not_a_uci")
        processor.process_pending_intent()
        assert match.current_turn() == "white"

    def test_illegal_move_clears_pending_intent(
        self, components: tuple[MatchState, TurnController, MoveProcessor]
    ) -> None:
        match, controller, processor = components
        controller.receive_move_intent("e2e5")
        processor.process_pending_intent()
        assert controller.pending_intent is None

    def test_malformed_uci_clears_pending_intent(
        self, components: tuple[MatchState, TurnController, MoveProcessor]
    ) -> None:
        match, controller, processor = components
        controller.receive_move_intent("not_a_uci")
        processor.process_pending_intent()
        assert controller.pending_intent is None


# ---------------------------------------------------------------------------
# No pending intent
# ---------------------------------------------------------------------------


class TestNoPendingIntent:
    def test_no_intent_returns_false(
        self, components: tuple[MatchState, TurnController, MoveProcessor]
    ) -> None:
        match, controller, processor = components
        result = processor.process_pending_intent()
        assert result is False

    def test_no_intent_does_not_alter_match_state(
        self, components: tuple[MatchState, TurnController, MoveProcessor]
    ) -> None:
        match, controller, processor = components
        processor.process_pending_intent()
        assert match.current_turn() == "white"

    def test_no_intent_pending_intent_remains_none(
        self, components: tuple[MatchState, TurnController, MoveProcessor]
    ) -> None:
        match, controller, processor = components
        processor.process_pending_intent()
        assert controller.pending_intent is None


# ---------------------------------------------------------------------------
# ADR-004: no direct python-chess import in the application layer
# ---------------------------------------------------------------------------


class TestNoPythonChessDirectImport:
    def test_move_processor_module_does_not_expose_chess(self) -> None:
        """Verify no direct python-chess import in move_processor (ADR-004)."""
        module_name = "simple_chess.app.move_processor"
        mod = sys.modules.get(module_name) or importlib.import_module(module_name)
        assert not hasattr(mod, "chess"), (
            "move_processor must not import python-chess directly (ADR-004)"
        )

    def test_app_init_does_not_expose_chess(self) -> None:
        """Verify the app __init__ does not expose python-chess (ADR-004)."""
        import simple_chess.app as app_pkg
        assert not hasattr(app_pkg, "chess"), (
            "simple_chess.app must not expose python-chess directly (ADR-004)"
        )
