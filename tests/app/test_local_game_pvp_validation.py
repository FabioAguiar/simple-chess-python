"""Proportional M6-05 validation for local PvP and layer boundaries."""
from __future__ import annotations

import ast
from pathlib import Path

from simple_chess.app import LocalGame


def test_pvp_sequence_updates_application_snapshot_after_valid_moves() -> None:
    game = LocalGame.new_pvp()

    white_applied, after_white = game.submit_move_intent_with_snapshot("e2e4")
    black_applied, after_black = game.submit_move_intent_with_snapshot("d7d5")

    assert white_applied is True
    assert after_white["turn"] == "black"
    assert after_white["board"]["e4"] == "P"
    assert "e2" not in after_white["board"]

    assert black_applied is True
    assert after_black["turn"] == "white"
    assert after_black["board"]["d5"] == "p"
    assert "d7" not in after_black["board"]


def test_invalid_pvp_move_is_rejected_without_state_mutation() -> None:
    game = LocalGame.new_pvp()
    before = game.game_state_snapshot()

    applied, after = game.submit_move_intent_with_snapshot("e2e5")

    assert applied is False
    assert after["turn"] == before["turn"] == "white"
    assert after["board"] == before["board"]


def test_wrong_turn_pvp_move_is_rejected_without_state_mutation() -> None:
    game = LocalGame.new_pvp()
    before = game.game_state_snapshot()

    applied, after = game.submit_move_intent_with_snapshot("e7e5")

    assert applied is False
    assert after["turn"] == before["turn"] == "white"
    assert after["board"] == before["board"]


def test_pvp_capture_is_reflected_in_application_snapshot() -> None:
    game = LocalGame.new_pvp()

    assert game.submit_move_intent("e2e4") is True
    assert game.submit_move_intent("d7d5") is True
    capture_applied, after_capture = game.submit_move_intent_with_snapshot("e4d5")

    assert capture_applied is True
    assert after_capture["turn"] == "black"
    assert after_capture["board"]["d5"] == "P"
    assert "e4" not in after_capture["board"]
    assert "d7" not in after_capture["board"]


def test_ui_layer_does_not_import_domain_or_python_chess_directly() -> None:
    project_root = Path(__file__).resolve().parents[2]
    ui_root = project_root / "src" / "simple_chess" / "ui"
    checked_files: list[Path] = []

    for path in ui_root.rglob("*.py"):
        if "__pycache__" in path.parts:
            continue

        checked_files.append(path.relative_to(project_root))
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        forbidden_imports = [
            node
            for node in ast.walk(tree)
            if _imports_module(node, "chess")
            or _imports_module(node, "simple_chess.domain")
        ]

        assert forbidden_imports == [], (
            f"{path.relative_to(project_root)} must use the Application layer "
            "instead of importing Domain or python-chess directly"
        )

    assert checked_files


def _imports_module(node: ast.AST, module_name: str) -> bool:
    if isinstance(node, ast.Import):
        return any(_is_module(alias.name, module_name) for alias in node.names)
    if isinstance(node, ast.ImportFrom) and node.module is not None:
        return _is_module(node.module, module_name)
    return False


def _is_module(candidate: str, module_name: str) -> bool:
    return candidate == module_name or candidate.startswith(f"{module_name}.")
