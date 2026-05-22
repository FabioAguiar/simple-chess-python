"""Domain layer for chess rules and game state.

Public contract
---------------
External layers (application, AI, interface) must import from this package,
not from internal submodules.  No ``chess`` library type is re-exported here;
only domain-defined names are part of the public interface.

Example::

    from simple_chess.domain import MatchState

    match = MatchState()
    match.current_turn()          # "white"
    match.is_game_over()          # False
    match.legal_move_ucis()       # ["a2a3", ..., "h2h4"]
    match.is_legal_move("e2e4")   # True  (check-only, board unchanged)
    match.is_legal_move("e2e5")   # False (illegal; board unchanged)
    match.push_uci("e2e4")
    match.current_turn()          # "black"
"""

from simple_chess.domain.match import MatchState

__all__ = ["MatchState"]

