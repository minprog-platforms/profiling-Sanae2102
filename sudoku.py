from __future__ import annotations
from typing import Iterable, Sequence


class Sudoku:
    """A mutable sudoku puzzle."""

    def __init__(self, puzzle: Iterable[Iterable]):
        self._grid = []
        for puzzle_row in puzzle:
            for element in puzzle_row:
                self._grid.append([int(element)])

        self.rows = []
        for y in range(9):
            row = []
            for x in range(9):
                row.append(self._grid[x + 9 * y])
            self.rows.append(row)

        self.columns = []
        for x in range(9):
            column = []
            for y in range(9):
                column.append(self._grid[x + 9 * y])
            self.columns.append(column)

        self.blocks = []
        for i in range(9):
            block = []
            x_start = (i % 3) * 3
            y_start = (i // 3) * 3
            for x in range(x_start, x_start + 3):
                for y in range(y_start, y_start + 3):
                    block.append(self._grid[x+9*y])
            self.blocks.append(block)

    def place(self, value: int, x: int, y: int) -> None:
        """Place value at x,y."""
        self._grid[x + 9 * y][0] = value

    def unplace(self, x: int, y: int) -> None:
        """Remove (unplace) a number at x,y."""
        self._grid[x + 9 * y][0] = 0

    def value_at(self, x: int, y: int) -> int:
        """Returns the value at x,y."""
        value = -1
        if x < 9 and y < 9 and x >= 0 and y >= 0:
            value = self._grid[x + 9 * y][0]
        return value

    def options_at(self, x: int, y: int) -> Iterable[int]:
        """Returns all possible values (options) at x,y."""
        options = set([1, 2, 3, 4, 5, 6, 7, 8, 9])

        current_row = set(self.row_values(y))
        current_column = set(self.column_values(x))
        block_index = self.block_index_of(x, y)
        current_block = set(self.block_values(block_index))
        options = options - (current_row | current_column | current_block)

        return list(options)

    def next_empty_index(self) -> tuple[int, int]:
        """
        Returns the next index (x,y) that is empty (value 0).
        If there is no empty spot, returns (-1,-1)
        """
        next_x, next_y = -1, -1

        for y in range(9):
            for x in range(9):
                if self.value_at(x, y) == 0 and next_x == -1 and next_y == -1:
                    next_x, next_y = x, y
                    break
            else:
                continue  # only executed if the inner loop did NOT break
            break

        return next_x, next_y

    def row_values(self, i: int) -> Iterable[int]:
        """Returns all values at i-th row."""
        return sum(self.rows[i], [])

    def column_values(self, i: int) -> Iterable[int]:
        """Returns all values at i-th column."""
        return sum(self.columns[i], [])

    def block_values(self, i: int) -> Iterable[int]:
        """
        Returns all values at i-th block.
        The blocks are arranged as follows:
        0 1 2
        3 4 5
        6 7 8
        """
        return sum(self.blocks[i], [])

    def block_index_of(self, x: int, y: int) -> int:
        """Returns the index of a block from an index (x,y)."""
        return (y // 3) * 3 + x // 3

    def is_solved(self) -> bool:
        """
        Returns True if and only if all rows, columns and blocks contain
        only the numbers 1 through 9. False otherwise.
        """
        values = set([1, 2, 3, 4, 5, 6, 7, 8, 9])

        result = True

        for i in range(9):
            current_row = set(self.row_values(i))
            current_column = set(self.column_values(i))
            current_block = set(self.block_values(i))
            remainder_row = values - current_row
            remainder_column = values - current_column
            remainder_block = values - current_block

            if remainder_row | remainder_column | remainder_block:
                result = False
                break

        return result

    def __str__(self) -> str:
        representation = ""

        for i in range(9):
            row = sum(self.rows[i], [])
            row = "".join(str(e) for e in row)
            representation += row + "\n"

        return representation.strip()


def load_from_file(filename: str) -> Sudoku:
    """Load a Sudoku from filename."""
    puzzle: list[str] = []

    with open(filename) as f:
        for line in f:

            # strip newline and remove all commas
            line = line.strip().replace(",", "")

            puzzle.append(line)

    return Sudoku(puzzle)