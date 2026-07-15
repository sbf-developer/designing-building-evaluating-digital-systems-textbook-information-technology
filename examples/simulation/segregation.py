"""A small, reproducible Schelling-style grid model.

The model is educational. It does not represent all causes or meanings of
residential segregation and should not be used to predict a real population.
"""

from dataclasses import dataclass
import random
from typing import Optional

Grid = list[list[Optional[str]]]


@dataclass(frozen=True)
class SimulationResult:
    grid: Grid
    steps: int
    unhappy_remaining: int


def neighbours_of(grid: Grid, row: int, col: int) -> list[Optional[str]]:
    """Return the eight surrounding cells inside the grid."""
    result: list[Optional[str]] = []
    for drow in (-1, 0, 1):
        for dcol in (-1, 0, 1):
            if drow == 0 and dcol == 0:
                continue
            new_row = row + drow
            new_col = col + dcol
            if 0 <= new_row < len(grid) and 0 <= new_col < len(grid[0]):
                result.append(grid[new_row][new_col])
    return result


def is_happy(grid: Grid, row: int, col: int, tolerance: float) -> bool:
    """Apply the model's local similarity rule."""
    agent = grid[row][col]
    if agent is None:
        return True
    occupied = [item for item in neighbours_of(grid, row, col) if item is not None]
    if not occupied:
        return True
    similar = sum(item == agent for item in occupied)
    return similar / len(occupied) >= tolerance


def make_grid(size: int = 8, empty_fraction: float = 0.2, seed: int = 7) -> Grid:
    """Create a balanced random grid using a local random generator."""
    if size <= 0:
        raise ValueError("size must be positive")
    if not 0 <= empty_fraction < 1:
        raise ValueError("empty_fraction must be in [0, 1)")
    rng = random.Random(seed)
    cells = ["A", "B"] * ((size * size) // 2 + 1)
    rng.shuffle(cells)
    grid: Grid = []
    for row in range(size):
        current: list[Optional[str]] = []
        for col in range(size):
            current.append(None if rng.random() < empty_fraction else cells.pop())
        grid.append(current)
    return grid


def run(grid: Grid, tolerance: float = 0.5, max_steps: int = 100) -> SimulationResult:
    """Move unhappy agents into empty cells until stable or bounded."""
    if not 0 <= tolerance <= 1:
        raise ValueError("tolerance must be in [0, 1]")
    if max_steps < 0:
        raise ValueError("max_steps must be non-negative")
    steps = 0
    while steps < max_steps:
        unhappy = [
            (row, col)
            for row in range(len(grid))
            for col in range(len(grid[0]))
            if grid[row][col] is not None and not is_happy(grid, row, col, tolerance)
        ]
        empty = [
            (row, col)
            for row in range(len(grid))
            for col in range(len(grid[0]))
            if grid[row][col] is None
        ]
        if not unhappy or not empty:
            break
        old = unhappy[0]
        new = empty[0]
        grid[new[0]][new[1]] = grid[old[0]][old[1]]
        grid[old[0]][old[1]] = None
        steps += 1
    remaining = sum(
        grid[row][col] is not None and not is_happy(grid, row, col, tolerance)
        for row in range(len(grid))
        for col in range(len(grid[0]))
    )
    return SimulationResult(grid=grid, steps=steps, unhappy_remaining=remaining)


if __name__ == "__main__":
    initial = make_grid()
    result = run(initial)
    print({"steps": result.steps, "unhappy_remaining": result.unhappy_remaining})
