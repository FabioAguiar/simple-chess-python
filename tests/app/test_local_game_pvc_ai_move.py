"""Proportional M8-03 validation: AI move application via domain.

Covers M8-03 acceptance criteria:

- The AI returns a legal move choice for the application.
- The application applies the AI move via the domain boundary.
- The AI does not mutate game state directly.
- The domain rejects invalid moves even when originating from the AI.
- The integration remains local.

Validates:
- AI callable is invoked on the computer's turn with legal moves from the domain.
- The chosen move is applied through the domain (Application/Domain boundary).
- Calling request_and_apply_ai_move on the human's turn raises RuntimeError.
- An illegal move returned by the AI is rejected by the domain; state unchanged.
- submit_human_move_intent_with_snapshot chains human move and AI response in PvC.
- In PvP mode, no AI is triggered after a human move.
- The AI callable receives only plain Python types (ADR-004 isolation).
"""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

from simple_chess.app.local_game import LocalGame


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _pvc_after_e2e4() -> LocalGame:
    """Return a PvC LocalGame where white (human) has played e2e4.

    It is now black's (computer) turn.
    """
    game = LocalGame.new_pvc()
    game.submit_move_intent("e2e4")
    return game


# ---------------------------------------------------------------------------
# request_and_apply_ai_move
# ---------------------------------------------------------------------------


class TestRequestAndApplyAiMove:
    def test_ai_move_is_applied_via_domain_on_computer_turn(self) -> None:
        """AI move is applied through the domain; game state updates correctly."""
        game = _pvc_after_e2e4()
        state_before = game.game_state_snapshot()
        assert state_before["turn"] == "black"

        applied = game.request_and_apply_ai_move(lambda moves: moves[0])

        assert applied is True
        state_after = game.game_state_snapshot()
        # Domain updated the turn after applying the AI move.
        assert state_after["turn"] == "white"
        # The board changed — a black piece moved.
        assert state_after["board"] != state_before["board"]

    def test_raises_runtime_error_on_human_turn(self) -> None:
        """RuntimeError is raised when called during the human player's turn."""
        game = LocalGame.new_pvc()
        assert game.game_state_snapshot()["turn"] == "white"  # human's turn

        with pytest.raises(RuntimeError):
            game.request_and_apply_ai_move(lambda moves: moves[0])

    def test_ai_callable_receives_legal_moves_as_plain_strings(self) -> None:
        """AI callable receives a non-empty list of legal UCI strings."""
        game = _pvc_after_e2e4()
        received: list[list[str]] = []

        def capture(legal_moves: list[str]) -> str:
            received.append(legal_moves)
            return legal_moves[0]

        game.request_and_apply_ai_move(capture)

        assert len(received) == 1
        legal = received[0]
        assert isinstance(legal, list)
        assert len(legal) > 0
        assert all(isinstance(m, str) for m in legal)

    def test_ai_callable_receives_current_legal_moves_from_domain(self) -> None:
        """Legal moves passed to the AI reflect the current domain state."""
        game = _pvc_after_e2e4()
        domain_legal = game.game_state_snapshot()["legal_moves"]

        received: list[list[str]] = []

        def capture(legal_moves: list[str]) -> str:
            received.append(list(legal_moves))
            return legal_moves[0]

        game.request_and_apply_ai_move(capture)

        assert sorted(received[0]) == sorted(domain_legal)

    def test_ai_callable_is_invoked_exactly_once(self) -> None:
        """The AI callable is invoked exactly once per call."""
        game = _pvc_after_e2e4()
        call_count = [0]

        def counting(legal_moves: list[str]) -> str:
            call_count[0] += 1
            return legal_moves[0]

        game.request_and_apply_ai_move(counting)
        assert call_count[0] == 1

    def test_domain_rejects_illegal_ai_move_and_state_is_unchanged(self) -> None:
        """An illegal move returned by the AI is rejected; state is not mutated."""
        game = _pvc_after_e2e4()
        state_before = game.game_state_snapshot()

        # "e7e4" is turn-compatible (black pawn at e7, black's turn) but not a
        # legal chess move (pawn cannot advance three squares in one move).
        applied = game.request_and_apply_ai_move(lambda _: "e7e4")

        assert applied is False
        state_after = game.game_state_snapshot()
        assert state_after["turn"] == state_before["turn"]
        assert state_after["board"] == state_before["board"]

    def test_ai_does_not_mutate_state_directly(self) -> None:
        """The AI callable cannot alter game state; it only returns a move string."""
        game = _pvc_after_e2e4()

        mutation_attempted = [False]

        def side_effect(legal_moves: list[str]) -> str:
            # Verify the AI only receives strings — no mutable domain objects.
            mutation_attempted[0] = True
            assert isinstance(legal_moves, list)
            assert all(isinstance(m, str) for m in legal_moves)
            return legal_moves[0]

        applied = game.request_and_apply_ai_move(side_effect)

        assert mutation_attempted[0] is True
        assert applied is True
        # Only the application/domain boundary changed the state.
        assert game.game_state_snapshot()["turn"] == "white"

    def test_ai_move_chosen_from_legal_moves_is_accepted(self) -> None:
        """A move from the legal-moves list is always accepted by the domain."""
        game = _pvc_after_e2e4()
        legal = game.game_state_snapshot()["legal_moves"]

        for candidate in legal[:3]:  # check first few for speed
            g = _pvc_after_e2e4()
            applied = g.request_and_apply_ai_move(lambda _: candidate)
            assert applied is True, f"Legal move {candidate!r} was rejected unexpectedly"


# ---------------------------------------------------------------------------
# AI response not triggered when conditions not met
# ---------------------------------------------------------------------------


class TestAiNotTriggeredOutsideComputerTurn:
    def test_no_ai_response_in_pvp_mode(self) -> None:
        """In PvP mode, the AI callable is never invoked."""
        game = LocalGame.new_pvp()
        ai_called = [False]

        def ai_fn(moves: list[str]) -> str:
            ai_called[0] = True
            return moves[0]

        game.submit_human_move_intent_with_snapshot("e2e4", ai_fn)
        assert ai_called[0] is False

    def test_no_ai_response_after_invalid_human_move(self) -> None:
        """If the human move is invalid, the AI is not triggered."""
        game = LocalGame.new_pvc()
        ai_called = [False]

        def ai_fn(moves: list[str]) -> str:
            ai_called[0] = True
            return moves[0]

        applied, _ = game.submit_human_move_intent_with_snapshot("e2e5", ai_fn)

        assert applied is False
        assert ai_called[0] is False

    def test_no_ai_response_after_wrong_turn_human_move(self) -> None:
        """Wrong-turn human move (black piece on white's turn) does not trigger AI."""
        game = LocalGame.new_pvc()
        ai_called = [False]

        def ai_fn(moves: list[str]) -> str:
            ai_called[0] = True
            return moves[0]

        applied, _ = game.submit_human_move_intent_with_snapshot("e7e5", ai_fn)

        assert applied is False
        assert ai_called[0] is False


# ---------------------------------------------------------------------------
# submit_human_move_intent_with_snapshot — PvC integration
# ---------------------------------------------------------------------------


class TestSubmitHumanMoveIntentWithSnapshotPvC:
    def test_valid_human_move_triggers_ai_and_returns_turn_to_white(self) -> None:
        """After a valid white move in PvC, the AI responds and it becomes white's turn."""
        game = LocalGame.new_pvc()

        human_applied, state_after = game.submit_human_move_intent_with_snapshot("e2e4")

        assert human_applied is True
        # The AI responded: both human and AI moves were applied.
        assert state_after["turn"] == "white"

    def test_invalid_human_move_does_not_trigger_ai_response(self) -> None:
        """Invalid human move returns False; turn and board remain unchanged."""
        game = LocalGame.new_pvc()
        ai_called = [False]

        def ai_fn(moves: list[str]) -> str:
            ai_called[0] = True
            return moves[0]

        human_applied, state_after = game.submit_human_move_intent_with_snapshot(
            "e2e5", ai_fn
        )

        assert human_applied is False
        assert ai_called[0] is False
        assert state_after["turn"] == "white"

    def test_pvp_human_move_does_not_trigger_ai_callable(self) -> None:
        """In PvP mode, a valid human move does not invoke the AI callable."""
        game = LocalGame.new_pvp()
        ai_called = [False]

        def ai_fn(moves: list[str]) -> str:
            ai_called[0] = True
            return moves[0]

        human_applied, state_after = game.submit_human_move_intent_with_snapshot(
            "e2e4", ai_fn
        )

        assert human_applied is True
        assert ai_called[0] is False
        assert state_after["turn"] == "black"  # black human's turn

    def test_snapshot_reflects_state_after_both_moves(self) -> None:
        """The returned snapshot is taken after both human and AI moves."""
        game = LocalGame.new_pvc()

        _, state = game.submit_human_move_intent_with_snapshot("e2e4")

        # White pawn moved to e4; AI responded with a black move; turn returned to white.
        assert state["turn"] == "white"
        board = state["board"]
        assert board.get("e4") == "P"  # white pawn still on e4
        assert "e2" not in board  # pawn no longer on e2

    def test_snapshot_shows_ai_moved_after_human(self) -> None:
        """The board in the snapshot reflects the AI's response move."""
        game = LocalGame.new_pvc()
        state_initial = game.game_state_snapshot()

        _, state_after = game.submit_human_move_intent_with_snapshot("e2e4")

        # Board changed beyond just the human move.
        assert state_after["board"] != state_initial["board"]


# ---------------------------------------------------------------------------
# AI isolation: ADR-004 compliance
# ---------------------------------------------------------------------------


class TestAiIsolation:
    def test_ai_callable_receives_only_builtin_types(self) -> None:
        """AI callable receives only builtins types — no python-chess types (ADR-004)."""
        game = _pvc_after_e2e4()
        type_modules: list[str] = []

        def inspect(legal_moves: list[str]) -> str:
            type_modules.append(type(legal_moves).__module__)
            for move in legal_moves:
                type_modules.append(type(move).__module__)
            return legal_moves[0]

        game.request_and_apply_ai_move(inspect)

        assert all(m == "builtins" for m in type_modules), (
            "AI callable must receive only builtins types — no python-chess types"
        )

    def test_ai_module_does_not_import_pygame_or_python_chess(self) -> None:
        """The AI module must not import Pygame, python-chess, or domain internals."""
        project_root = Path(__file__).resolve().parents[2]
        ai_root = project_root / "src" / "simple_chess" / "ai"
        checked_files: list[Path] = []

        for path in ai_root.rglob("*.py"):
            if "__pycache__" in path.parts:
                continue
            checked_files.append(path)
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))

            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        assert not alias.name.startswith("pygame"), (
                            f"{path.name}: AI must not import Pygame"
                        )
                        assert not alias.name.startswith("chess"), (
                            f"{path.name}: AI must not import python-chess directly"
                        )
                elif isinstance(node, ast.ImportFrom) and node.module is not None:
                    assert not node.module.startswith("pygame"), (
                        f"{path.name}: AI must not import Pygame"
                    )
                    assert not node.module.startswith("chess"), (
                        f"{path.name}: AI must not import python-chess directly"
                    )
                    assert not node.module.startswith("simple_chess.domain"), (
                        f"{path.name}: AI must not import domain internals directly"
                    )

        assert checked_files, "No AI source files were checked — verify ai_root path"
