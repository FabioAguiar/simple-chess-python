"""Tests for match state move application and rejection."""
from __future__ import annotations

import unittest

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


if __name__ == "__main__":
    unittest.main()
