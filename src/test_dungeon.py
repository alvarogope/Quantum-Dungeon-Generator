"""Tests for the dungeon module."""

import numpy as np
import pytest
from src.dungeon import DungeonGrid, assign_room_types, RoomType


def test_grid_dimensions():
    dungeon = DungeonGrid(size=(4, 4), target_rooms=6)
    assert dungeon.rows == 4
    assert dungeon.cols == 4
    assert dungeon.total_cells == 16


def test_cell_index_roundtrip():
    dungeon = DungeonGrid(size=(4, 4), target_rooms=6)
    for row in range(dungeon.rows):
        for col in range(dungeon.cols):
            idx = dungeon.cell_to_index(row, col)
            assert dungeon.index_to_cell(idx) == (row, col)


def test_neighbors_corner():
    dungeon = DungeonGrid(size=(4, 4), target_rooms=6)
    neighbors = dungeon.get_neighbors(0, 0)
    assert set(neighbors) == {(1, 0), (0, 1)}


def test_neighbors_center():
    dungeon = DungeonGrid(size=(4, 4), target_rooms=6)
    neighbors = dungeon.get_neighbors(1, 1)
    assert set(neighbors) == {(0, 1), (2, 1), (1, 0), (1, 2)}


def test_is_connected_single_room():
    dungeon = DungeonGrid(size=(3, 3), target_rooms=1)
    layout = np.zeros((3, 3), dtype=int)
    layout[1, 1] = 1
    assert dungeon.is_connected(layout)


def test_is_connected_true():
    dungeon = DungeonGrid(size=(3, 3), target_rooms=3)
    layout = np.array([[1, 1, 0], [0, 1, 0], [0, 0, 0]])
    assert dungeon.is_connected(layout)


def test_is_connected_false():
    dungeon = DungeonGrid(size=(3, 3), target_rooms=2)
    layout = np.array([[1, 0, 1], [0, 0, 0], [0, 0, 0]])
    assert not dungeon.is_connected(layout)


def test_assign_room_types_has_entrance_and_exit():
    layout = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    typed = assign_room_types(layout)
    assert RoomType.ENTRANCE.value in typed
    assert RoomType.EXIT.value in typed


def test_assign_room_types_no_rooms():
    layout = np.zeros((3, 3), dtype=int)
    typed = assign_room_types(layout)
    assert typed.sum() == 0
