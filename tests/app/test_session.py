"""Tests for GameSession initialization and basic configuration (M4-01).

Covers the acceptance criteria of issue M4-05 for GameSession:

- Session can be created with PvP and PvC modes.
- In PvP mode, both sides are assigned PlayerType.HUMAN.
- In PvC mode, white is HUMAN and black is COMPUTER.
- current_player_type() returns the correct PlayerType for the current turn.
- Properties mode, white_player, black_player, and match are accessible.
- session.py does not import python-chess directly (ADR-004).

Note: is_computer_turn(), request_ai_move(), and game_state_snapshot() are
covered by test_session_ai_hook.py (M4-04). This file does not duplicate them.
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
def pvp_match() -> MatchState:
    """Standard starting position MatchState."""
    return MatchState()


@pytest.fixture()
def pvp_session(pvp_match: MatchState) -> GameSession:
    """PvP session at the standard starting position."""
    return GameSession(mode=GameMode.PVP, match=pvp_match)


@pytest.fixture()
def pvc_session() -> GameSession:
    """PvC session at the standard starting position."""
    return GameSession(mode=GameMode.PVC, match=MatchState())


# ---------------------------------------------------------------------------
# Mode property
# ---------------------------------------------------------------------------


class TestSessionMode:
    def test_pvp_session_has_pvp_mode(self, pvp_session: GameSession) -> None:
        assert pvp_session.mode == GameMode.PVP

    def test_pvc_session_has_pvc_mode(self, pvc_session: GameSession) -> None:
        assert pvc_session.mode == GameMode.PVC


# ---------------------------------------------------------------------------
# Player type assignment — PvP
# ---------------------------------------------------------------------------


class TestPlayerTypePvP:
    def test_pvp_white_player_is_human(self, pvp_session: GameSession) -> None:
        assert pvp_session.white_player == PlayerType.HUMAN

    def test_pvp_black_player_is_human(self, pvp_session: GameSession) -> None:
        assert pvp_session.black_player == PlayerType.HUMAN


# ---------------------------------------------------------------------------
# Player type assignment — PvC
# ---------------------------------------------------------------------------


class TestPlayerTypePvC:
    def test_pvc_white_player_is_human(self, pvc_session: GameSession) -> None:
        assert pvc_session.white_player == PlayerType.HUMAN

    def test_pvc_black_player_is_computer(self, pvc_session: GameSession) -> None:
        assert pvc_session.black_player == PlayerType.COMPUTER


# ---------------------------------------------------------------------------
# current_player_type — PvP
# ---------------------------------------------------------------------------


class TestCurrentPlayerTypePvP:
    def test_pvp_current_player_type_at_start_is_human(
        self, pvp_session: GameSession
    ) -> None:
        """At the start of a PvP game, white (HUMAN) plays first."""
        assert pvp_session.current_player_type() == PlayerType.HUMAN

    def test_pvp_current_player_type_after_white_move_is_human(self) -> None:
        """After white moves, black (HUMAN) plays — still HUMAN in PvP."""
        match = MatchState()
        match.push_uci("e2e4")
        session = GameSession(mode=GameMode.PVP, match=match)
        assert session.current_player_type() == PlayerType.HUMAN


# ---------------------------------------------------------------------------
# current_player_type — PvC
# ---------------------------------------------------------------------------


class TestCurrentPlayerTypePvC:
    def test_pvc_current_player_type_at_start_is_human(
        self, pvc_session: GameSession
    ) -> None:
        """At the start of a PvC game, white (HUMAN) plays first."""
        assert pvc_session.current_player_type() == PlayerType.HUMAN

    def test_pvc_current_player_type_after_white_move_is_computer(self) -> None:
        """After white moves, it is black's turn — COMPUTER in PvC."""
        match = MatchState()
        match.push_uci("e2e4")
        session = GameSession(mode=GameMode.PVC, match=match)
        assert session.current_player_type() == PlayerType.COMPUTER


# ---------------------------------------------------------------------------
# match property
# ---------------------------------------------------------------------------


class TestMatchProperty:
    def test_match_property_returns_injected_match(
        self, pvp_match: MatchState, pvp_session: GameSession
    ) -> None:
        assert pvp_session.match is pvp_match


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
