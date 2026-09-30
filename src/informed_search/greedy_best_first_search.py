import heapq
from collections.abc import Callable
from typing import Any

from src.utils.graph import Graph, Node


def manhattan_heuristic(state: Any, goal: Any) -> float:
    """
    Manhattan heuristic function for 2D grid.

    Args:
        state: Current state as (row, col) tuple.
        goal: Goal state as (row, col) tuple.

    Returns:
        float: The Manhattan distance.
    """
    return abs(state[0] - goal[0]) + abs(state[1] - goal[1])


def greedy_best_first_search(
    graph: Graph, start: Any, goal: Any, h: Callable = manhattan_heuristic
) -> Node | None:
    """
    Greedy Best-First Search Algorithm

    Expands the node with the lowest heuristic estimate h(n) first.

    Args:
        graph: Graph to search in
        start: Start node
        goal: Goal node
        h: Heuristic function h(state, goal) -> float

    Returns:
        Node if goal is found, None otherwise
    """
    # Step 1: Put start node into open (min-heap ordered by h(n))
    start_node = Node(state=start)
    # tie breaker for h(n)
    counter = 0
    open_heap: list[tuple[float, int, Node]] = [(h(start, goal), counter, start_node)]

    # Track states in open and closed to avoid revisiting
    open_states: set = {start}
    closed_states: set = set()

    # Step 2: If open is empty -> search fails
    while open_heap:
        # Step 3: Take the node with lowest h(n) from open, call it O. Put O into closed.
        _, _, current = heapq.heappop(open_heap)
        open_states.discard(current.state)
        closed_states.add(current.state)

        # Step 4: If O is the goal -> search succeeds
        if current.state == goal:
            return current

        # Step 5: Find all children of O not in open and closed,
        #         add to open sorted by ascending h(n).
        for neighbor in graph.get_neighbors(current.state):
            if neighbor not in open_states and neighbor not in closed_states:
                child = Node(
                    state=neighbor,
                    parent=current,
                    action=neighbor,
                    path_cost=current.path_cost
                    + graph.get_weight(current.state, neighbor),
                )
                open_states.add(neighbor)
                counter += 1
                heapq.heappush(open_heap, (h(neighbor, goal), counter, child))

    # Step 2 (loop ended): open is empty -> search fails
    return None
