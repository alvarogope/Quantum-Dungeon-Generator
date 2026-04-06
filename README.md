**PROJECT DESCRIPTION**

In this project I developed a Procedural Dungeon Generator powered by Quantum Computing using IBM's Qiskit framework.
The generator uses the Quantum Approximate Optimization Algorithm (QAOA) to find optimal room placements based on game design constraints.
Instead of traditional random generation, dungeon rules are encoded as a mathematical optimization problem that quantum circuits solve.

---

**ABOUT THE PROJECT**

By implementing QAOA, I encoded dungeon constraints as a Quadratic Unconstrained Binary Optimization (QUBO) problem. Each cell in the grid becomes a binary variable (room or empty), and the algorithm finds layouts that minimize a cost function representing "bad dungeon design."

The constraints I encoded include:
- Target number of rooms (penalizes having too many or too few)
- Connectivity reward (adjacent rooms get lower energy)
- Entrance placement (rooms in the top row are preferred)
- Exit placement (rooms in the bottom row are preferred)

After QAOA finds a valid layout, a post-processing step assigns room types: Entrance, Exit, Boss, Treasure, and Enemy rooms.

---

**TECH STACK:**

*Quantum Computing:*

Qiskit - IBM's open-source quantum computing SDK,

Qiskit-Aer - High-performance quantum circuit simulator,

Qiskit-Algorithms - Contains QAOA implementation,

Qiskit-Optimization - Tools for encoding QUBO problems.

*Visualization & Data:*

Matplotlib - For dungeon and circuit visualization,

NumPy - For grid operations and data handling.

*Development:*

Python 3.12,

PyCharm IDE.

---

**FEATURES:**

QAOA Solver - Uses quantum superposition to explore all possible dungeon layouts simultaneously.

QUBO Encoding - Translates game design rules into mathematical constraints.

Connectivity Validation - Ensures all rooms are connected using flood-fill algorithm.

Room Type Assignment - Automatically places Entrance, Exit, Boss, Treasure, and Enemy rooms.

Circuit Visualization - Displays the actual quantum circuit used for optimization.

Retry Logic - Regenerates if the dungeon is disconnected.

---

**PROJECT FILES EXPLANATION:**

*src/dungeon.py* - Contains the DungeonGrid class that represents the grid, handles coordinate conversion, neighbor detection, and connectivity checking. Also contains RoomType enum and the assign_room_types function for post-processing.

*src/quantum_core.py* - The core of the project. Contains QuantumDungeonSolver class that builds the QUBO problem, sets up QAOA with Qiskit, and runs the optimization. Also includes circuit visualization method.

*src/visualizer.py* - Handles all visualization: ASCII dungeon printing and Matplotlib graphical rendering with color-coded room types.

*main.py* - Entry point for portfolio showcase. Generates dungeons with professional console output and saves visualizations to the output folder.

*test_solver.py* - Development test file for running quick generations and debugging.

*requirements.txt* - Lists all Python dependencies needed to run the project.

---

**HOW QAOA WORKS:**

QAOA is a hybrid quantum-classical algorithm:

1. Hadamard gates create a superposition of ALL possible dungeon layouts at once.

2. Cost Layer applies the dungeon constraints (room count, connectivity, entrance/exit).

3. Mixer Layer allows the quantum state to explore different solutions.

4. Classical Optimizer (COBYLA) tunes the quantum circuit parameters.

5. Measurement collapses the superposition into a single dungeon layout.

The circuit looks like:

'''

|0⟩ ─[H]─[Cost]─[Mixer]─[Cost]─[Mixer]─[Measure]

|0⟩ ─[H]─[Cost]─[Mixer]─[Cost]─[Mixer]─[Measure]

'''

---

**ROOM TYPES:**

| Symbol | Type | Color | Description |
|--------|------|-------|-------------|
| E | Entrance | Green | Starting point, placed in top row |
| X | Exit | Red | Goal, placed in bottom row |
| B | Boss | Pink | Guardian room, adjacent to exit |
| $ | Treasure | Gold | Reward rooms |
| ! | Enemy | Purple | Combat encounters |

---

**CHALLENGES PROGRESS AND EVOLUTION:**

Firstly, I had to understand how QUBO encoding works. Translating "rooms should be connected" into mathematical penalties required learning about Ising Hamiltonians and quadratic cost functions.

The main challenge was balancing constraint weights. If the room count penalty was too high, QAOA would ignore connectivity. If connectivity reward was too strong, it would cluster all rooms together ignoring entrance/exit placement.

For larger grids (4x4 = 16 qubits), computation time increased significantly. I solved this by reducing QAOA repetitions and implementing retry logic instead of forcing perfect solutions.

I also learned that quantum algorithms are probabilistic - running the same code twice gives different results. This is actually a feature for procedural generation, as it creates variety.

---

**INSTALLATION:**
```bash
# Clone the repository
git clone https://github.com/alvarogope/Quantum-Dungeon-Generator.git
cd Quantum-Dungeon-Generator

# Create virtual environment
python -m venv venv
.\venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run the generator
python main.py
```

---

**EXAMPLE OUTPUT:**

╔══════════════════════════════════════════════════════════╗
║              QUANTUM DUNGEON GENERATOR                    ║
║         QAOA-Powered Procedural Generation                ║
╚══════════════════════════════════════════════════════════╝
Grid Size:     4x4
Target Rooms:  9
QAOA Depth:    1
──────────────────────────────────
Running QAOA optimization...
──────────────────────────────────
Attempt  1: Energy=   -434 | Rooms=9 | ✓ Connected
✓ SUCCESS after 1 attempt(s)

---

**REFERENCES:**

QAOA Paper - Farhi et al., 2014 (https://arxiv.org/abs/1411.4028)

Procedural Generation Using Quantum Computing - Wootton, 2020 (https://arxiv.org/abs/2007.11510)

IBM Qiskit Documentation (https://qiskit.org/)
