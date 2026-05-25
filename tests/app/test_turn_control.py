"""Tests for TurnController (M4-02).

Covers the acceptance criteria of issue M4-05 for TurnController:

- current_side() returns "white" at the start of the game.
- current_side() returns "black" after white's first move.
- current_player_type() returns the correct PlayerType in PvP and PvC modes.
- receive_move_intent(uci) stores the UCI string as pending_intent.
- pending_intent is None before any intent is received.
- pending_intent holds the UCI string after receive_move_intent().
- clear_intent() resets pending_intent to None.
- TurnController does not import python-chess directly (ADR-004).
"""
from __future__ import annotations

import importlib
import sys

import pytest

from simple_chess.app.session import GameMode, GameSession, PlayerType
from simple_chess.app.turn_controller import TurnController
from simple_chess.domain.match import MatchState


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def pvp_controller() -> TurnController:
    """TurnController for a PvP session at the starting position."""
    match = MatchState()
    session = GameSession(mode=GameMode.PVP, match=match)
    return TurnController(session=session)


@pytest.fixture()
def pvc_controller() -> TurnController:
    """TurnController for a PvC session at the starting position."""
    match = MatchState()
    session = GameSession(mode=GameMode.PVC, match=match)
    return TurnController(session=session)


# ---------------------------------------------------------------------------
# current_side
# ---------------------------------------------------------------------------


class TestCurrentSide:
    def test_current_side_is_white_at_start(
        self, pvp_controller: TurnController
    ) -> None:
        assert pvp_controller.current_side() == "white"

    def test_current_side_is_black_after_white_move(self) -> None:
        """After white plays e2e4, it is black's turn."""
        match = MatchState()
        match.push_uci("e2e4")
        session = GameSession(mode=GameMode.PVP, match=match)
        controller = TurnController(session=session)
        assert controller.current_side() == "black"


# ---------------------------------------------------------------------------
# current_player_type — PvP
# ---------------------------------------------------------------------------


class TestCurrentPlayerTypePvP:
    def test_pvp_white_turn_is_human(
        self, pvp_controller: TurnController
    ) -> None:
        assert pvp_controller.current_player_type() == PlayerType.HUMAN

    def test_pvp_black_turn_is_human(self) -> None:
        """After white moves in PvP, black (HUMAN) is next."""
        match = MatchState()
        match.push_uci("e2e4")
        session = GameSession(mode=GameMode.PVP, match=match)
        controller = TurnController(session=session)
        assert controller.current_player_type() == PlayerType.HUMAN


# ---------------------------------------------------------------------------
# current_player_type — PvC
# ---------------------------------------------------------------------------


class TestCurrentPlayerTypePvC:
    def test_pvc_white_turn_is_human(
        self, pvc_controller: TurnController
    ) -> None:
        """At the start of a PvC game, white (HUMAN) plays first."""
        assert pvc_controller.current_player_type() == PlayerType.HUMAN

    def test_pvc_black_turn_is_computer(self) -> None:
        """After white moves in PvC, black (COMPUTER) is next."""
        match = MatchState()
        match.push_uci("e2e4")
        session = GameSession(mode=GameMode.PVC, match=match)
        controller = TurnController(session=session)
        assert controller.current_player_type() == PlayerType.COMPUTER


# ---------------------------------------------------------------------------
# receive_move_intent and pending_intent
# ---------------------------------------------------------------------------


class TestMoveIntent:
    def test_pending_intent_is_none_initially(
        self, pvp_controller: TurnController
    ) -> None:
        assert pvp_controller.pending_intent is None

    def test_receive_move_intent_stores_uci(
        self, pvp_controller: TurnController
    ) -> None:
        pvp_controller.receive_move_intent("e2e4")
        assert pvp_controller.pending_intent == "e2e4"

    def test_receive_move_intent_overwrites_previous(
        self, pvp_controller: TurnController
    ) -> None:
        pvp_controller.receive_move_intent("e2e4")
        pvp_controller.receive_move_intent("d2d4")
        assert pvp_controller.pending_intent == "d2d4"

    def test_clear_intent_resets_to_none(
        self, pvp_controller: TurnController
    ) -> None:
        pvp_controller.receive_move_intent("e2e4")
        pvp_controller.clear_intent()
        assert pvp_controller.pending_intent is None

    def test_clear_intent_on_none_is_safe(
        self, pvp_controller: TurnController
    ) -> None:
        """clear_intent() on an already-None intent must not raise."""
        pvp_controller.clear_intent()
        assert pvp_controller.pending_intent is None


# ---------------------------------------------------------------------------
# ADR-004: no direct python-chess import in turn_controller
# ---------------------------------------------------------------------------


class TestNoPythonChessDirectImport:
    def test_turn_controller_module_does_not_expose_chess(self) -> None:
        """Verify turn_controller.py does not import python-chess directly (ADR-004)."""
        module_name = "simple_chess.app.turn_controller"
        mod = sys.modules.get(module_name) or importlib.import_module(module_name)
        assert not hasattr(mod, "chess"), (
            "turn_controller must not import python-chess directly (ADR-004)"
        )
