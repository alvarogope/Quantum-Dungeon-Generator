# Quantum Dungeon Generator

[![Qiskit](https://img.shields.io/badge/Qiskit-6929C4?style=flat&logo=qiskit&logoColor=white)](https://qiskit.org/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)](https://python.org/)
[![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat&logo=numpy&logoColor=white)](https://numpy.org/)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-11557c?style=flat&logo=python&logoColor=white)](https://matplotlib.org/)

A procedural dungeon generator powered by Quantum Computing. Instead of traditional random generation, dungeon layout constraints are encoded as a Quadratic Unconstrained Binary Optimization (QUBO) problem and solved using the Quantum Approximate Optimization Algorithm (QAOA). Each cell becomes a qubit, and the quantum circuit explores all possible layouts simultaneously before collapsing to an optimal solution.

---

## ✨ Features

* ⚛️ **QAOA Solver** — Uses quantum superposition to explore all possible dungeon layouts simultaneously, finding optimal room placements
* 🧮 **QUBO Encoding** — Translates game design rules (room count, connectivity, entrance/exit) into mathematical constraints
* 🔗 **Connectivity Validation** — Flood-fill algorithm ensures all rooms are reachable; disconnected dungeons are rejected and regenerated
* 🏰 **Room Type Assignment** — Automatically places Entrance, Exit, Boss, Treasure, and Enemy rooms based on layout topology
* 📊 **Circuit Visualization** — Displays the actual quantum circuit used for optimization
* 🔄 **Retry Logic** — Regenerates layouts until a fully connected dungeon is found

---

## 🏗️ Architecture

┌─────────────────────┐         ┌──────────────────────┐
│   DungeonGrid       │ ──────▶ │   QuantumSolver      │
│   (constraints)     │         │   (QAOA circuit)     │
└─────────────────────┘         └──────────┬───────────┘
│
┌─────────────────┼──────────────────┐
▼                 ▼                  ▼
QUBO Problem      StatevectorSampler    COBYLA
(cost function)      (quantum sim)      (optimizer)
│                 │                  │
└─────────────────┼──────────────────┘
▼
Room Layout
(binary grid)
│
┌─────────────────┼──────────────────┐
▼                 ▼                  ▼
Connectivity       Room Types          Visualizer
Validation        Assignment          (Matplotlib)

---

## 🗂️ Project Structure

quantum-dungeon-generator/
├── src/
│   ├── dungeon.py          # Grid data structure, connectivity check, room type assignment
│   ├── quantum_core.py     # QAOA solver — QUBO encoding, circuit construction, optimization
│   ├── visualizer.py       # ASCII and Matplotlib dungeon rendering
│   └── init.py         # Package exports
├── output/                  # Generated dungeon images
├── main.py                  # Entry point — portfolio showcase with formatted output
├── test_solver.py           # Development testing
├── requirements.txt         # Python dependencies

---

## 🛠️ Tech Stack

| Layer | Technology |
| --- | --- |
| Quantum Computing | Qiskit, Qiskit-Aer, Qiskit-Algorithms, Qiskit-Optimization |
| Optimization | QAOA (Quantum Approximate Optimization Algorithm), COBYLA |
| Data | NumPy |
| Visualization | Matplotlib |
| Language | Python 3.12 |

---

## 🎮 Room Types

| Symbol | Type | Color | Description |
|--------|------|-------|-------------|
| E | Entrance | 🟢 Green | Starting point, placed in top row |
| X | Exit | 🔴 Red | Goal, placed in bottom row |
| B | Boss | 🩷 Pink | Guardian room, adjacent to exit |
| $ | Treasure | 🟡 Gold | Reward rooms |
| ! | Enemy | 🟣 Purple | Combat encounters |

---

## ⚙️ How QAOA Works

|0⟩ ─[H]─[U(γ,C)]─[U(β,B)]─[U(γ,C)]─[U(β,B)]─[Measure]
|0⟩ ─[H]─[U(γ,C)]─[U(β,B)]─[U(γ,C)]─[U(β,B)]─[Measure]
...      Cost      Mixer     Cost      Mixer

1. **Hadamard (H)** — Creates superposition of all 2^n possible dungeon layouts
2. **Cost Layer U(γ,C)** — Applies dungeon constraints as phase rotations
3. **Mixer Layer U(β,B)** — Enables exploration of the solution space
4. **Classical Optimizer** — Tunes γ, β parameters to minimize cost
5. **Measurement** — Collapses superposition to optimal layout

---

## 🚀 Installation
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

## 📸 Example Output

╔══════════════════════════════════════════════════════════╗
║              QUANTUM DUNGEON GENERATOR                    ║
║         QAOA-Powered Procedural Generation                ║
╚══════════════════════════════════════════════════════════╝
Grid Size:     4x4
Target Rooms:  9
QAOA Depth:    1
────────────────────────────────────────
Running QAOA optimization...
────────────────────────────────────────
Attempt  1: Energy=   -434 | Rooms=9 | ✓ Connected
✓ SUCCESS after 1 attempt(s)
