from src.blind_search.bfs import bfs
from src.utils import Graph


class TestBfsBasic:
    """Basic BFS functionality tests."""

    def test_direct_connection(self):
        """BFS finds a goal that is a direct neighbor of start."""
        graph = Graph()
        graph.add_edge("A", "B")
        result = bfs(graph, "A", "B")

        assert result is not None
        assert result.state == "B"

    def test_start_is_goal(self):
        """BFS returns immediately when start equals goal."""
        graph = Graph()
        graph.add_edge("A", "B")
        result = bfs(graph, "A", "A")

        assert result is not None
        assert result.state == "A"
        assert result.parent is None

    def test_goal_not_reachable(self):
        """BFS returns None when the goal is unreachable."""
        graph = Graph()
        graph.add_edge("A", "B")
        graph.add_edge("C", "D")
        result = bfs(graph, "A", "D")

        assert result is None

    def test_goal_not_in_graph(self):
        """BFS returns None when goal node does not exist in the graph."""
        graph = Graph()
        graph.add_edge("A", "B")
        result = bfs(graph, "A", "Z")

        assert result is None


class TestBfsPath:
    """Tests that BFS returns the shallowest (fewest-edge) path."""

    def test_shortest_path_linear(self):
        """BFS finds path A -> B -> C in a linear graph."""
        graph = Graph()
        graph.add_edge("A", "B")
        graph.add_edge("B", "C")
        result = bfs(graph, "A", "C")

        assert result is not None
        path_states = [node.state for node in result.get_path()]
        assert path_states == ["A", "B", "C"]

    def test_shortest_path_with_shortcut(self):
        """BFS prefers A -> C (1 edge) over A -> B -> C (2 edges)."""
        #   A ---> B
        #   |      |
        #   +----> C
        graph = Graph()
        graph.add_edge("A", "B")
        graph.add_edge("B", "C")
        graph.add_edge("A", "C")
        result = bfs(graph, "A", "C")

        assert result is not None
        path_states = [node.state for node in result.get_path()]
        # BFS explores layer by layer, so it finds the direct edge first
        assert path_states == ["A", "C"]

    def test_path_cost_tracking(self):
        """BFS correctly accumulates path_cost along the path."""
        graph = Graph()
        graph.add_edge("A", "B", weight=3.0)
        graph.add_edge("B", "C", weight=7.0)
        result = bfs(graph, "A", "C")

        assert result is not None
        assert result.path_cost == 10.0


class TestBfsCycleHandling:
    """Tests that BFS handles cycles without infinite loops."""

    def test_triangle_cycle(self):
        """BFS handles a simple cycle (A-B-C-A) without looping."""
        graph = Graph()
        graph.add_edge("A", "B")
        graph.add_edge("B", "C")
        graph.add_edge("C", "A")
        result = bfs(graph, "A", "C")

        assert result is not None
        assert result.state == "C"

    def test_self_loop(self):
        """BFS handles a node with an edge to itself."""
        graph = Graph()
        graph.add_edge("A", "A")
        graph.add_edge("A", "B")
        result = bfs(graph, "A", "B")

        assert result is not None
        assert result.state == "B"


class TestBfsLargerGraphs:
    """Tests on more complex graph structures."""

    def test_diamond_graph(self):
        """BFS on a diamond-shaped graph (A -> B,C -> D)."""
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
        result = bfs(graph, "A", "D")

        assert result is not None
        path_states = [node.state for node in result.get_path()]
        # Both A->B->D and A->C->D are valid (same depth), BFS returns whichever is found first
        assert len(path_states) == 3
        assert path_states[0] == "A"
        assert path_states[-1] == "D"

    def test_multi_level_graph(self):
        """BFS traverses multiple levels correctly."""
        #  1 -> 2 -> 4
        #  |    |
        #  v    v
        #  3 -> 5 -> 6
        graph = Graph(directed=True)
        graph.add_edge(1, 2)
        graph.add_edge(1, 3)
        graph.add_edge(2, 4)
        graph.add_edge(2, 5)
        graph.add_edge(3, 5)
        graph.add_edge(5, 6)
        result = bfs(graph, 1, 6)

        assert result is not None
        path_states = [node.state for node in result.get_path()]
        # Shortest path: 1 -> 2 -> 5 -> 6 or 1 -> 3 -> 5 -> 6 (both length 3)
        assert len(path_states) == 4
        assert path_states[0] == 1
        assert path_states[-1] == 6

    def test_disconnected_components(self):
        """BFS returns None when start and goal are in different components."""
        graph = Graph()
        graph.add_edge("A", "B")
        graph.add_edge("B", "C")
        graph.add_edge("X", "Y")
        graph.add_edge("Y", "Z")
        result = bfs(graph, "A", "Z")

        assert result is None


class TestBfsEdgeCases:
    """Edge case tests."""

    def test_single_node_graph(self):
        """BFS on a graph with only one node (start == goal)."""
        graph = Graph()
        # Add a dummy edge so the node exists, but search for it as start == goal
        graph.add_edge("A", "B")
        result = bfs(graph, "A", "A")

        assert result is not None
        assert result.state == "A"
        path_states = [node.state for node in result.get_path()]
        assert path_states == ["A"]

    def test_numeric_nodes(self):
        """BFS works with integer node identifiers."""
        graph = Graph()
        graph.add_edge(1, 2)
        graph.add_edge(2, 3)
        graph.add_edge(3, 4)
        result = bfs(graph, 1, 4)

        assert result is not None
        path_states = [node.state for node in result.get_path()]
        assert path_states == [1, 2, 3, 4]

    def test_result_node_has_correct_parent_chain(self):
        """Each node in the returned path has the correct parent reference."""
        graph = Graph()
        graph.add_edge("A", "B")
        graph.add_edge("B", "C")
        graph.add_edge("C", "D")
        result = bfs(graph, "A", "D")

        assert result is not None
        assert result.state == "D"
        assert result.parent.state == "C"
        assert result.parent.parent.state == "B"
        assert result.parent.parent.parent.state == "A"
        assert result.parent.parent.parent.parent is None
