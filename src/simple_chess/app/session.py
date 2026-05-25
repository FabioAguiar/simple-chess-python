"""Session layer for chess game coordination (M4-01).

Defines the game session structure: mode (PvP or PvC), player types
(human or computer per side), and reference to the domain MatchState.

The application layer does not implement chess rules — those belong to
the domain (``simple_chess.domain``).  It does not depend on Pygame —
that belongs to the interface layer (M5).

Example usage::

    from simple_chess.domain.match import MatchState
    from simple_chess.app.session import GameMode, GameSession, PlayerType

    match = MatchState()
    session = GameSession(mode=GameMode.PVP, match=match)
    session.current_player_type()   # PlayerType.HUMAN
    session.mode                    # GameMode.PVP
"""
from __future__ import annotations

from enum import Enum

from simple_chess.domain.match import MatchState


class GameMode(Enum):
    """Explicit representation of the chess game mode.

    Attributes:
        PVP: Player vs Player — both sides are human.
        PVC: Player vs Computer — white is human, black is the computer.
    """

    PVP = "pvp"
    PVC = "pvc"


class PlayerType(Enum):
    """Explicit representation of the type of player on each side.

    Attributes:
        HUMAN: A human player controlling this side.
        COMPUTER: An automated/AI player controlling this side.
    """

    HUMAN = "human"
    COMPUTER = "computer"


class GameSession:
    """Represents a chess game session.

    Coordinates game mode, player configuration per side, and the
    domain-level :class:`~simple_chess.domain.match.MatchState`.

    Responsibilities:
    - Hold the game mode (PvP or PvC).
    - Hold the player type for each side (human or computer).
    - Expose which player type is active for the current turn.
    - Reference the domain state without reimplementing chess rules.

    Non-responsibilities (explicit scope boundaries):
    - Does **not** implement chess rules — delegates to ``MatchState``.
    - Does **not** import or depend on Pygame.
    - Does **not** import ``python-chess`` (``chess``) directly.
    - Does **not** manage turn flow or AI calls (M4-02, M4-04).

    Args:
        mode: The game mode — :attr:`GameMode.PVP` or :attr:`GameMode.PVC`.
        match: The domain :class:`~simple_chess.domain.match.MatchState`,
            injected to allow replacement in tests without real domain state.

    In **PvP** mode both sides are assigned :attr:`PlayerType.HUMAN`.
    In **PvC** mode white is :attr:`PlayerType.HUMAN` and black is
    :attr:`PlayerType.COMPUTER`.
    """

    def __init__(self, mode: GameMode, match: MatchState) -> None:
        self._mode = mode
        self._match = match
        self._white_player = PlayerType.HUMAN
        self._black_player = (
            PlayerType.HUMAN if mode == GameMode.PVP else PlayerType.COMPUTER
        )

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def mode(self) -> GameMode:
        """The game mode for this session."""
        return self._mode

    @property
    def white_player(self) -> PlayerType:
        """The player type assigned to the white side."""
        return self._white_player

    @property
    def black_player(self) -> PlayerType:
        """The player type assigned to the black side."""
        return self._black_player

    @property
    def match(self) -> MatchState:
        """The domain match state associated with this session."""
        return self._match

    # ------------------------------------------------------------------
    # Coordination
    # ------------------------------------------------------------------

    def current_player_type(self) -> PlayerType:
        """Return the :class:`PlayerType` for the side currently to move.

        Combines the current turn reported by the domain with the session's
        player configuration.  Intended to be used by the turn coordinator
        (M4-02) to decide whether to await human input or trigger the AI.

        Returns:
            :attr:`PlayerType.HUMAN` or :attr:`PlayerType.COMPUTER` for
            whichever side holds the current turn.
        """
        return (
            self._white_player
            if self._match.current_turn() == "white"
            else self._black_player
        )
