"""Dungeon visualization - ASCII and graphical."""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.colors import ListedColormap


def print_dungeon(layout: np.ndarray) -> None:
    """ASCII render of the dungeon."""
    symbols = {0: '·', 1: '█'}
    rows, cols = layout.shape

    print("┌" + "──" * cols + "─┐")
    for row in range(rows):
        line = "│ "
        for col in range(cols):
            line += symbols[layout[row, col]] + " "
        line += "│"
        print(line)
    print("└" + "──" * cols + "─┘")


def print_dungeon_fancy(layout: np.ndarray, title: str = "QAOA Dungeon") -> None:
    """ASCII with entrance/exit markers."""
    rows, cols = layout.shape

    print(f"\n  {title}")
    print("  " + "─" * (cols * 2 + 1))

    top_rooms = np.where(layout[0] == 1)[0]
    entrance_col = int(top_rooms[0]) if len(top_rooms) > 0 else -1

    for row in range(rows):
        line = "  │"
        bottom_rooms = np.where(layout[row] == 1)[0] if row == rows - 1 else None
        exit_col = int(bottom_rooms[-1]) if bottom_rooms is not None and len(bottom_rooms) > 0 else -1

        for col in range(cols):
            if layout[row, col] == 1:
                if row == 0 and col == entrance_col:
                    line += "E "
                elif row == rows - 1 and col == exit_col:
                    line += "X "
                else:
                    line += "█ "
            else:
                line += "· "
        line += "│"
        print(line)

    print("  " + "─" * (cols * 2 + 1))


def plot_dungeon(layout: np.ndarray, title: str = "QAOA Dungeon", save_path: str = None, show: bool = True):
    """Matplotlib visualization of the dungeon."""
    rows, cols = layout.shape

    # Color scheme for room types
    colors = {
        0: '#1a1a2e',  # Empty
        1: '#4a4e69',  # Room
        2: '#22b573',  # Entrance (green)
        3: '#c9184a',  # Exit (red)
        4: '#f9c74f',  # Treasure (gold)
        5: '#7209b7',  # Enemy (purple)
        6: '#ff4d6d',  # Boss (bright red)
    }

    labels = {
        2: 'E',
        3: 'X',
        4: '$',
        5: '!',
        6: 'B',
    }

    # Create figure
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_facecolor('#1a1a2e')
    fig.patch.set_facecolor('#0f0f1a')

    # Draw cells
    for row in range(rows):
        for col in range(cols):
            val = layout[row, col]
            color = colors.get(val, '#1a1a2e')
            label = labels.get(val, '')

            rect = Rectangle((col, rows - 1 - row), 1, 1,
                             facecolor=color,
                             edgecolor='#ffffff' if val > 0 else '#333344',
                             linewidth=2 if val > 0 else 1)
            ax.add_patch(rect)

            if label:
                ax.text(col + 0.5, rows - 1 - row + 0.5, label,
                        ha='center', va='center', fontsize=20,
                        fontweight='bold', color='white')

    # Configure axes
    ax.set_xlim(0, cols)
    ax.set_ylim(0, rows)
    ax.set_aspect('equal')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(title, fontsize=18, fontweight='bold', color='white', pad=20)

    # Legend
    legend_elements = [
        Rectangle((0, 0), 1, 1, facecolor='#22b573', edgecolor='white', label='Entrance'),
        Rectangle((0, 0), 1, 1, facecolor='#ff4d6d', edgecolor='white', label='Boss'),
        Rectangle((0, 0), 1, 1, facecolor='#c9184a', edgecolor='white', label='Exit'),
        Rectangle((0, 0), 1, 1, facecolor='#f9c74f', edgecolor='white', label='Treasure'),
        Rectangle((0, 0), 1, 1, facecolor='#7209b7', edgecolor='white', label='Enemy'),
        Rectangle((0, 0), 1, 1, facecolor='#4a4e69', edgecolor='white', label='Room'),
    ]
    ax.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(1.02, 1),
              facecolor='#0f0f1a', edgecolor='#333344', labelcolor='white')

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight', facecolor='#0f0f1a', edgecolor='none')
        print(f"Dungeon saved: {save_path}")

    if show:
        plt.show()