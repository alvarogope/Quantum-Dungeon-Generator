"""
Dungeon grid data structure.
Each cell can become a room - QAOA will decide which ones.
"""

from collections import deque
from dataclasses import dataclass
from enum import Enum
from typing import Tuple, List
import random

import numpy as np

class RoomType(Enum):
    EMPTY = 0
    ROOM = 1
    ENTRANCE = 2
    EXIT = 3
    TREASURE = 4
    ENEMY = 5
    BOSS = 6


@dataclass
class DungeonGrid:
    size: Tuple[int, int]
    target_rooms: int

    def __post_init__(self):
        self.rows, self.cols = self.size
        self.grid = np.zeros(self.size, dtype=int)

    @property
    def total_cells(self) -> int:
        return self.rows * self.cols

    def cell_to_index(self, row: int, col: int) -> int:
        return row * self.cols + col

    def index_to_cell(self, index: int) -> Tuple[int, int]:
        return index // self.cols, index % self.cols

    def get_neighbors(self, row: int, col: int) -> List[Tuple[int, int]]:
        neighbors = []
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = row + dr, col + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                neighbors.append((nr, nc))
        return neighbors

    def is_connected(self, layout: np.ndarray) -> bool:
        """Check if all rooms are connected using flood fill."""
        rooms = []
        for row in range(self.rows):
            for col in range(self.cols):
                if layout[row, col] == 1:
                    rooms.append((row, col))

        if len(rooms) <= 1:
            return True

        visited = set()
        queue = deque([rooms[0]])
        visited.add(rooms[0])

        while queue:
            row, col = queue.popleft()
            for nr, nc in self.get_neighbors(row, col):
                if (nr, nc) not in visited and layout[nr, nc] == 1:
                    visited.add((nr, nc))
                    queue.append((nr, nc))

        return len(visited) == len(rooms)

    def __str__(self) -> str:
        symbols = {0: '·', 1: '█'}
        lines = []
        for row in range(self.rows):
            line = ' '.join(symbols[self.grid[row, col]] for col in range(self.cols))
            lines.append(line)
        return '\n'.join(lines)


def assign_room_types(layout: np.ndarray) -> np.ndarray:
    """
    Assign room types to a generated layout.
    Boss room is placed adjacent to exit.
    """
    rows, cols = layout.shape
    typed_layout = np.zeros_like(layout)

    # Find all room positions
    rooms = []
    for row in range(rows):
        for col in range(cols):
            if layout[row, col] == 1:
                rooms.append((row, col))

    if not rooms:
        return typed_layout

    # Find entrance (first room in top row)
    entrance = None
    for col in range(cols):
        if layout[0, col] == 1:
            entrance = (0, col)
            break
    if not entrance:
        entrance = rooms[0]

    # Find exit (last room in bottom row)
    exit_room = None
    for col in range(cols - 1, -1, -1):
        if layout[rows - 1, col] == 1:
            exit_room = (rows - 1, col)
            break
    if not exit_room:
        exit_room = rooms[-1]

    # Find boss room (adjacent to exit, not entrance)
    boss_room = None
    exit_r, exit_c = exit_room
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = exit_r + dr, exit_c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            if layout[nr, nc] == 1 and (nr, nc) != entrance:
                boss_room = (nr, nc)
                break

    # Assign fixed rooms
    typed_layout[entrance] = RoomType.ENTRANCE.value
    typed_layout[exit_room] = RoomType.EXIT.value
    if boss_room:
        typed_layout[boss_room] = RoomType.BOSS.value

    # Get remaining rooms
    special_rooms = {entrance, exit_room}
    if boss_room:
        special_rooms.add(boss_room)
    normal_rooms = [r for r in rooms if r not in special_rooms]

    # Randomly assign treasure and enemies
    random.shuffle(normal_rooms)

    num_treasure = max(1, len(normal_rooms) // 4)
    num_enemies = max(1, len(normal_rooms) // 3)

    for i, room in enumerate(normal_rooms):
        if i < num_treasure:
            typed_layout[room] = RoomType.TREASURE.value
        elif i < num_treasure + num_enemies:
            typed_layout[room] = RoomType.ENEMY.value
        else:
            typed_layout[room] = RoomType.ROOM.value

    return typed_layout