import heapq

from src.utils import Graph, Node

def ucs(graph: Graph, start: any, goal: any) -> Node | None:
    """
    Uniform Cost Search Algorithm

    Args:
        graph: Graph to search in
        start: Start node
        goal: Goal node

    Returns:
        Node if goal is found, None otherwise
    """
    # Step 1: Put start node into open (min-heap ordered by g(n))
    start_node = Node(state=start)
    counter = 0
    open_heap: list[tuple[float, int, Node]] = [(0.0, counter, start_node)]

    # Track best known cost for states in open, and closed set
    open_states: dict[any, Node] = {start: start_node}
    closed_states: set = set()

    # Step 2: If open is empty -> search fails
    while open_heap:
        # Step 3: Take the node with lowest g(n) from open, call it O. Put O into closed.
        _, _, current = heapq.heappop(open_heap)

        # Skip stale entries (node was already relaxed and re-added)
        if current.state in closed_states:
            continue

        open_states.pop(current.state, None)
        closed_states.add(current.state)

        # Step 4: If O is the goal -> search succeeds
        if current.state == goal:
            return current

        # Step 5: Find all children of O
        for neighbor in graph.get_neighbors(current.state):
            new_cost = current.path_cost + graph.get_weight(current.state, neighbor)

            if neighbor in closed_states:
                # If child already in closed, skip
                continue
            elif neighbor in open_states:
                # If child already in open but has higher g(child), update g(child) and parent
                existing = open_states[neighbor]
                if new_cost < existing.path_cost:
                    child = Node(
                        state=neighbor,
                        parent=current,
                        action=neighbor,
                        path_cost=new_cost,
                    )
                    open_states[neighbor] = child
                    counter += 1
                    heapq.heappush(open_heap, (new_cost, counter, child))
            else:
                # If child not in open and closed, add to open
                child = Node(
                    state=neighbor,
                    parent=current,
                    action=neighbor,
                    path_cost=new_cost,
                )
                open_states[neighbor] = child
                counter += 1
                heapq.heappush(open_heap, (new_cost, counter, child))

    # Step 2 (loop ended): open is empty -> search fails
    return None
