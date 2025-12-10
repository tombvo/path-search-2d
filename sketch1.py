"""
2D Pathfinding Visualization Tool

A terminal-based visualization of the Breadth-First Search (BFS) algorithm
for finding the shortest path in a 2D grid with obstacles.
"""

from __future__ import annotations

import os
from collections import deque
from dataclasses import dataclass, field
from enum import Enum
from random import randint
from typing import Optional

import colorama
from rich import print as rich_print

# Initialize terminal colors
colorama.init()
os.system("")


class Direction(Enum):
    """Cardinal directions for neighbor searching."""
    UP = (-1, 0)
    RIGHT = (0, 1)
    DOWN = (1, 0)
    LEFT = (0, -1)


@dataclass
class Field:
    """Represents a single cell in the grid."""
    row: int
    col: int
    is_obstacle: bool = False
    is_start: bool = False
    is_end: bool = False
    was_searched: bool = False
    is_on_best_path: bool = False

    def __repr__(self) -> str:
        return f"Field({self.row}, {self.col})"

    def is_accessible(self) -> bool:
        """Check if this field can be traversed."""
        return not self.is_obstacle and not self.is_start and not self.was_searched


@dataclass
class SearchConfig:
    """Configuration for the pathfinding search."""
    rows: int = 15
    cols: int = 25
    obstacle_probability: int = 4  # 1 in N chance of obstacle
    start_col: int = 3
    end_col: int = 18
    log_file: Optional[str] = "paths.txt"


class Board:
    """Manages the 2D grid of fields."""

    def __init__(self, config: SearchConfig) -> None:
        self.config = config
        self.rows = config.rows
        self.cols = config.cols
        self.grid: list[list[Field]] = []
        self.start_field: Optional[Field] = None
        self.end_field: Optional[Field] = None
        self._create_grid()

    def _create_grid(self) -> None:
        """Initialize the grid with empty fields."""
        self.grid = [
            [Field(row, col) for col in range(self.cols)]
            for row in range(self.rows)
        ]

    def setup_start_end_obstacles(self) -> None:
        """Configure start point, end point, and random obstacles."""
        # Set start point (top row)
        self.start_field = self.grid[0][self.config.start_col]
        self.start_field.is_start = True

        # Set end point (bottom row)
        self.end_field = self.grid[self.rows - 1][self.config.end_col]
        self.end_field.is_end = True

        # Generate random obstacles (skip first and last rows)
        for row_idx in range(1, self.rows - 1):
            for col_idx in range(self.cols):
                if randint(1, self.config.obstacle_probability) == 1:
                    self.grid[row_idx][col_idx].is_obstacle = True

    def get_field(self, row: int, col: int) -> Optional[Field]:
        """Safely get a field by coordinates."""
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.grid[row][col]
        return None

    def get_neighbor(self, current_field: Field, direction: Direction) -> Optional[Field]:
        """
        Get a neighbor field in the given direction.
        Returns the field if accessible, None otherwise.
        """
        row_offset, col_offset = direction.value
        new_row = current_field.row + row_offset
        new_col = current_field.col + col_offset

        neighbor = self.get_field(new_row, new_col)
        if neighbor is None:
            return None

        # Cannot traverse obstacles or the start
        if neighbor.is_obstacle or neighbor.is_start:
            return None

        # End field is always accessible
        if neighbor.is_end:
            neighbor.was_searched = True
            return neighbor

        # Regular field - check if already visited
        if neighbor.was_searched:
            return None

        neighbor.was_searched = True
        return neighbor

    def reset_search_state(self) -> None:
        """Reset all search-related field states."""
        for row in self.grid:
            for cell in row:
                cell.was_searched = False
                cell.is_on_best_path = False


class Visualizer:
    """Handles terminal-based visualization of the board."""

    # Rich markup colors for different field states
    COLORS = {
        "obstacle": "[red]X[/]",
        "start": "[green]S[/]",
        "end": "[green]E[/]",
        "best_path": "[green]m[/]",
        "searched": "[blue]m[/]",
        "unsearched": "[yellow]m[/]",
    }

    def __init__(self, board: Board) -> None:
        self.board = board

    def clear_screen(self) -> None:
        """Clear the terminal screen."""
        rich_print("\033[0J")

    def move_cursor_up(self, lines: int) -> None:
        """Move cursor up by specified number of lines."""
        rich_print(f"\033[{lines}A")

    def render_board(self) -> None:
        """Render the current board state to the terminal."""
        for row in self.board.grid:
            rich_print("")
            for cell in row:
                symbol = self._get_cell_symbol(cell)
                rich_print(f"{symbol} ", end="")

    def _get_cell_symbol(self, cell: Field) -> str:
        """Get the display symbol for a cell based on its state."""
        if cell.is_obstacle:
            return self.COLORS["obstacle"]
        if cell.is_start:
            return self.COLORS["start"]
        if cell.is_end:
            return self.COLORS["end"]
        if cell.is_on_best_path:
            return self.COLORS["best_path"]
        if cell.was_searched:
            return self.COLORS["searched"]
        return self.COLORS["unsearched"]

    def animate_best_path(self, path: list[Field]) -> None:
        """Animate the display of the best path."""
        self.move_cursor_up(self.board.rows + 3)
        for cell in path:
            self.board.grid[cell.row][cell.col].is_on_best_path = True
            self.render_board()
            self.move_cursor_up(self.board.rows + 1)


@dataclass
class SearchState:
    """Tracks the state during pathfinding."""
    paths: deque = field(default_factory=deque)
    completed_paths: list[list[Field]] = field(default_factory=list)
    iteration: int = 0
    found_end: bool = False


class PathFinder:
    """Implements BFS pathfinding algorithm with visualization."""

    DIRECTIONS = [Direction.UP, Direction.RIGHT, Direction.LEFT, Direction.DOWN]

    def __init__(self, board: Board, visualizer: Visualizer, config: SearchConfig) -> None:
        self.board = board
        self.visualizer = visualizer
        self.config = config
        self.state = SearchState()

    def find_path(self) -> Optional[list[Field]]:
        """
        Execute BFS to find the shortest path from start to end.
        Returns the shortest path if found, None otherwise.
        """
        if self.board.start_field is None:
            return None

        self._initialize_search()
        self._run_bfs()

        if self.state.completed_paths:
            return self._get_shortest_path()
        return None

    def _initialize_search(self) -> None:
        """Initialize the search state."""
        self.state = SearchState()
        self.state.paths.append([self.board.start_field])

        # Clear log file
        if self.config.log_file:
            with open(self.config.log_file, "w") as f:
                f.write("")

    def _run_bfs(self) -> None:
        """Run the BFS algorithm with visualization."""
        while self.state.paths:
            current_path = self.state.paths.popleft()
            current_field = current_path[-1]

            new_paths = self._explore_neighbors(current_field, current_path)
            self.state.paths.extend(new_paths)

            self.visualizer.render_board()

            # Check if we've completed an iteration (all paths at current depth explored)
            if not self.state.paths and self.state.completed_paths:
                self._log_iteration()

                if self.state.found_end:
                    break

                # Continue with paths from completed iteration
                self.state.paths = deque(self.state.completed_paths)
                self.state.completed_paths = []
                self.state.iteration += 1

            elif self.state.paths:
                self.visualizer.move_cursor_up(self.board.rows + 1)

    def _explore_neighbors(
        self, current_field: Field, current_path: list[Field]
    ) -> list[list[Field]]:
        """Explore all neighbors of the current field."""
        new_paths = []

        for direction in self.DIRECTIONS:
            neighbor = self.board.get_neighbor(current_field, direction)
            if neighbor is not None:
                new_path = current_path + [neighbor]
                self.state.completed_paths.append(new_path)

                if neighbor.is_end:
                    self.state.found_end = True

        return new_paths

    def _get_shortest_path(self) -> list[Field]:
        """Find the shortest path that reaches the end."""
        shortest_path: Optional[list[Field]] = None

        for path in self.state.completed_paths:
            if path and path[-1].is_end:
                if shortest_path is None or len(path) < len(shortest_path):
                    shortest_path = path

        return shortest_path if shortest_path else []

    def _log_iteration(self) -> None:
        """Log the current iteration state to file."""
        if not self.config.log_file:
            return

        with open(self.config.log_file, "a+") as f:
            f.write(f"Iteration Number: {self.state.iteration}\n")
            f.write(f"Length of paths: {len(self.state.paths)}\n")
            f.write(f"Length of completed_paths: {len(self.state.completed_paths)}\n")
            f.write(f"Paths: {list(self.state.paths)}\n")
            f.write(f"Completed paths: {self.state.completed_paths}\n\n")


def main() -> None:
    """Main entry point for the pathfinding visualization."""
    config = SearchConfig()

    # Initialize components
    board = Board(config)
    board.setup_start_end_obstacles()

    visualizer = Visualizer(board)
    visualizer.clear_screen()

    pathfinder = PathFinder(board, visualizer, config)

    # Find and display the shortest path
    best_path = pathfinder.find_path()

    if best_path:
        rich_print(f"\nBest Path: {best_path}")
        visualizer.animate_best_path(best_path)
    else:
        rich_print("\nNo path found!")


if __name__ == "__main__":
    main()
