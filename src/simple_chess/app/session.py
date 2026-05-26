"""Session layer for chess game coordination (M4-01, M4-04).

Defines the game session structure: mode (PvP or PvC), player types
(human or computer per side), and reference to the domain MatchState.

M4-04 extends the session with:
- AI turn detection (is_computer_turn).
- AI hook that accepts an external callable without own AI logic
  (request_ai_move).
- Game state snapshot for the future interface layer M5
  (game_state_snapshot).

The application layer does not implement chess rules — those belong to
the domain (``simple_chess.domain``).  It does not depend on Pygame —
that belongs to the interface layer (M5).

Example usage::

    from simple_chess.domain.match import MatchState
    from simple_chess.app.session import GameMode, GameSession, PlayerType

    match = MatchState()
    session = GameSession(mode=GameMode.PVC, match=match)
    session.current_player_type()   # PlayerType.HUMAN (white's turn)
    session.is_computer_turn()      # False (human starts)
    session.game_state_snapshot()   # {"turn": "white", "mode": "pvc", ...}
"""
from __future__ import annotations

from collections.abc import Callable
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

    def is_computer_turn(self) -> bool:
        """Return ``True`` if the current player is a computer (AI) player.

        Uses :meth:`current_player_type` and the session's player
        configuration.  Intended as the primary check in the AI hook
        before invoking an external AI callable.

        Returns:
            ``True`` when the side to move is :attr:`PlayerType.COMPUTER`,
            ``False`` otherwise (always ``False`` in PvP mode).
        """
        return self.current_player_type() == PlayerType.COMPUTER

    def request_ai_move(self, ai_fn: Callable[[list[str]], str]) -> str:
        """Request a move from an external AI function.

        Collects the current legal moves from the domain and passes them to
        the provided callable.  **No AI logic is implemented here** — the
        session only acts as the integration point.  The actual strategy
        belongs to the AI layer (M7).

        Args:
            ai_fn: A callable that receives a list of legal UCI move strings
                and returns a chosen UCI move string.  Any function with this
                signature is accepted, which keeps the session decoupled from
                any specific AI implementation.

        Returns:
            The UCI move string returned by *ai_fn*.
        """
        legal_moves = self._match.legal_move_ucis()
        return ai_fn(legal_moves)

    def game_state_snapshot(self) -> dict[str, object]:
        """Return a snapshot of the current game state as plain Python types.

        Provides the information needed by the future interface layer (M5)
        to render the game without accessing the domain directly.  All
        values use standard Python types — no types from ``python-chess``
        are included, in compliance with ADR-004.

        Returns:
            A ``dict`` with the following keys:

            - ``"turn"`` (``str``): ``"white"`` or ``"black"``.
            - ``"mode"`` (``str``): ``"pvp"`` or ``"pvc"``.
            - ``"is_game_over"`` (``bool``): whether the game has ended.
            - ``"is_check"`` (``bool``): whether the side to move is in check.
            - ``"outcome"`` (``str | None``): termination reason string, or
              ``None`` if the game is still in progress.
            - ``"legal_moves"`` (``list[str]``): UCI strings of legal moves
              for the current position; empty when the game is over.
            - ``"board"`` (``dict[str, str]``): mapping of occupied square
              names (``"a1"``–``"h8"``) to piece symbols (``"K"``,
              ``"k"``, etc.) as plain Python strings; empty squares are
              omitted.  Provided by the domain via :meth:`MatchState.board_map`
              without any ``python-chess`` types in compliance with ADR-004.
        """
        return {
            "turn": self._match.current_turn(),
            "mode": self._mode.value,
            "is_game_over": self._match.is_game_over(),
            "is_check": self._match.is_check(),
            "outcome": self._match.outcome(),
            "legal_moves": self._match.legal_move_ucis(),
            "board": self._match.board_map(),
        }
