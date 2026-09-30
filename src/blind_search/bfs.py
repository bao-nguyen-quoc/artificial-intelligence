from collections import deque

from src.utils.graph import Graph, Node


def bfs(graph: Graph, start: any, goal: any) -> Node | None:
    """
    Breadth-First Search Algorithm

    Args:
        graph: Graph to search in
        start: Start node
        goal: Goal node

    Returns:
        Node if goal is found, None otherwise
    """
    # Step 1: Put start node into open (FIFO queue)
    start_node = Node(state=start)
    open_list: deque[Node] = deque([start_node])

    # Track states in open and closed to avoid revisiting
    open_states: set = {start}
    closed_states: set = set()

    # Step 2: If open is empty -> search fails
    while open_list:
        # Step 3: Take the first node from open, call it O. Put O into closed.
        current = open_list.popleft()
        open_states.discard(current.state)
        closed_states.add(current.state)

        # Step 4: If O is the goal -> search succeeds
        if current.state == goal:
            return current

        # Step 5: Find all children of O not in open and closed, append to end of open.
        for neighbor in graph.get_neighbors(current.state):
            if neighbor not in open_states and neighbor not in closed_states:
                child = Node(
                    state=neighbor,
                    parent=current,
                    action=neighbor,
                    path_cost=current.path_cost
                    + graph.get_weight(current.state, neighbor),
                )
                open_list.append(child)
                open_states.add(neighbor)

    # Step 2 (loop ended): open is empty -> search fails
    return None
