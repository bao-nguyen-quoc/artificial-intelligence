from dataclasses import dataclass
from typing import Any


@dataclass
class Node:
    state: Any
    parent: "Node | None" = None
    action: Any = None
    path_cost: float = 0.0

    def get_path(self) -> list["Node"]:
        """
        Return list of nodes from root to current node.

        Returns:
            List of nodes from root to current node
        """
        nodes: list[Node] = []
        node: Node | None = self
        while node:
            nodes.append(node)
            node = node.parent
        return list(reversed(nodes))


class Graph:
    def __init__(self, directed=False):
        """Constructor"""
        self.edges: dict[Any, list] = {}
        self.weight: dict[tuple, float] = {}
        self.directed = directed

    def add_edge(self, u: Any, v: Any, weight: float = 1.0):
        """
        Add weighted edge to graph

        Args:
            u: Node to add edge `from`
            v: Node to add edge `to`
            weight: Weight of the edge
        """
        self.edges.setdefault(u, []).append(v)
        self.weight[(u, v)] = weight
        if not self.directed:
            self.edges.setdefault(v, []).append(u)
            self.weight[(v, u)] = weight

    def get_neighbors(self, node: Any) -> list:
        """
        Return list of neighbors of a node.

        Args:
            node: Node to get neighbors of

        Returns:
            List of neighbors of the node
        """
        return self.edges.get(node, [])

    def get_weight(self, u: Any, v: Any) -> float:
        """
        Return weight of an edge.

        Args:
            u: Node to get weight from
            v: Node to get weight to

        Returns:
            Weight of the edge
        """
        return self.weight.get((u, v), float("inf"))
