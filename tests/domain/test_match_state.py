"""Domain behavior tests for the public chess match contract."""
from __future__ import annotations

import ast
from pathlib import Path
import unittest

import simple_chess.domain as domain
from simple_chess.domain import MatchState


class MatchStateInitialPositionTests(unittest.TestCase):
    def test_initial_match_state_exposes_standard_starting_position(self) -> None:
        match = MatchState()

        legal_moves = match.legal_move_ucis()

        self.assertEqual(match.current_turn(), "white")
        self.assertFalse(match.is_game_over())
        self.assertFalse(match.is_check())
        self.assertIsNone(match.outcome())
        self.assertEqual(len(legal_moves), 20)
        self.assertIn("e2e4", legal_moves)
        self.assertIn("g1f3", legal_moves)
        self.assertIn("b1c3", legal_moves)


class MatchStateMoveValidationTests(unittest.TestCase):
    def test_is_legal_move_reports_legal_illegal_and_malformed_moves(self) -> None:
        match = MatchState()
        turn_before = match.current_turn()
        legal_moves_before = match.legal_move_ucis()

        self.assertTrue(match.is_legal_move("e2e4"))
        self.assertFalse(match.is_legal_move("e2e5"))
        self.assertFalse(match.is_legal_move("not-a-move"))

        self.assertEqual(match.current_turn(), turn_before)
        self.assertEqual(match.legal_move_ucis(), legal_moves_before)

    def test_push_uci_applies_legal_move_and_updates_turn(self) -> None:
        match = MatchState()

        match.push_uci("e2e4")

        self.assertEqual(match.current_turn(), "black")
        self.assertIn("e7e5", match.legal_move_ucis())
        self.assertFalse(match.is_legal_move("e2e4"))

    def test_push_uci_rejects_illegal_move_without_changing_state(self) -> None:
        match = MatchState()
        turn_before = match.current_turn()
        legal_moves_before = match.legal_move_ucis()

        with self.assertRaisesRegex(ValueError, "Illegal move in current position"):
            match.push_uci("e2e5")

        self.assertEqual(match.current_turn(), turn_before)
        self.assertEqual(match.legal_move_ucis(), legal_moves_before)

    def test_push_uci_rejects_malformed_move_without_changing_state(self) -> None:
        match = MatchState()
        turn_before = match.current_turn()
        legal_moves_before = match.legal_move_ucis()

        with self.assertRaisesRegex(ValueError, "Invalid UCI string"):
            match.push_uci("not-a-move")

        self.assertEqual(match.current_turn(), turn_before)
        self.assertEqual(match.legal_move_ucis(), legal_moves_before)


class DomainBoundaryTests(unittest.TestCase):
    def test_domain_public_contract_does_not_expose_python_chess(self) -> None:
        self.assertEqual(domain.__all__, ["MatchState"])
        self.assertIs(domain.MatchState, MatchState)
        self.assertFalse(hasattr(domain, "chess"))

    def test_domain_does_not_import_pygame(self) -> None:
        domain_root = _project_root() / "src" / "simple_chess" / "domain"
        checked_files: list[Path] = []

        for path in domain_root.rglob("*.py"):
            if "__pycache__" in path.parts:
                continue

            checked_files.append(path.relative_to(domain_root))
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            pygame_imports = [
                node for node in ast.walk(tree) if _imports_module(node, "pygame")
            ]

            self.assertEqual(
                pygame_imports,
                [],
                f"{path.relative_to(_project_root())} imports Pygame directly",
            )

        self.assertGreaterEqual(len(checked_files), 1)


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


if __name__ == "__main__":
    unittest.main()
