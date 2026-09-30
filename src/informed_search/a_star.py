import heapq
import itertools
from collections.abc import Callable, Iterator
from typing import Any

from src.informed_search.greedy_best_first_search import manhattan_heuristic
from src.utils.graph import Graph, Node


def _push_to_open(
    state: Any,
    parent: Node | None,
    path_cost: float,
    goal: Any,
    h: Callable,
    open_states: dict[Any, Node],
    open_heap: list[tuple[float, int, Node]],
    counter: Iterator[int],
) -> None:
    """
    Helper function to push a node into open

    Args:
        state: State to push
        parent: Parent node
        path_cost: Path cost to this node
        goal: Goal node
        h: Heuristic function
        open_states: Dictionary of open states
        open_heap: Min-heap of open nodes
        counter: Counter for tie-breaking
    """
    child = Node(
        state=state,
        parent=parent,
        action=state if parent is not None else None,
        path_cost=path_cost,
    )
    f_cost = path_cost + h(state, goal)
    open_states[state] = child
    heapq.heappush(open_heap, (f_cost, next(counter), child))


def a_star(
    graph: Graph, start: Any, goal: Any, h: Callable = manhattan_heuristic
) -> Node | None:
    """
    A* Search Algorithm

    Expands the node with the lowest f(n) = g(n) + h(n) first.
    Guarantees optimal solution when heuristic is admissible: h(n) <= h*(n).

    Args:
        graph: Graph to search in
        start: Start node
        goal: Goal node
        h: Heuristic function h(state, goal) -> float

    Returns:
        Node if goal is found, None otherwise
    """
    # tie breaker for f(n)
    counter = itertools.count()

    open_heap: list[tuple[float, int, Node]] = []

    # Track best known nodes in open (state -> Node)
    # and closed nodes with their best g-cost (state -> g_cost)
    open_states: dict[Any, Node] = {}
    closed_states: dict[Any, float] = {}

    # Step 1: Put start node into open (min-heap ordered by f(n))
    _push_to_open(start, None, 0.0, goal, h, open_states, open_heap, counter)

    # Step 2: If open is empty -> search fails
    while open_heap:
        # Step 3: Take the node with lowest f(n) from open, call it O. Put O into closed.
        _, _, current = heapq.heappop(open_heap)

        # Skip stale entries (node was relaxed and re-added with better cost)
        if current.state in closed_states:
            continue
        if current.state in open_states and open_states[current.state] is not current:
            continue

        open_states.pop(current.state, None)
        closed_states[current.state] = current.path_cost

        # Step 4: If O is the goal -> search succeeds
        if current.state == goal:
            return current

        # Step 5: For each child C of O, compute g' = g(O) + cost(O, C)
        for neighbor in graph.get_neighbors(current.state):
            g_new = current.path_cost + graph.get_weight(current.state, neighbor)

            if neighbor not in open_states and neighbor not in closed_states:
                # C not in open and closed: add C to open
                _push_to_open(
                    neighbor, current, g_new, goal, h, open_states, open_heap, counter
                )

            elif neighbor in open_states and g_new < open_states[neighbor].path_cost:
                # g' < g(C): update g(C), f(C), parent
                _push_to_open(
                    neighbor,
                    current,
                    g_new,
                    goal,
                    h,
                    open_states,
                    open_heap,
                    counter,
                )

            # g' < g(C): re-open C (move from closed back to open)
            elif neighbor in closed_states and g_new < closed_states[neighbor]:
                del closed_states[neighbor]
                _push_to_open(
                    neighbor,
                    current,
                    g_new,
                    goal,
                    h,
                    open_states,
                    open_heap,
                    counter,
                )

    # Step 2 (loop ended): open is empty -> search fails
    return None
