from src.utils import Graph
from src.blind_search.dfs import dfs


class TestDfsBasic:
    """Basic DFS functionality tests."""

    def test_direct_connection(self):
        """DFS finds a goal that is a direct neighbor of start."""
        graph = Graph()
        graph.add_edge("A", "B")
        result = dfs(graph, "A", "B")

        assert result is not None
        assert result.state == "B"

    def test_start_is_goal(self):
        """DFS returns immediately when start equals goal."""
        graph = Graph()
        graph.add_edge("A", "B")
        result = dfs(graph, "A", "A")

        assert result is not None
        assert result.state == "A"
        assert result.parent is None

    def test_goal_not_reachable(self):
        """DFS returns None when the goal is unreachable."""
        graph = Graph()
        graph.add_edge("A", "B")
        graph.add_edge("C", "D")
        result = dfs(graph, "A", "D")

        assert result is None

    def test_goal_not_in_graph(self):
        """DFS returns None when goal node does not exist in the graph."""
        graph = Graph()
        graph.add_edge("A", "B")
        result = dfs(graph, "A", "Z")

        assert result is None


class TestDfsPath:
    """Tests that DFS follows a depth-first traversal order."""

    def test_linear_path(self):
        """DFS finds path A -> B -> C in a linear graph."""
        graph = Graph()
        graph.add_edge("A", "B")
        graph.add_edge("B", "C")
        result = dfs(graph, "A", "C")

        assert result is not None
        path_states = [node.state for node in result.get_path()]
        assert path_states == ["A", "B", "C"]

    def test_dfs_goes_deep_first(self):
        """DFS goes deep before exploring siblings (LIFO behavior)."""
        #  A -> B -> D
        #  |
        #  +-> C
        graph = Graph(directed=True)
        graph.add_edge("A", "B")
        graph.add_edge("A", "C")
        graph.add_edge("B", "D")
        result = dfs(graph, "A", "D")

        assert result is not None
        path_states = [node.state for node in result.get_path()]
        # DFS prepends B's children before C, so it finds A -> B -> D
        assert path_states == ["A", "B", "D"]

    def test_path_cost_tracking(self):
        """DFS correctly accumulates path_cost along the path."""
        graph = Graph()
        graph.add_edge("A", "B", weight=3.0)
        graph.add_edge("B", "C", weight=7.0)
        result = dfs(graph, "A", "C")

        assert result is not None
        assert result.path_cost == 10.0


class TestDfsCycleHandling:
    """Tests that DFS handles cycles without infinite loops."""

    def test_triangle_cycle(self):
        """DFS handles a simple cycle (A-B-C-A) without looping."""
        graph = Graph()
        graph.add_edge("A", "B")
        graph.add_edge("B", "C")
        graph.add_edge("C", "A")
        result = dfs(graph, "A", "C")

        assert result is not None
        assert result.state == "C"

    def test_self_loop(self):
        """DFS handles a node with an edge to itself."""
        graph = Graph()
        graph.add_edge("A", "A")
        graph.add_edge("A", "B")
        result = dfs(graph, "A", "B")

        assert result is not None
        assert result.state == "B"

    def test_complex_cycle(self):
        """DFS handles a graph with multiple cycles."""
        #  A -> B -> C
        #  ^         |
        #  |         v
        #  +--- D <--+
        graph = Graph(directed=True)
        graph.add_edge("A", "B")
        graph.add_edge("B", "C")
        graph.add_edge("C", "D")
        graph.add_edge("D", "A")
        result = dfs(graph, "A", "D")

        assert result is not None
        assert result.state == "D"


class TestDfsLargerGraphs:
    """Tests on more complex graph structures."""

    def test_diamond_graph(self):
        """DFS on a diamond-shaped graph (A -> B,C -> D)."""
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
        result = dfs(graph, "A", "D")

        assert result is not None
        path_states = [node.state for node in result.get_path()]
        # DFS goes deep via B first, so path is A -> B -> D
        assert path_states[0] == "A"
        assert path_states[-1] == "D"

    def test_deep_chain(self):
        """DFS traverses a long chain correctly."""
        graph = Graph(directed=True)
        graph.add_edge(1, 2)
        graph.add_edge(2, 3)
        graph.add_edge(3, 4)
        graph.add_edge(4, 5)
        graph.add_edge(5, 6)
        result = dfs(graph, 1, 6)

        assert result is not None
        path_states = [node.state for node in result.get_path()]
        assert path_states == [1, 2, 3, 4, 5, 6]

    def test_disconnected_components(self):
        """DFS returns None when start and goal are in different components."""
        graph = Graph()
        graph.add_edge("A", "B")
        graph.add_edge("B", "C")
        graph.add_edge("X", "Y")
        graph.add_edge("Y", "Z")
        result = dfs(graph, "A", "Z")

        assert result is None


class TestDfsEdgeCases:
    """Edge case tests."""

    def test_single_node_graph(self):
        """DFS on a graph where start == goal."""
        graph = Graph()
        graph.add_edge("A", "B")
        result = dfs(graph, "A", "A")

        assert result is not None
        assert result.state == "A"
        path_states = [node.state for node in result.get_path()]
        assert path_states == ["A"]

    def test_numeric_nodes(self):
        """DFS works with integer node identifiers."""
        graph = Graph()
        graph.add_edge(1, 2)
        graph.add_edge(2, 3)
        graph.add_edge(3, 4)
        result = dfs(graph, 1, 4)

        assert result is not None
        path_states = [node.state for node in result.get_path()]
        assert path_states == [1, 2, 3, 4]

    def test_result_node_has_correct_parent_chain(self):
        """Each node in the returned path has the correct parent reference."""
        graph = Graph()
        graph.add_edge("A", "B")
        graph.add_edge("B", "C")
        graph.add_edge("C", "D")
        result = dfs(graph, "A", "D")

        assert result is not None
        assert result.state == "D"
        assert result.parent.state == "C"
        assert result.parent.parent.state == "B"
        assert result.parent.parent.parent.state == "A"
        assert result.parent.parent.parent.parent is None
