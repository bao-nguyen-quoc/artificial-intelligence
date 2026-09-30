from src.informed_search.greedy_best_first_search import greedy_best_first_search
from src.utils.graph import Graph


def zero_heuristic(state, goal) -> float:
    """Always returns 0 — makes Greedy Best-First Search behave like BFS."""
    return 0.0


def simple_heuristic(state, goal) -> float:
    """Simple heuristic: absolute difference between numeric states and goal."""
    return abs(state - goal)


def letter_heuristic(state, goal) -> float:
    """Heuristic for letter-based nodes: distance in alphabet order."""
    return abs(ord(state) - ord(goal))


class TestGreedyBestFirstSearchBasic:
    """Basic Greedy Best-First Search functionality tests."""

    def test_direct_connection(self):
        """Finds a goal that is a direct neighbor of start."""
        graph = Graph()
        graph.add_edge("A", "B")
        result = greedy_best_first_search(graph, "A", "B", h=letter_heuristic)

        assert result is not None
        assert result.state == "B"

    def test_start_is_goal(self):
        """Returns immediately when start equals goal."""
        graph = Graph()
        graph.add_edge("A", "B")
        result = greedy_best_first_search(graph, "A", "A", h=letter_heuristic)

        assert result is not None
        assert result.state == "A"
        assert result.parent is None

    def test_goal_not_reachable(self):
        """Returns None when the goal is unreachable."""
        graph = Graph()
        graph.add_edge("A", "B")
        graph.add_edge("C", "D")
        result = greedy_best_first_search(graph, "A", "D", h=letter_heuristic)

        assert result is None

    def test_goal_not_in_graph(self):
        """Returns None when goal node does not exist in the graph."""
        graph = Graph()
        graph.add_edge("A", "B")
        result = greedy_best_first_search(graph, "A", "Z", h=letter_heuristic)

        assert result is None


class TestGreedyBestFirstSearchHeuristicGuided:
    """Tests that Greedy Best-First Search is guided by the heuristic h(n)."""

    def test_heuristic_guides_expansion(self):
        """Expands toward the node with lowest h(n)."""
        #  A -> B (h=10)
        #  A -> C (h=1) -> D (goal, h=0)
        graph = Graph(directed=True)
        graph.add_edge("A", "B")
        graph.add_edge("A", "C")
        graph.add_edge("C", "D")
        graph.add_edge("B", "D")

        heuristic_values = {"A": 5, "B": 10, "C": 1, "D": 0}
        h = lambda state, goal: heuristic_values.get(state, float("inf"))

        result = greedy_best_first_search(graph, "A", "D", h=h)

        assert result is not None
        path_states = [node.state for node in result.get_path()]
        # Expands C first (h=1) before B (h=10), so path is A->C->D
        assert path_states == ["A", "C", "D"]

    def test_with_zero_heuristic_finds_goal(self):
        """With h=0 everywhere, still finds the goal."""
        graph = Graph()
        graph.add_edge("A", "B")
        graph.add_edge("B", "C")
        result = greedy_best_first_search(graph, "A", "C", h=zero_heuristic)

        assert result is not None
        assert result.state == "C"

    def test_greedy_may_not_find_optimal_path(self):
        """Greedy Best-First Search may not find the cheapest path."""
        #  A --(1)--> B --(1)--> D (goal)
        #  A --(100)--> C --(1)--> D
        #  h(B)=10, h(C)=1 => picks C first despite higher edge cost
        graph = Graph(directed=True)
        graph.add_edge("A", "B", weight=1.0)
        graph.add_edge("B", "D", weight=1.0)
        graph.add_edge("A", "C", weight=100.0)
        graph.add_edge("C", "D", weight=1.0)

        heuristic_values = {"A": 5, "B": 10, "C": 1, "D": 0}
        h = lambda state, goal: heuristic_values.get(state, float("inf"))

        result = greedy_best_first_search(graph, "A", "D", h=h)

        assert result is not None
        path_states = [node.state for node in result.get_path()]
        # Greedy picks A->C->D (cost 101) because h(C)=1 < h(B)=10
        assert path_states == ["A", "C", "D"]
        assert result.path_cost == 101.0

    def test_linear_path(self):
        """Finds a path in a linear graph."""
        graph = Graph()
        graph.add_edge(1, 2)
        graph.add_edge(2, 3)
        result = greedy_best_first_search(graph, 1, 3, h=simple_heuristic)

        assert result is not None
        path_states = [node.state for node in result.get_path()]
        assert path_states == [1, 2, 3]


class TestGreedyBestFirstSearchCycleHandling:
    """Tests that Greedy Best-First Search handles cycles without infinite loops."""

    def test_triangle_cycle(self):
        """Handles a simple cycle (A-B-C-A) without looping."""
        graph = Graph()
        graph.add_edge("A", "B")
        graph.add_edge("B", "C")
        graph.add_edge("C", "A")
        result = greedy_best_first_search(graph, "A", "C", h=letter_heuristic)

        assert result is not None
        assert result.state == "C"

    def test_self_loop(self):
        """Handles a node with an edge to itself."""
        graph = Graph()
        graph.add_edge("A", "A")
        graph.add_edge("A", "B")
        result = greedy_best_first_search(graph, "A", "B", h=letter_heuristic)

        assert result is not None
        assert result.state == "B"


class TestGreedyBestFirstSearchLargerGraphs:
    """Tests on more complex graph structures."""

    def test_diamond_graph(self):
        """Picks the heuristically better branch in a diamond graph."""
        #       A
        #      / \
        #     B   C
        #      \ /
        #       D
        graph = Graph()
        graph.add_edge("A", "B")
        graph.add_edge("A", "C")
        graph.add_edge("B", "D")
        graph.add_edge("C", "D")

        # h(B)=5, h(C)=1 => prefer C
        heuristic_values = {"A": 3, "B": 5, "C": 1, "D": 0}
        h = lambda state, goal: heuristic_values.get(state, float("inf"))

        result = greedy_best_first_search(graph, "A", "D", h=h)

        assert result is not None
        path_states = [node.state for node in result.get_path()]
        assert path_states == ["A", "C", "D"]

    def test_disconnected_components(self):
        """Returns None when start and goal are in different components."""
        graph = Graph()
        graph.add_edge("A", "B")
        graph.add_edge("B", "C")
        graph.add_edge("X", "Y")
        graph.add_edge("Y", "Z")
        result = greedy_best_first_search(graph, "A", "Z", h=letter_heuristic)

        assert result is None

    def test_multi_level_graph(self):
        """Works on a multi-level directed graph."""
        graph = Graph(directed=True)
        graph.add_edge(1, 2)
        graph.add_edge(1, 3)
        graph.add_edge(2, 4)
        graph.add_edge(3, 4)
        graph.add_edge(4, 5)
        result = greedy_best_first_search(graph, 1, 5, h=simple_heuristic)

        assert result is not None
        assert result.state == 5


class TestGreedyBestFirstSearchManhattan:
    """Tests using the default Manhattan heuristic on 2D grid graphs."""

    def test_grid_simple_path(self):
        """On a small 2D grid using Manhattan distance."""
        #  (0,0) -> (0,1) -> (0,2)
        #    |                  |
        #  (1,0) ----------> (1,2)
        graph = Graph(directed=True)
        graph.add_edge((0, 0), (0, 1))
        graph.add_edge((0, 1), (0, 2))
        graph.add_edge((0, 0), (1, 0))
        graph.add_edge((0, 2), (1, 2))
        graph.add_edge((1, 0), (1, 2))

        result = greedy_best_first_search(graph, (0, 0), (1, 2))

        assert result is not None
        assert result.state == (1, 2)

    def test_grid_prefers_closer_node(self):
        """Manhattan heuristic guides search toward the goal."""
        #  (0,0) -> (0,1) -> (0,2)
        #    |
        #  (1,0)
        # Goal is (0,2). h((0,1))=1, h((1,0))=3 => expands (0,1) first
        graph = Graph(directed=True)
        graph.add_edge((0, 0), (0, 1))
        graph.add_edge((0, 0), (1, 0))
        graph.add_edge((0, 1), (0, 2))

        result = greedy_best_first_search(graph, (0, 0), (0, 2))

        assert result is not None
        path_states = [node.state for node in result.get_path()]
        assert path_states == [(0, 0), (0, 1), (0, 2)]


class TestGreedyBestFirstSearchEdgeCases:
    """Edge case tests."""

    def test_single_node_graph(self):
        """On a graph where start == goal."""
        graph = Graph()
        graph.add_edge("A", "B")
        result = greedy_best_first_search(graph, "A", "A", h=letter_heuristic)

        assert result is not None
        assert result.state == "A"
        path_states = [node.state for node in result.get_path()]
        assert path_states == ["A"]

    def test_numeric_nodes(self):
        """Works with integer node identifiers."""
        graph = Graph()
        graph.add_edge(1, 2)
        graph.add_edge(2, 3)
        graph.add_edge(3, 4)
        result = greedy_best_first_search(graph, 1, 4, h=simple_heuristic)

        assert result is not None
        path_states = [node.state for node in result.get_path()]
        assert path_states == [1, 2, 3, 4]

    def test_result_node_has_correct_parent_chain(self):
        """Each node in the returned path has the correct parent reference."""
        graph = Graph()
        graph.add_edge("A", "B")
        graph.add_edge("B", "C")
        graph.add_edge("C", "D")
        result = greedy_best_first_search(graph, "A", "D", h=letter_heuristic)

        assert result is not None
        assert result.state == "D"
        assert result.parent.state == "C"
        assert result.parent.parent.state == "B"
        assert result.parent.parent.parent.state == "A"
        assert result.parent.parent.parent.parent is None

    def test_path_cost_tracking(self):
        """Correctly accumulates path_cost along the path."""
        graph = Graph()
        graph.add_edge("A", "B", weight=3.0)
        graph.add_edge("B", "C", weight=7.0)
        result = greedy_best_first_search(graph, "A", "C", h=letter_heuristic)

        assert result is not None
        assert result.path_cost == 10.0
