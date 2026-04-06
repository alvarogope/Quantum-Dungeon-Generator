"""
╔═══════════════════════════════════════════════════════════════════╗
║         QUANTUM DUNGEON GENERATOR                                  ║
║         QAOA-Powered Procedural Content Generation                 ║
║                                                                    ║
║         Author: [Your Name]                                        ║
║         Built with: IBM Qiskit                                     ║
╚═══════════════════════════════════════════════════════════════════╝

This project uses the Quantum Approximate Optimization Algorithm (QAOA)
to generate dungeon layouts by encoding game design constraints as a
Quadratic Unconstrained Binary Optimization (QUBO) problem.

Constraints encoded:
  - Target room count
  - Room connectivity (adjacent rooms rewarded)
  - Entrance at top row
  - Exit at bottom row

Room types assigned post-generation:
  - Entrance (E) - Starting point
  - Exit (X) - Goal
  - Boss (B) - Adjacent to exit
  - Treasure ($) - Rewards
  - Enemy (!) - Encounters
"""

import os
from datetime import datetime
from src.dungeon import DungeonGrid, assign_room_types
from src.quantum_core import QuantumDungeonSolver
from src.visualizer import plot_dungeon
import matplotlib.pyplot as plt


def generate_dungeon(
        size: tuple = (4, 4),
        target_rooms: int = 9,
        qaoa_reps: int = 1,
        max_attempts: int = 10,
        output_dir: str = "output"
):
    """
    Generate a quantum dungeon and save visualizations.

    Args:
        size: Grid dimensions (rows, cols)
        target_rooms: Desired number of rooms
        qaoa_reps: QAOA circuit depth (higher = better but slower)
        max_attempts: Max retries for connected dungeon
        output_dir: Directory for output files

    Returns:
        SolverResult with the generated dungeon
    """
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Header
    print("╔" + "═" * 58 + "╗")
    print("║" + "QUANTUM DUNGEON GENERATOR".center(58) + "║")
    print("║" + "QAOA-Powered Procedural Generation".center(58) + "║")
    print("╚" + "═" * 58 + "╝")
    print()

    # Setup
    dungeon = DungeonGrid(size=size, target_rooms=target_rooms)

    print(f"  Grid Size:     {size[0]}x{size[1]}")
    print(f"  Total Cells:   {dungeon.total_cells}")
    print(f"  Target Rooms:  {target_rooms}")
    print(f"  QAOA Depth:    {qaoa_reps}")
    print(f"  Max Attempts:  {max_attempts}")
    print()
    print("  " + "─" * 40)
    print("  Running QAOA optimization...")
    print("  " + "─" * 40)

    # Generate
    result = None
    solver = None
    connected = False

    for attempt in range(1, max_attempts + 1):
        solver = QuantumDungeonSolver(dungeon, qaoa_reps=qaoa_reps, seed=attempt)
        result = solver.solve()

        connected = dungeon.is_connected(result.room_layout)
        status = "✓ Connected" if connected else "✗ Disconnected"

        print(f"  Attempt {attempt:2d}: Energy={result.best_energy:7.0f} | Rooms={result.room_layout.sum()} | {status}")

        if connected:
            break

    print("  " + "─" * 40)

    if connected:
        print(f"  ✓ SUCCESS after {attempt} attempt(s)")
    else:
        print(f"  ✗ FAILED after {max_attempts} attempts")
        print("    Try increasing connectivity_reward in quantum_core.py")

    print()

    # Assign room types
    typed_layout = assign_room_types(result.room_layout)

    # Save dungeon visualization
    dungeon_path = os.path.join(output_dir, f"dungeon_{timestamp}.png")
    plot_dungeon(
        typed_layout,
        title=f"Quantum Dungeon ({size[0]}x{size[1]}) | Energy: {result.best_energy:.0f}",
        save_path=dungeon_path,
        show=False,
    )

    # Save circuit diagram
    print("  Generating QAOA circuit diagram...")
    circuit_path = os.path.join(output_dir, f"circuit_{timestamp}.png")
    if solver is not None:
        try:
            solver.get_circuit_diagram(save_path=circuit_path)
        except Exception as e:
            print(f"  Warning: Could not generate circuit diagram: {e}")

    print()
    print(f"  Output saved to: {output_dir}/")
    print()

    return result, typed_layout


def showcase_multiple(count: int = 3):
    """Generate multiple dungeons to showcase variety."""
    print("\n" + "=" * 60)
    print("GENERATING MULTIPLE DUNGEONS FOR PORTFOLIO")
    print("=" * 60 + "\n")

    configs = [
        {"size": (3, 3), "target_rooms": 5, "name": "Small"},
        {"size": (4, 4), "target_rooms": 8, "name": "Medium"},
        {"size": (4, 4), "target_rooms": 12, "name": "Dense"},
    ]

    for i, config in enumerate(configs[:count]):
        print(f"\n>>> Dungeon {i + 1}: {config['name']} ({config['size'][0]}x{config['size'][1]})\n")
        generate_dungeon(
            size=config["size"],
            target_rooms=config["target_rooms"],
            output_dir=f"output/{config['name'].lower()}"
        )


if __name__ == "__main__":
    # Single dungeon generation
    generate_dungeon(
        size=(4, 4),
        target_rooms=9,
        qaoa_reps=1,
        max_attempts=10
    )