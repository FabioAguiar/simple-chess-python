"""Tests for match state move application and rejection."""
from __future__ import annotations

import ast
from pathlib import Path
import unittest

import simple_chess.domain as domain
from simple_chess.domain import MatchState


class MatchStateMoveApplicationTests(unittest.TestCase):
    def test_push_uci_applies_legal_move_and_updates_observable_state(self) -> None:
        match = MatchState()

        self.assertEqual(match.current_turn(), "white")
        self.assertIn("e2e4", match.legal_move_ucis())

        match.push_uci("e2e4")

        self.assertEqual(match.current_turn(), "black")
        self.assertNotIn("e2e4", match.legal_move_ucis())
        self.assertIn("e7e5", match.legal_move_ucis())

    def test_push_uci_rejects_invalid_uci_and_preserves_state(self) -> None:
        match = MatchState()
        turn_before = match.current_turn()
        legal_moves_before = match.legal_move_ucis()

        with self.assertRaisesRegex(ValueError, "Invalid UCI string"):
            match.push_uci("invalid")

        self.assertEqual(match.current_turn(), turn_before)
        self.assertEqual(match.legal_move_ucis(), legal_moves_before)

    def test_push_uci_rejects_illegal_move_and_preserves_state(self) -> None:
        match = MatchState()
        turn_before = match.current_turn()
        legal_moves_before = match.legal_move_ucis()

        with self.assertRaisesRegex(ValueError, "Illegal move in current position"):
            match.push_uci("e2e5")

        self.assertEqual(match.current_turn(), turn_before)
        self.assertEqual(match.legal_move_ucis(), legal_moves_before)


class DomainBoundaryTests(unittest.TestCase):
    def test_domain_public_contract_exposes_only_domain_types(self) -> None:
        self.assertEqual(domain.__all__, ["MatchState"])
        self.assertIs(domain.MatchState, MatchState)
        self.assertFalse(hasattr(domain, "chess"))

    def test_python_chess_is_not_imported_outside_domain(self) -> None:
        package_root = Path(__file__).resolve().parents[1]
        checked_files: list[Path] = []

        for path in package_root.rglob("*.py"):
            relative_path = path.relative_to(package_root)
            if relative_path.parts[0] == "domain":
                continue

            checked_files.append(relative_path)
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            chess_imports = [
                node
                for node in ast.walk(tree)
                if _imports_python_chess(node)
            ]

            self.assertEqual(
                chess_imports,
                [],
                f"{relative_path} imports python-chess directly",
            )

        self.assertGreaterEqual(len(checked_files), 1)


def _imports_python_chess(node: ast.AST) -> bool:
    if isinstance(node, ast.Import):
        return any(_is_python_chess_module(alias.name) for alias in node.names)
    if isinstance(node, ast.ImportFrom) and node.module is not None:
        return _is_python_chess_module(node.module)
    return False


def _is_python_chess_module(module_name: str) -> bool:
    return module_name == "chess" or module_name.startswith("chess.")


if __name__ == "__main__":
    unittest.main()
