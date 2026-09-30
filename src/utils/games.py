from typing import Any

from src.utils.game import Game


class ExplicitTreeGame(Game):
    """
    A game whose tree is given explicitly as nested lists.
    Leaves are numbers, internal nodes are lists of children.

        tree = [[3, 5], [2, 9]]

              MAX
             /    \\
          MIN      MIN
          / \\      / \\
         3   5    2   9

    State = (subtree, is_max). Action = index of the child.
    `evaluate` (used when depth runs out) = average of all leaves below the node.
    """

    def __init__(self, tree: list, max_first: bool = True):
        self.tree = tree
        self.max_first = max_first

    def initial_state(self) -> Any:
        return (self.tree, self.max_first)

    def to_move(self, state: Any) -> bool:
        return state[1]

    def actions(self, state: Any) -> list:
        return list(range(len(state[0])))

    def result(self, state: Any, action: Any) -> Any:
        node, is_max = state
        return (node[action], not is_max)

    def is_terminal(self, state: Any) -> bool:
        return not isinstance(state[0], list)

    def utility(self, state: Any) -> float:
        return float(state[0])

    def evaluate(self, state: Any) -> float:
        leaves = self._leaves(state[0])
        return sum(leaves) / len(leaves)

    def _leaves(self, node: Any) -> list:
        if not isinstance(node, list):
            return [float(node)]
        return [x for child in node for x in self._leaves(child)]


_LINES = [
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
]


class TicTacToe(Game):
    """
    Tic-tac-toe. X = MAX (moves first), O = MIN.
    State = tuple of 9 cells: " ", "X" or "O" (index 0..8, row by row).
    Action = index of an empty cell.
    utility: +1 if X wins, -1 if O wins, 0 for a draw.
    evaluate: (#lines still open for X) - (#lines still open for O).
    """

    def initial_state(self) -> Any:
        return (" ",) * 9

    def to_move(self, state: Any) -> bool:
        return state.count("X") == state.count("O")

    def actions(self, state: Any) -> list:
        return [i for i, cell in enumerate(state) if cell == " "]

    def result(self, state: Any, action: Any) -> Any:
        mark = "X" if self.to_move(state) else "O"
        board = list(state)
        board[action] = mark
        return tuple(board)

    def winner(self, state: Any) -> str | None:
        for a, b, c in _LINES:
            if state[a] != " " and state[a] == state[b] == state[c]:
                return state[a]
        return None

    def is_terminal(self, state: Any) -> bool:
        return self.winner(state) is not None or " " not in state

    def utility(self, state: Any) -> float:
        w = self.winner(state)
        return 1.0 if w == "X" else -1.0 if w == "O" else 0.0

    def evaluate(self, state: Any) -> float:
        x_open = sum(1 for line in _LINES if all(state[i] != "O" for i in line))
        o_open = sum(1 for line in _LINES if all(state[i] != "X" for i in line))
        return float(x_open - o_open)
