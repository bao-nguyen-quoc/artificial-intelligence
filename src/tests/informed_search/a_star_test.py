from src.informed_search.a_star import a_star
from src.utils import Graph


def zero_heuristic(state, goal) -> float:
    """Always returns 0 — makes A* behave like UCS."""
    return 0.0


def simple_heuristic(state, goal) -> float:
    """Simple admissible heuristic: absolute difference between numeric states."""
    return abs(state - goal)


def letter_heuristic(state, goal) -> float:
    """Heuristic for letter-based nodes: distance in alphabet order."""
    return abs(ord(state) - ord(goal))


class TestAStarBasic:
    """Basic A* functionality tests."""

    def test_direct_connection(self):
        """A* finds a goal that is a direct neighbor of start."""
        graph = Graph()
        graph.add_edge("A", "B", weight=5.0)
        result = a_star(graph, "A", "B", h=letter_heuristic)

        assert result is not None
        assert result.state == "B"
        assert result.path_cost == 5.0

    def test_start_is_goal(self):
        """A* returns immediately when start equals goal."""
        graph = Graph()
        graph.add_edge("A", "B", weight=1.0)
        result = a_star(graph, "A", "A", h=letter_heuristic)

        assert result is not None
        assert result.state == "A"
        assert result.parent is None
        assert result.path_cost == 0.0

    def test_goal_not_reachable(self):
        """A* returns None when the goal is unreachable."""
        graph = Graph()
        graph.add_edge("A", "B", weight=1.0)
        graph.add_edge("C", "D", weight=1.0)
        result = a_star(graph, "A", "D", h=letter_heuristic)

        assert result is None

    def test_goal_not_in_graph(self):
        """A* returns None when goal node does not exist in the graph."""
        graph = Graph()
        graph.add_edge("A", "B", weight=1.0)
        result = a_star(graph, "A", "Z", h=letter_heuristic)

        assert result is None


class TestAStarOptimalPath:
    """Tests that A* returns optimal (lowest-cost) paths with admissible heuristic."""

    def test_prefers_cheaper_path(self):
        """A* picks A->C (cost 2) over A->B->C (cost 6)."""
        graph = Graph()
        graph.add_edge("A", "B", weight=1.0)
        graph.add_edge("B", "C", weight=5.0)
        graph.add_edge("A", "C", weight=2.0)
        result = a_star(graph, "A", "C", h=letter_heuristic)

        assert result is not None
        path_states = [node.state for node in result.get_path()]
        assert path_states == ["A", "C"]
        assert result.path_cost == 2.0

    def test_prefers_longer_but_cheaper_path(self):
        """A* picks A->B->C->D (cost 3) over A->D (cost 10)."""
        graph = Graph()
        graph.add_edge("A", "B", weight=1.0)
        graph.add_edge("B", "C", weight=1.0)
        graph.add_edge("C", "D", weight=1.0)
        graph.add_edge("A", "D", weight=10.0)
        result = a_star(graph, "A", "D", h=letter_heuristic)

        assert result is not None
        path_states = [node.state for node in result.get_path()]
        assert path_states == ["A", "B", "C", "D"]
        assert result.path_cost == 3.0

    def test_a_star_vs_greedy(self):
        """A* finds optimal path where Greedy Best-First would not.

        Greedy would pick A->C->D (cost 101) because h(C)=1 < h(B)=2.
        A* considers f(n) = g(n) + h(n), so it picks A->B->D (cost 2).
        """
        graph = Graph(directed=True)
        graph.add_edge("A", "B", weight=1.0)
        graph.add_edge("B", "D", weight=1.0)
        graph.add_edge("A", "C", weight=100.0)
        graph.add_edge("C", "D", weight=1.0)

        heuristic_values = {"A": 2, "B": 1, "C": 1, "D": 0}
        h = lambda state, goal: heuristic_values.get(state, float("inf"))

        result = a_star(graph, "A", "D", h=h)

        assert result is not None
        path_states = [node.state for node in result.get_path()]
        assert path_states == ["A", "B", "D"]
        assert result.path_cost == 2.0

    def test_with_zero_heuristic_behaves_like_ucs(self):
        """With h=0, A* degenerates into UCS and still finds optimal path."""
        graph = Graph()
        graph.add_edge("A", "B", weight=1.0)
        graph.add_edge("B", "C", weight=1.0)
        graph.add_edge("A", "C", weight=10.0)
        result = a_star(graph, "A", "C", h=zero_heuristic)

        assert result is not None
        path_states = [node.state for node in result.get_path()]
        assert path_states == ["A", "B", "C"]
        assert result.path_cost == 2.0

    def test_equal_costs_still_finds_goal(self):
        """A* finds a goal when multiple paths have identical cost."""
        graph = Graph()
        graph.add_edge("A", "B", weight=5.0)
        graph.add_edge("A", "C", weight=5.0)
        graph.add_edge("B", "D", weight=5.0)
        graph.add_edge("C", "D", weight=5.0)
        result = a_star(graph, "A", "D", h=letter_heuristic)

        assert result is not None
        assert result.state == "D"
        assert result.path_cost == 10.0

    def test_path_cost_accumulation(self):
        """A* correctly accumulates path_cost (g(n)) along the optimal path."""
        graph = Graph()
        graph.add_edge("A", "B", weight=3.0)
        graph.add_edge("B", "C", weight=4.0)
        graph.add_edge("C", "D", weight=2.0)
        result = a_star(graph, "A", "D", h=letter_heuristic)

        assert result is not None
        assert result.path_cost == 9.0


class TestAStarRelaxation:
    """Tests that A* correctly relaxes paths in open and re-opens closed nodes."""

    def test_relaxes_open_node(self):
        """A* updates a node in open when a cheaper path is found.

        A --(10)--> D     (D first added to open with g=10)
        A --(1)-->  B --(1)--> D   (D later discovered via B with g=2, relaxed)
        """
        graph = Graph(directed=True)
        graph.add_edge("A", "D", weight=10.0)
        graph.add_edge("A", "B", weight=1.0)
        graph.add_edge("B", "D", weight=1.0)
        result = a_star(graph, "A", "D", h=letter_heuristic)

        assert result is not None
        path_states = [node.state for node in result.get_path()]
        assert path_states == ["A", "B", "D"]
        assert result.path_cost == 2.0

    def test_relaxation_with_multiple_paths(self):
        """A* relaxes path costs correctly across multiple competing paths.

        A --(1)--> B --(1)--> C --(1)--> E
        A --(2)--> D --(1)--> E
        A --(100)--> E
        Optimal: A->B->C->E or A->D->E (both cost 3), cheaper than A->E (100).
        """
        graph = Graph(directed=True)
        graph.add_edge("A", "B", weight=1.0)
        graph.add_edge("B", "C", weight=1.0)
        graph.add_edge("C", "E", weight=1.0)
        graph.add_edge("A", "D", weight=2.0)
        graph.add_edge("D", "E", weight=1.0)
        graph.add_edge("A", "E", weight=100.0)
        result = a_star(graph, "A", "E", h=letter_heuristic)

        assert result is not None
        assert result.path_cost == 3.0

    def test_reopens_closed_node(self):
        """A* re-opens a node from closed when a cheaper g' is found.

        A --(5)--> B --(1)--> D (goal)
        A --(1)--> C --(1)--> B    (cheaper B via C, g=2 < 5)
        h: A=3, B=1, C=2, D=0

        Trace:
          Pop A: add B(g=5,f=6), add C(g=1,f=3)
          Pop C(f=3): B in open g=5, new g=2 < 5 → relax B
          Pop B(g=2,f=3): add D(g=3,f=3)
          Pop D: goal! Path: A->C->B->D, cost=3
        """
        graph = Graph(directed=True)
        graph.add_edge("A", "B", weight=5.0)
        graph.add_edge("B", "D", weight=1.0)
        graph.add_edge("A", "C", weight=1.0)
        graph.add_edge("C", "B", weight=1.0)

        heuristic_values = {"A": 3, "B": 1, "C": 2, "D": 0}
        h = lambda state, goal: heuristic_values.get(state, float("inf"))

        result = a_star(graph, "A", "D", h=h)

        assert result is not None
        path_states = [node.state for node in result.get_path()]
        assert path_states == ["A", "C", "B", "D"]
        assert result.path_cost == 3.0

    def test_reopen_from_closed_with_cheaper_path(self):
        """A* moves a node from closed back to open when g' < g(C).

        A --(3)--> B --(1)--> D
        A --(1)--> C --(1)--> B
        h: A=2, B=1, C=3, D=0

        Trace:
          Pop A: add B(g=3,f=4), add C(g=1,f=4)
          Pop B(g=3,f=4,counter=1): closed={A,B}, add D(g=4,f=4)
          Pop C(g=1,f=4,counter=2): B in closed, g'=2 < 3 → re-open B
          Pop B(g=2,f=3): D in open g=4, new g=3 < 4 → relax D
          Pop D(g=3): goal! Path: A->C->B->D, cost=3
        """
        graph = Graph(directed=True)
        graph.add_edge("A", "B", weight=3.0)
        graph.add_edge("B", "D", weight=1.0)
        graph.add_edge("A", "C", weight=1.0)
        graph.add_edge("C", "B", weight=1.0)

        heuristic_values = {"A": 2, "B": 1, "C": 3, "D": 0}
        h = lambda state, goal: heuristic_values.get(state, float("inf"))

        result = a_star(graph, "A", "D", h=h)

        assert result is not None
        path_states = [node.state for node in result.get_path()]
        assert path_states == ["A", "C", "B", "D"]
        assert result.path_cost == 3.0

    def test_relaxation_on_undirected_graph(self):
        """A* finds optimal path on undirected graph thanks to relaxation.

        A --(1)-- B --(1)-- C --(1)-- D
        A --(10)-- D
        Without relaxation, D added from A with g=10 blocks the cheaper path.
        With relaxation, D is updated to g=3 via A->B->C->D.
        """
        graph = Graph()
        graph.add_edge("A", "B", weight=1.0)
        graph.add_edge("B", "C", weight=1.0)
        graph.add_edge("C", "D", weight=1.0)
        graph.add_edge("A", "D", weight=10.0)
        result = a_star(graph, "A", "D", h=letter_heuristic)

        assert result is not None
        assert result.path_cost == 3.0
        path_states = [node.state for node in result.get_path()]
        assert path_states == ["A", "B", "C", "D"]


class TestAStarHeuristicInfluence:
    """Tests that the heuristic steers expansion order."""

    def test_heuristic_guides_expansion(self):
        """A* expands toward lower f(n), combining cost and heuristic.

        A -> B (g=1, h=10, f=11)
        A -> C (g=1, h=1,  f=2) -> D (goal)
        f(C)=2 < f(B)=11 => A* expands C first.
        """
        graph = Graph(directed=True)
        graph.add_edge("A", "B", weight=1.0)
        graph.add_edge("A", "C", weight=1.0)
        graph.add_edge("C", "D", weight=1.0)
        graph.add_edge("B", "D", weight=1.0)

        heuristic_values = {"A": 3, "B": 10, "C": 1, "D": 0}
        h = lambda state, goal: heuristic_values.get(state, float("inf"))

        result = a_star(graph, "A", "D", h=h)

        assert result is not None
        path_states = [node.state for node in result.get_path()]
        assert path_states == ["A", "C", "D"]


class TestAStarCycleHandling:
    """Tests that A* handles cycles without infinite loops."""

    def test_triangle_cycle(self):
        """A* handles a simple cycle (A-B-C-A) without looping."""
        graph = Graph()
        graph.add_edge("A", "B", weight=1.0)
        graph.add_edge("B", "C", weight=1.0)
        graph.add_edge("C", "A", weight=1.0)
        result = a_star(graph, "A", "C", h=letter_heuristic)

        assert result is not None
        assert result.state == "C"

    def test_self_loop(self):
        """A* handles a node with an edge to itself."""
        graph = Graph()
        graph.add_edge("A", "A", weight=1.0)
        graph.add_edge("A", "B", weight=2.0)
        result = a_star(graph, "A", "B", h=letter_heuristic)

        assert result is not None
        assert result.state == "B"
        assert result.path_cost == 2.0


class TestAStarLargerGraphs:
    """Tests on more complex graph structures."""

    def test_asymmetric_diamond(self):
        """A* picks the cheapest total path in a weighted diamond.

           A
        1/   \\5
        B     C
        1\\   /1
           D
        """
        graph = Graph()
        graph.add_edge("A", "B", weight=1.0)
        graph.add_edge("A", "C", weight=5.0)
        graph.add_edge("B", "D", weight=1.0)
        graph.add_edge("C", "D", weight=1.0)
        result = a_star(graph, "A", "D", h=letter_heuristic)

        assert result is not None
        path_states = [node.state for node in result.get_path()]
        assert path_states == ["A", "B", "D"]
        assert result.path_cost == 2.0

    def test_disconnected_components(self):
        """A* returns None when start and goal are in different components."""
        graph = Graph()
        graph.add_edge("A", "B", weight=1.0)
        graph.add_edge("B", "C", weight=1.0)
        graph.add_edge("X", "Y", weight=1.0)
        graph.add_edge("Y", "Z", weight=1.0)
        result = a_star(graph, "A", "Z", h=letter_heuristic)

        assert result is None

    def test_numeric_multi_level(self):
        """A* on a multi-level directed graph with numeric nodes."""
        graph = Graph(directed=True)
        graph.add_edge(1, 2, weight=1.0)
        graph.add_edge(1, 3, weight=5.0)
        graph.add_edge(2, 4, weight=1.0)
        graph.add_edge(3, 4, weight=1.0)
        graph.add_edge(4, 5, weight=1.0)
        result = a_star(graph, 1, 5, h=simple_heuristic)

        assert result is not None
        path_states = [node.state for node in result.get_path()]
        assert path_states == [1, 2, 4, 5]
        assert result.path_cost == 3.0


class TestAStarManhattan:
    """Tests using the default Manhattan heuristic on 2D grid graphs."""

    def test_grid_simple_path(self):
        """A* on a small 2D grid using Manhattan distance."""
        graph = Graph(directed=True)
        graph.add_edge((0, 0), (0, 1), weight=1.0)
        graph.add_edge((0, 1), (0, 2), weight=1.0)
        graph.add_edge((0, 0), (1, 0), weight=1.0)
        graph.add_edge((0, 2), (1, 2), weight=1.0)
        graph.add_edge((1, 0), (1, 2), weight=2.0)

        result = a_star(graph, (0, 0), (1, 2))

        assert result is not None
        assert result.state == (1, 2)
        assert result.path_cost == 3.0

    def test_grid_prefers_closer_node(self):
        """Manhattan heuristic guides A* toward the goal efficiently."""
        graph = Graph(directed=True)
        graph.add_edge((0, 0), (0, 1), weight=1.0)
        graph.add_edge((0, 0), (1, 0), weight=1.0)
        graph.add_edge((0, 1), (0, 2), weight=1.0)

        result = a_star(graph, (0, 0), (0, 2))

        assert result is not None
        path_states = [node.state for node in result.get_path()]
        assert path_states == [(0, 0), (0, 1), (0, 2)]
        assert result.path_cost == 2.0


class TestAStarEdgeCases:
    """Edge case tests."""

    def test_single_node_graph(self):
        """A* on a graph where start == goal."""
        graph = Graph()
        graph.add_edge("A", "B", weight=1.0)
        result = a_star(graph, "A", "A", h=letter_heuristic)

        assert result is not None
        assert result.state == "A"
        path_states = [node.state for node in result.get_path()]
        assert path_states == ["A"]

    def test_numeric_nodes(self):
        """A* works with integer node identifiers."""
        graph = Graph()
        graph.add_edge(1, 2, weight=3.0)
        graph.add_edge(2, 3, weight=4.0)
        graph.add_edge(3, 4, weight=5.0)
        result = a_star(graph, 1, 4, h=simple_heuristic)

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
        result = a_star(graph, "A", "D", h=letter_heuristic)

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
        result = a_star(graph, "A", "C", h=letter_heuristic)

        assert result is not None
        assert result.path_cost == 10.0
