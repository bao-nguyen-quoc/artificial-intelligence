from src.blind_search.ucs import ucs
from src.utils.graph import Graph


class TestUcsBasic:
    """Basic UCS functionality tests."""

    def test_direct_connection(self):
        """UCS finds a goal that is a direct neighbor of start."""
        graph = Graph()
        graph.add_edge("A", "B", weight=5.0)
        result = ucs(graph, "A", "B")

        assert result is not None
        assert result.state == "B"
        assert result.path_cost == 5.0

    def test_start_is_goal(self):
        """UCS returns immediately when start equals goal."""
        graph = Graph()
        graph.add_edge("A", "B", weight=1.0)
        result = ucs(graph, "A", "A")

        assert result is not None
        assert result.state == "A"
        assert result.parent is None
        assert result.path_cost == 0.0

    def test_goal_not_reachable(self):
        """UCS returns None when the goal is unreachable."""
        graph = Graph()
        graph.add_edge("A", "B", weight=1.0)
        graph.add_edge("C", "D", weight=1.0)
        result = ucs(graph, "A", "D")

        assert result is None

    def test_goal_not_in_graph(self):
        """UCS returns None when goal node does not exist in the graph."""
        graph = Graph()
        graph.add_edge("A", "B", weight=1.0)
        result = ucs(graph, "A", "Z")

        assert result is None


class TestUcsOptimalPath:
    """Tests that UCS returns the lowest-cost path (not necessarily fewest edges)."""

    def test_prefers_cheaper_path(self):
        """UCS picks A->C (cost 2) over A->B->C (cost 1+5=6)."""
        graph = Graph()
        graph.add_edge("A", "B", weight=1.0)
        graph.add_edge("B", "C", weight=5.0)
        graph.add_edge("A", "C", weight=2.0)
        result = ucs(graph, "A", "C")

        assert result is not None
        path_states = [node.state for node in result.get_path()]
        assert path_states == ["A", "C"]
        assert result.path_cost == 2.0

    def test_prefers_longer_but_cheaper_path(self):
        """UCS picks the longer path A->B->C->D (cost 1+1+1=3) over A->D (cost 10)."""
        graph = Graph()
        graph.add_edge("A", "B", weight=1.0)
        graph.add_edge("B", "C", weight=1.0)
        graph.add_edge("C", "D", weight=1.0)
        graph.add_edge("A", "D", weight=10.0)
        result = ucs(graph, "A", "D")

        assert result is not None
        path_states = [node.state for node in result.get_path()]
        assert path_states == ["A", "B", "C", "D"]
        assert result.path_cost == 3.0

    def test_equal_costs_still_finds_goal(self):
        """UCS finds a goal when multiple paths have identical cost."""
        graph = Graph()
        graph.add_edge("A", "B", weight=5.0)
        graph.add_edge("A", "C", weight=5.0)
        graph.add_edge("B", "D", weight=5.0)
        graph.add_edge("C", "D", weight=5.0)
        result = ucs(graph, "A", "D")

        assert result is not None
        assert result.state == "D"
        assert result.path_cost == 10.0

    def test_path_cost_accumulation(self):
        """UCS correctly accumulates path_cost along the optimal path."""
        graph = Graph()
        graph.add_edge("A", "B", weight=3.0)
        graph.add_edge("B", "C", weight=4.0)
        graph.add_edge("C", "D", weight=2.0)
        result = ucs(graph, "A", "D")

        assert result is not None
        assert result.path_cost == 9.0


class TestUcsPathRelaxation:
    """Tests that UCS correctly updates (relaxes) paths when a cheaper route is found."""

    def test_relaxes_open_node(self):
        """UCS updates a node in open when a cheaper path is discovered."""
        #  A --(1)--> B --(1)--> D
        #  A --(10)--> D
        #  B is explored first (cost 1), then discovers D via B with cost 2,
        #  which is cheaper than the direct A->D (cost 10).
        graph = Graph(directed=True)
        graph.add_edge("A", "B", weight=1.0)
        graph.add_edge("A", "D", weight=10.0)
        graph.add_edge("B", "D", weight=1.0)
        result = ucs(graph, "A", "D")

        assert result is not None
        path_states = [node.state for node in result.get_path()]
        assert path_states == ["A", "B", "D"]
        assert result.path_cost == 2.0

    def test_relaxation_with_multiple_paths(self):
        """UCS relaxes path costs correctly across a more complex graph."""
        #  A --(1)--> B --(1)--> C --(1)--> E
        #  A --(2)--> D --(1)--> E
        #  A --(100)-> E
        #  Optimal: A->B->C->E (cost 3) vs A->D->E (cost 3) vs A->E (cost 100)
        graph = Graph(directed=True)
        graph.add_edge("A", "B", weight=1.0)
        graph.add_edge("B", "C", weight=1.0)
        graph.add_edge("C", "E", weight=1.0)
        graph.add_edge("A", "D", weight=2.0)
        graph.add_edge("D", "E", weight=1.0)
        graph.add_edge("A", "E", weight=100.0)
        result = ucs(graph, "A", "E")

        assert result is not None
        assert result.path_cost == 3.0


class TestUcsCycleHandling:
    """Tests that UCS handles cycles without infinite loops."""

    def test_triangle_cycle(self):
        """UCS handles a simple cycle (A-B-C-A) without looping."""
        graph = Graph()
        graph.add_edge("A", "B", weight=1.0)
        graph.add_edge("B", "C", weight=1.0)
        graph.add_edge("C", "A", weight=1.0)
        result = ucs(graph, "A", "C")

        assert result is not None
        assert result.state == "C"

    def test_self_loop(self):
        """UCS handles a node with an edge to itself."""
        graph = Graph()
        graph.add_edge("A", "A", weight=1.0)
        graph.add_edge("A", "B", weight=2.0)
        result = ucs(graph, "A", "B")

        assert result is not None
        assert result.state == "B"
        assert result.path_cost == 2.0


class TestUcsLargerGraphs:
    """Tests on more complex graph structures."""

    def test_weighted_diamond_graph(self):
        """UCS on a weighted diamond picks the cheapest path."""
        #       A
        #    1/   \10
        #    B     C
        #   10\   /1
        #       D
        graph = Graph()
        graph.add_edge("A", "B", weight=1.0)
        graph.add_edge("A", "C", weight=10.0)
        graph.add_edge("B", "D", weight=10.0)
        graph.add_edge("C", "D", weight=1.0)
        result = ucs(graph, "A", "D")

        assert result is not None
        # A->B->D costs 11, A->C->D costs 11, both equal — either is valid
        assert result.path_cost == 11.0

    def test_asymmetric_diamond(self):
        """UCS picks the cheaper branch in an asymmetric diamond."""
        #       A
        #    1/   \5
        #    B     C
        #    1\   /1
        #       D
        graph = Graph()
        graph.add_edge("A", "B", weight=1.0)
        graph.add_edge("A", "C", weight=5.0)
        graph.add_edge("B", "D", weight=1.0)
        graph.add_edge("C", "D", weight=1.0)
        result = ucs(graph, "A", "D")

        assert result is not None
        path_states = [node.state for node in result.get_path()]
        assert path_states == ["A", "B", "D"]
        assert result.path_cost == 2.0

    def test_disconnected_components(self):
        """UCS returns None when start and goal are in different components."""
        graph = Graph()
        graph.add_edge("A", "B", weight=1.0)
        graph.add_edge("B", "C", weight=1.0)
        graph.add_edge("X", "Y", weight=1.0)
        graph.add_edge("Y", "Z", weight=1.0)
        result = ucs(graph, "A", "Z")

        assert result is None

    def test_ucs_becomes_bfs_with_uniform_weights(self):
        """When all edges have weight 1, UCS behaves like BFS (finds shallowest path)."""
        graph = Graph()
        graph.add_edge("A", "B", weight=1.0)
        graph.add_edge("B", "C", weight=1.0)
        graph.add_edge("A", "C", weight=1.0)
        result = ucs(graph, "A", "C")

        assert result is not None
        path_states = [node.state for node in result.get_path()]
        # Direct A->C has cost 1, A->B->C has cost 2, so UCS picks A->C
        assert path_states == ["A", "C"]
        assert result.path_cost == 1.0


class TestUcsEdgeCases:
    """Edge case tests."""

    def test_single_node_graph(self):
        """UCS on a graph where start == goal."""
        graph = Graph()
        graph.add_edge("A", "B", weight=1.0)
        result = ucs(graph, "A", "A")

        assert result is not None
        assert result.state == "A"
        path_states = [node.state for node in result.get_path()]
        assert path_states == ["A"]

    def test_numeric_nodes(self):
        """UCS works with integer node identifiers."""
        graph = Graph()
        graph.add_edge(1, 2, weight=3.0)
        graph.add_edge(2, 3, weight=4.0)
        graph.add_edge(3, 4, weight=5.0)
        result = ucs(graph, 1, 4)

        assert result is not None
        path_states = [node.state for node in result.get_path()]
        assert path_states == [1, 2, 3, 4]
        assert result.path_cost == 12.0

    def test_result_node_has_correct_parent_chain(self):
        """Each node in the returned path has the correct parent reference."""
        graph = Graph()
        graph.add_edge("A", "B", weight=1.0)
        graph.add_edge("B", "C", weight=2.0)
        graph.add_edge("C", "D", weight=3.0)
        result = ucs(graph, "A", "D")

        assert result is not None
        assert result.state == "D"
        assert result.parent.state == "C"
        assert result.parent.parent.state == "B"
        assert result.parent.parent.parent.state == "A"
        assert result.parent.parent.parent.parent is None
