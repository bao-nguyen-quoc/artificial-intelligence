import math
from typing import Any

from src.utils.game import Game, SearchResult, SearchStats


def minimax(game: Game, state: Any) -> SearchResult:
    stats = SearchStats()
    value, action = _minimax(game, state, stats)
    return SearchResult(value, action, stats.nodes)


def _minimax(game: Game, state: Any, stats: SearchStats) -> tuple[float, Any | None]:
    # Step 1: Count this node (stats.nodes += 1)
    stats.nodes += 1

    # Step 2: If state is terminal -> return (utility(state), None)
    if game.is_terminal(state):
        return game.utility(state), None

    best_action = None
    if game.to_move(state):
        # Step 3: If it is MAX's turn:
        #           best = -inf
        #           for each action: value of child = _minimax(child)
        #           keep the value (and action) if strictly greater than best
        best = -math.inf
        for action in game.actions(state):
            value, _ = _minimax(game, game.result(state, action), stats)
            if value > best:
                best, best_action = value, action
    else:
        # Step 4: Otherwise (MIN's turn): same, with +inf and strictly smaller
        best = math.inf
        for action in game.actions(state):
            value, _ = _minimax(game, game.result(state, action), stats)
            if value < best:
                best, best_action = value, action

    # Step 5: Return (best, best_action)
    return best, best_action


def minimax_depth_limited(
    game: Game, state: Any, depth: float = math.inf
) -> SearchResult:
    stats = SearchStats()
    value, action = _minimax_depth_limited(game, state, depth, stats)
    return SearchResult(value, action, stats.nodes)


def _minimax_depth_limited(
    game: Game, state: Any, depth: float, stats: SearchStats
) -> tuple[float, Any | None]:
    # Step 1: Count this node
    stats.nodes += 1

    # Step 2: If state is terminal -> return (utility(state), None)
    if game.is_terminal(state):
        return game.utility(state), None

    # Step 3: If depth == 0 -> return (evaluate(state), None)
    if depth == 0:
        return game.evaluate(state), None

    # Step 4: Same as traditional minimax, but recurse with depth - 1
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
    # alpha: best value MAX can already guarantee on the path from the root
    # beta : best value MIN can already guarantee on the path from the root
    #
    # Step 1: Count this node
    stats.nodes += 1

    # Step 2: If terminal -> (utility, None); if depth == 0 -> (evaluate, None)
    if game.is_terminal(state):
        return game.utility(state), None
    if depth == 0:
        return game.evaluate(state), None

    best_action = None
    if game.to_move(state):
        # Step 3: If MAX's turn:
        #           for each action:
        #               value of child = _alpha_beta(child, depth - 1, alpha, beta)
        #               if value > alpha: update alpha and best_action
        #               if alpha >= beta: break   (prune remaining children)
        #           return (alpha, best_action)
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
        # Step 4: If MIN's turn: symmetric, updating beta with `value < beta`
        #           return (beta, best_action)
        for action in game.actions(state):
            value, _ = _alpha_beta(
                game, game.result(state, action), depth - 1, alpha, beta, stats
            )
            if value < beta:
                beta, best_action = value, action
            if alpha >= beta:
                break
        return beta, best_action


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
    # The returned value is from the point of view of the player to move in `state`.
    #
    # Step 1: Count this node
    stats.nodes += 1

    # Step 2: sign = _sign(game, state)
    #         If terminal -> (sign * utility(state), None)
    #         If depth == 0 -> (sign * evaluate(state), None)
    sign = _sign(game, state)
    if game.is_terminal(state):
        return sign * game.utility(state), None
    if depth == 0:
        return sign * game.evaluate(state), None

    best_action = None
    # Step 3: for each action:
    #             value = -_negamax(child, depth - 1, -beta, -alpha)   (flip sign!)
    #             if value > alpha: update alpha and best_action
    #             if alpha >= beta: break
    for action in game.actions(state):
        value, _ = _negamax(
            game, game.result(state, action), depth - 1, -beta, -alpha, stats
        )
        value = -value
        if value > alpha:
            alpha, best_action = value, action
        if alpha >= beta:
            break

    # Step 4: return (alpha, best_action)
    return alpha, best_action
