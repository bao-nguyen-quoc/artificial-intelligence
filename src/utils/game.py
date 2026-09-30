from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


class Game(ABC):
    """
    Interface for a 2-player, zero-sum, perfect-information, deterministic game.

    Convention: every value (utility / evaluate) is from the point of view of MAX.
    MAX wants a high value, MIN wants a low value.
    States must be treated as immutable: `result` returns a NEW state.
    """

    @abstractmethod
    def initial_state(self) -> Any:
        """Return the starting state."""

    @abstractmethod
    def to_move(self, state: Any) -> bool:
        """Return True if it is MAX's turn in `state`, False if it is MIN's turn."""

    @abstractmethod
    def actions(self, state: Any) -> list:
        """Return legal actions in `state`, in a fixed deterministic order."""

    @abstractmethod
    def result(self, state: Any, action: Any) -> Any:
        """Return the new state after applying `action` (never mutate `state`)."""

    @abstractmethod
    def is_terminal(self, state: Any) -> bool:
        """Return True if the game is over in `state`."""

    @abstractmethod
    def utility(self, state: Any) -> float:
        """Exact value of a terminal state, from MAX's point of view."""

    @abstractmethod
    def evaluate(self, state: Any) -> float:
        """Heuristic value of a non-terminal state, from MAX's point of view."""


@dataclass
class SearchResult:
    """Result returned by every minimax variant."""

    value: float  # minimax value of the root, from MAX's point of view
    action: Any | None  # best action at the root (None if root is terminal/cut off)
    nodes_expanded: int = 0  # number of nodes visited (used to compare variants)


@dataclass
class SearchStats:
    """Mutable counter shared by all recursive calls of one search."""

    nodes: int = 0
