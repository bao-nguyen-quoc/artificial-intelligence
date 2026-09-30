import math
from typing import Any

from src.utils.game import Game, SearchResult, SearchStats


# ---------------------------------------------------------------------------
# Task 1: Pure Minimax
# ---------------------------------------------------------------------------
def minimax(game: Game, state: Any) -> SearchResult:
    stats = SearchStats()
    value, action = _minimax(game, state, stats)
    return SearchResult(value, action, stats.nodes)


def _minimax(game: Game, state: Any, stats: SearchStats) -> tuple[float, Any | None]:
    stats.nodes += 1
    if game.is_terminal(state):
        return game.utility(state), None

    best_action = None
    if game.to_move(state):
        best = -math.inf
        for action in game.actions(state):
            value, _ = _minimax(game, game.result(state, action), stats)
            if value > best:
                best, best_action = value, action
    else:
        best = math.inf
        for action in game.actions(state):
            value, _ = _minimax(game, game.result(state, action), stats)
            if value < best:
                best, best_action = value, action
    return best, best_action


# ---------------------------------------------------------------------------
# Task 2: Depth-limited Minimax
# ---------------------------------------------------------------------------
def minimax_depth_limited(
    game: Game, state: Any, depth: float = math.inf
) -> SearchResult:
    stats = SearchStats()
    value, action = _minimax_depth_limited(game, state, depth, stats)
    return SearchResult(value, action, stats.nodes)


def _minimax_depth_limited(
    game: Game, state: Any, depth: float, stats: SearchStats
) -> tuple[float, Any | None]:
    stats.nodes += 1
    if game.is_terminal(state):
        return game.utility(state), None
    if depth == 0:
        return game.evaluate(state), None

    best_action = None
    if game.to_move(state):
        best = -math.inf
        for action in game.actions(state):
            value, _ = _minimax_depth_limited(
                game, game.result(state, action), depth - 1, stats
            )
            if value > best:
                best, best_action = value, action
    else:
        best = math.inf
        for action in game.actions(state):
            value, _ = _minimax_depth_limited(
                game, game.result(state, action), depth - 1, stats
            )
            if value < best:
                best, best_action = value, action
    return best, best_action


# ---------------------------------------------------------------------------
# Task 3: Minimax with Alpha-Beta pruning
# ---------------------------------------------------------------------------
def minimax_alpha_beta(game: Game, state: Any, depth: float = math.inf) -> SearchResult:
    stats = SearchStats()
    value, action = _alpha_beta(game, state, depth, -math.inf, math.inf, stats)
    return SearchResult(value, action, stats.nodes)


def _alpha_beta(
    game: Game,
    state: Any,
    depth: float,
    alpha: float,
    beta: float,
    stats: SearchStats,
) -> tuple[float, Any | None]:
    stats.nodes += 1
    if game.is_terminal(state):
        return game.utility(state), None
    if depth == 0:
        return game.evaluate(state), None

    best_action = None
    if game.to_move(state):
        for action in game.actions(state):
            value, _ = _alpha_beta(
                game, game.result(state, action), depth - 1, alpha, beta, stats
            )
            if value > alpha:
                alpha, best_action = value, action
            if alpha >= beta:
                break
        return alpha, best_action
    else:
        for action in game.actions(state):
            value, _ = _alpha_beta(
                game, game.result(state, action), depth - 1, alpha, beta, stats
            )
            if value < beta:
                beta, best_action = value, action
            if alpha >= beta:
                break
        return beta, best_action


# ---------------------------------------------------------------------------
# Task 4: Minimax with Alpha-Beta pruning (negamax style)
# ---------------------------------------------------------------------------
def _sign(game: Game, state: Any) -> int:
    return 1 if game.to_move(state) else -1


def minimax_negamax_alpha_beta(
    game: Game, state: Any, depth: float = math.inf
) -> SearchResult:
    stats = SearchStats()
    value, action = _negamax(game, state, depth, -math.inf, math.inf, stats)
    return SearchResult(_sign(game, state) * value, action, stats.nodes)


def _negamax(
    game: Game,
    state: Any,
    depth: float,
    alpha: float,
    beta: float,
    stats: SearchStats,
) -> tuple[float, Any | None]:
    stats.nodes += 1
    sign = _sign(game, state)
    if game.is_terminal(state):
        return sign * game.utility(state), None
    if depth == 0:
        return sign * game.evaluate(state), None

    best_action = None
    for action in game.actions(state):
        value, _ = _negamax(
            game, game.result(state, action), depth - 1, -beta, -alpha, stats
        )
        value = -value
        if value > alpha:
            alpha, best_action = value, action
        if alpha >= beta:
            break
    return alpha, best_action
