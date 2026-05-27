"""Tests for the isolated random AI move-selection strategy."""
from __future__ import annotations

import ast
from pathlib import Path
import random

import pytest

from simple_chess.ai import RandomMoveSelector, choose_random_move


LEGAL_MOVES = ["e2e4", "d2d4", "g1f3", "c2c4"]


class TestRandomMoveSelector:
    def test_select_move_returns_one_of_the_legal_moves(self) -> None:
        selector = RandomMoveSelector(rng=random.Random(42))

        selected = selector.select_move(LEGAL_MOVES)

        assert selected in LEGAL_MOVES
        assert isinstance(selected, str)

    def test_select_move_is_deterministic_with_injected_rng(self) -> None:
        first_selector = RandomMoveSelector(rng=random.Random(42))
        second_selector = RandomMoveSelector(rng=random.Random(42))

        assert first_selector.select_move(LEGAL_MOVES) == second_selector.select_move(
            LEGAL_MOVES
        )

    def test_select_move_rejects_empty_legal_moves(self) -> None:
        selector = RandomMoveSelector(rng=random.Random(42))

        with pytest.raises(ValueError, match="without legal moves"):
            selector.select_move([])

    def test_select_move_does_not_mutate_legal_moves(self) -> None:
        legal_moves = list(LEGAL_MOVES)
        original_legal_moves = legal_moves.copy()
        selector = RandomMoveSelector(rng=random.Random(42))

        selected = selector.select_move(legal_moves)

        assert selected in original_legal_moves
        assert legal_moves == original_legal_moves


class TestChooseRandomMove:
    def test_choose_random_move_returns_one_of_the_legal_moves(self) -> None:
        selected = choose_random_move(LEGAL_MOVES, rng=random.Random(7))

        assert selected in LEGAL_MOVES
        assert isinstance(selected, str)

    def test_choose_random_move_is_deterministic_with_injected_rng(self) -> None:
        first = choose_random_move(LEGAL_MOVES, rng=random.Random(7))
        second = choose_random_move(LEGAL_MOVES, rng=random.Random(7))

        assert first == second

    def test_choose_random_move_rejects_empty_legal_moves(self) -> None:
        with pytest.raises(ValueError, match="without legal moves"):
            choose_random_move([], rng=random.Random(7))


class TestAiLayerBoundaries:
    def test_ai_package_exports_only_move_selection_contract(self) -> None:
        import simple_chess.ai as ai

        assert ai.__all__ == ["RandomMoveSelector", "choose_random_move"]
        assert ai.RandomMoveSelector is RandomMoveSelector
        assert ai.choose_random_move is choose_random_move
        assert not hasattr(ai, "pygame")
        assert not hasattr(ai, "chess")

    def test_ai_sources_do_not_import_pygame_or_python_chess(self) -> None:
        ai_root = _project_root() / "src" / "simple_chess" / "ai"
        checked_files: list[Path] = []

        for path in ai_root.rglob("*.py"):
            if "__pycache__" in path.parts:
                continue

            checked_files.append(path.relative_to(ai_root))
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            forbidden_imports = [
                node
                for node in ast.walk(tree)
                if _imports_module(node, "pygame") or _imports_module(node, "chess")
            ]

            assert forbidden_imports == [], (
                f"{path.relative_to(_project_root())} imports Pygame or python-chess "
                "directly"
            )

        assert len(checked_files) >= 1


def _project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _imports_module(node: ast.AST, module_name: str) -> bool:
    if isinstance(node, ast.Import):
        return any(_is_module(alias.name, module_name) for alias in node.names)
    if isinstance(node, ast.ImportFrom) and node.module is not None:
        return _is_module(node.module, module_name)
    return False


def _is_module(candidate: str, module_name: str) -> bool:
    return candidate == module_name or candidate.startswith(f"{module_name}.")
