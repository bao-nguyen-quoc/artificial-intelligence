import math

from src.game_tree_search.minimax import (
    minimax,
    minimax_alpha_beta,
    minimax_depth_limited,
    minimax_negamax_alpha_beta,
)
from src.utils.games import ExplicitTreeGame, TicTacToe

# ──────────────────────────────────────────────────────────────────────
# Shared fixture trees
# ──────────────────────────────────────────────────────────────────────
#
#         MAX  (expected value = 3)
#        /    \
#     MIN      MIN
#     / \      / \
#    3   5    2   9
#
TREE_NOTEBOOK = [[3, 5], [2, 9]]

#         MAX  (expected value = 6)
#      /   |   \
#   MIN   MIN   MIN
#   /\    /\    /\
#  4  6  7  3  8  1
#
TREE_THREE_BRANCHES = [[4, 6], [7, 3], [8, 1]]

#  Single leaf (edge case)
TREE_SINGLE = 42


# ══════════════════════════════════════════════════════════════════════
# Task 1: Pure Minimax
# ══════════════════════════════════════════════════════════════════════
class TestMinimax:
    """Tests for pure minimax (no depth limit)."""

    def test_notebook_tree(self):
        """Classic 2-level tree from notebook: MAX picks branch with value 3."""
        game = ExplicitTreeGame(TREE_NOTEBOOK)
        result = minimax(game, game.initial_state())

        assert result.value == 3.0
        assert result.action == 0  # left branch (MIN=3) beats right (MIN=2)

    def test_three_branches(self):
        """Three-branch tree: MAX picks best MIN value."""
        game = ExplicitTreeGame(TREE_THREE_BRANCHES)
        result = minimax(game, game.initial_state())

        # MIN values: [4, 3, 1] → MAX picks 4 (branch 0)
        assert result.value == 4.0
        assert result.action == 0

    def test_single_leaf(self):
        """Terminal root returns its value and no action."""
        game = ExplicitTreeGame(TREE_SINGLE)
        result = minimax(game, game.initial_state())

        assert result.value == 42.0
        assert result.action is None

    def test_min_first(self):
        """MIN moves first: MIN picks the smallest MAX child."""
        game = ExplicitTreeGame(TREE_NOTEBOOK, max_first=False)
        result = minimax(game, game.initial_state())

        # MAX values per child: max(3,5)=5 and max(2,9)=9
        # MIN at root picks min(5, 9) = 5 → action 0
        assert result.value == 5.0
        assert result.action == 0

    def test_nodes_counted(self):
        """Every node (internal + leaf) increments the counter."""
        game = ExplicitTreeGame(TREE_NOTEBOOK)
        result = minimax(game, game.initial_state())

        # 1 root + 2 internal + 4 leaves = 7
        assert result.nodes_expanded == 7

    def test_symmetric_tree(self):
        """Symmetric tree: both branches have same minimax value."""
        tree = [[5, 3], [5, 3]]
        game = ExplicitTreeGame(tree)
        result = minimax(game, game.initial_state())

        # MIN values: [3, 3] → MAX picks 3 (first branch, action 0)
        assert result.value == 3.0
        assert result.action == 0

    def test_deep_tree(self):
        """Deeper tree (3 levels of decisions)."""
        tree = [[[1, 2], [3, 4]], [[5, 6], [7, 8]]]
        game = ExplicitTreeGame(tree)
        result = minimax(game, game.initial_state())

        # Level 3 (MAX): [max(1,2)=2, max(3,4)=4] and [max(5,6)=6, max(7,8)=8]
        # Level 2 (MIN): [min(2,4)=2] and [min(6,8)=6]
        # Level 1 (MAX): max(2, 6) = 6 → action 1
        assert result.value == 6.0
        assert result.action == 1


# ══════════════════════════════════════════════════════════════════════
# Task 2: Depth-limited Minimax
# ══════════════════════════════════════════════════════════════════════
class TestMinimaxDepthLimited:
    """Tests for minimax with a depth cutoff."""

    def test_infinite_depth_matches_pure(self):
        """depth=inf behaves identically to pure minimax."""
        game = ExplicitTreeGame(TREE_NOTEBOOK)
        state = game.initial_state()

        pure = minimax(game, state)
        limited = minimax_depth_limited(game, state, math.inf)

        assert limited.value == pure.value
        assert limited.action == pure.action

    def test_depth_zero_uses_evaluate(self):
        """depth=0 calls evaluate() on the root without expanding children."""
        game = ExplicitTreeGame(TREE_NOTEBOOK)
        result = minimax_depth_limited(game, game.initial_state(), depth=0)

        # evaluate = average of all leaves = (3+5+2+9)/4 = 4.75
        assert result.value == 4.75
        assert result.action is None
        assert result.nodes_expanded == 1

    def test_depth_one_evaluates_children(self):
        """depth=1 expands root, evaluates children with evaluate()."""
        game = ExplicitTreeGame(TREE_NOTEBOOK)
        result = minimax_depth_limited(game, game.initial_state(), depth=1)

        # Children evaluated: left avg=(3+5)/2=4.0, right avg=(2+9)/2=5.5
        # MAX at root picks max(4.0, 5.5) = 5.5 → action 1
        assert result.value == 5.5
        assert result.action == 1

    def test_depth_two_reaches_leaves(self):
        """depth=2 reaches all leaves → matches pure minimax."""
        game = ExplicitTreeGame(TREE_NOTEBOOK)
        result = minimax_depth_limited(game, game.initial_state(), depth=2)

        assert result.value == 3.0
        assert result.action == 0

    def test_terminal_ignores_depth(self):
        """A terminal state returns utility regardless of remaining depth."""
        game = ExplicitTreeGame(TREE_SINGLE)
        result = minimax_depth_limited(game, game.initial_state(), depth=5)

        assert result.value == 42.0
        assert result.action is None

    def test_fewer_nodes_at_lower_depth(self):
        """Lower depth should expand fewer nodes."""
        game = ExplicitTreeGame(TREE_NOTEBOOK)
        state = game.initial_state()

        r0 = minimax_depth_limited(game, state, depth=0)
        r1 = minimax_depth_limited(game, state, depth=1)
        r2 = minimax_depth_limited(game, state, depth=2)

        assert r0.nodes_expanded < r1.nodes_expanded < r2.nodes_expanded


# ══════════════════════════════════════════════════════════════════════
# Task 3: Minimax with Alpha-Beta pruning
# ══════════════════════════════════════════════════════════════════════
class TestMinimaxAlphaBeta:
    """Tests for alpha-beta pruning."""

    def test_same_value_as_pure(self):
        """Alpha-beta must return the same minimax value as pure minimax."""
        game = ExplicitTreeGame(TREE_NOTEBOOK)
        state = game.initial_state()

        pure = minimax(game, state)
        ab = minimax_alpha_beta(game, state)

        assert ab.value == pure.value
        assert ab.action == pure.action

    def test_prunes_nodes(self):
        """Alpha-beta should visit fewer (or equal) nodes than pure minimax."""
        game = ExplicitTreeGame(TREE_NOTEBOOK)
        state = game.initial_state()

        pure = minimax(game, state)
        ab = minimax_alpha_beta(game, state)

        assert ab.nodes_expanded <= pure.nodes_expanded

    def test_depth_limited(self):
        """Alpha-beta with depth limit returns same value as depth-limited minimax."""
        game = ExplicitTreeGame(TREE_THREE_BRANCHES)
        state = game.initial_state()

        dl = minimax_depth_limited(game, state, depth=1)
        ab = minimax_alpha_beta(game, state, depth=1)

        assert ab.value == dl.value
        assert ab.action == dl.action

    def test_three_branches_correctness(self):
        """Three-branch tree: alpha-beta returns correct minimax value."""
        game = ExplicitTreeGame(TREE_THREE_BRANCHES)
        result = minimax_alpha_beta(game, game.initial_state())

        assert result.value == 4.0
        assert result.action == 0

    def test_prunes_more_on_larger_tree(self):
        """On a wider tree, alpha-beta should prune significantly."""
        tree = [[3, 12, 8], [2, 4, 6], [14, 5, 2]]
        game = ExplicitTreeGame(tree)
        state = game.initial_state()

        pure = minimax(game, state)
        ab = minimax_alpha_beta(game, state)

        assert ab.value == pure.value
        assert ab.nodes_expanded <= pure.nodes_expanded

    def test_single_leaf(self):
        """Terminal root: alpha-beta returns value, no action."""
        game = ExplicitTreeGame(TREE_SINGLE)
        result = minimax_alpha_beta(game, game.initial_state())

        assert result.value == 42.0
        assert result.action is None


# ══════════════════════════════════════════════════════════════════════
# Task 4: Negamax with Alpha-Beta pruning
# ══════════════════════════════════════════════════════════════════════
class TestNegamaxAlphaBeta:
    """Tests for the negamax variant of alpha-beta."""

    def test_same_value_as_standard_ab(self):
        """Negamax must produce the same result as standard alpha-beta."""
        game = ExplicitTreeGame(TREE_NOTEBOOK)
        state = game.initial_state()

        ab = minimax_alpha_beta(game, state)
        neg = minimax_negamax_alpha_beta(game, state)

        assert neg.value == ab.value
        assert neg.action == ab.action

    def test_three_branches(self):
        """Three-branch tree correctness."""
        game = ExplicitTreeGame(TREE_THREE_BRANCHES)
        state = game.initial_state()

        ab = minimax_alpha_beta(game, state)
        neg = minimax_negamax_alpha_beta(game, state)

        assert neg.value == ab.value
        assert neg.action == ab.action

    def test_depth_limited(self):
        """Negamax with depth limit matches depth-limited minimax."""
        game = ExplicitTreeGame(TREE_NOTEBOOK)
        state = game.initial_state()

        dl = minimax_depth_limited(game, state, depth=1)
        neg = minimax_negamax_alpha_beta(game, state, depth=1)

        assert neg.value == dl.value
        assert neg.action == dl.action

    def test_single_leaf(self):
        """Terminal root: negamax returns value, no action."""
        game = ExplicitTreeGame(TREE_SINGLE)
        result = minimax_negamax_alpha_beta(game, game.initial_state())

        assert result.value == 42.0
        assert result.action is None

    def test_min_first(self):
        """MIN moves first: negamax agrees with standard alpha-beta."""
        game = ExplicitTreeGame(TREE_NOTEBOOK, max_first=False)
        state = game.initial_state()

        ab = minimax_alpha_beta(game, state)
        neg = minimax_negamax_alpha_beta(game, state)

        assert neg.value == ab.value
        assert neg.action == ab.action

    def test_deep_tree(self):
        """Deeper tree: negamax matches standard alpha-beta."""
        tree = [[[1, 2], [3, 4]], [[5, 6], [7, 8]]]
        game = ExplicitTreeGame(tree)
        state = game.initial_state()

        ab = minimax_alpha_beta(game, state)
        neg = minimax_negamax_alpha_beta(game, state)

        assert neg.value == ab.value
        assert neg.action == ab.action


# ══════════════════════════════════════════════════════════════════════
# Cross-variant: TicTacToe integration
# ══════════════════════════════════════════════════════════════════════
class TestTicTacToeIntegration:
    """All four variants must agree on TicTacToe positions."""

    def test_all_variants_agree_on_initial(self):
        """From the initial (empty) board, all four return the same value/action."""
        game = TicTacToe()
        state = game.initial_state()
        depth = 3  # shallow for speed

        dl = minimax_depth_limited(game, state, depth)
        ab = minimax_alpha_beta(game, state, depth)
        neg = minimax_negamax_alpha_beta(game, state, depth)

        assert dl.value == ab.value == neg.value
        assert dl.action == ab.action == neg.action

    def test_x_wins_forced(self):
        """X to move with a winning line available picks the winning cell."""
        # X X _
        # O O _
        # _ _ _
        board = ("X", "X", " ", "O", "O", " ", " ", " ", " ")
        game = TicTacToe()

        result = minimax_alpha_beta(game, board, depth=2)
        assert result.action == 2  # completes top row
        assert result.value >= 1.0  # X wins

    def test_o_blocks_forced(self):
        """O to move must block X's winning threat."""
        # X X _
        # O _ _
        # _ _ _
        board = ("X", "X", " ", "O", " ", " ", " ", " ", " ")
        game = TicTacToe()

        # It's O's turn (count X=2, O=1 → X's turn, so add one more O)
        # Actually X=2, O=1 → to_move = (2==1) = False → it's O's turn? No.
        # to_move: state.count("X") == state.count("O") → 2 == 1 → False → MIN's turn
        result = minimax_alpha_beta(game, board, depth=4)
        assert result.action == 2  # block top row

    def test_terminal_utility(self):
        """A terminal board returns correct utility."""
        # X X X
        # O O _
        # _ _ _
        board = ("X", "X", "X", "O", "O", " ", " ", " ", " ")
        game = TicTacToe()

        result = minimax(game, board)
        assert result.value == 1.0  # X wins
        assert result.action is None

    def test_draw_value(self):
        """A drawn board returns utility 0."""
        # X O X
        # X O O
        # O X X
        board = ("X", "O", "X", "X", "O", "O", "O", "X", "X")
        game = TicTacToe()

        result = minimax(game, board)
        assert result.value == 0.0
        assert result.action is None
