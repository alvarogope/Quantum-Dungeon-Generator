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

![Architecture](https://img.shields.io/badge/Flow-Dungeon→QUBO→QAOA→Layout→Visualizer-blue?style=for-the-badge)

| Component | Role | Output |
|-----------|------|--------|
| 🎮 **DungeonGrid** | Defines grid size, target rooms, neighbor relationships | Constraint parameters |
| 🧮 **QUBO Builder** | Encodes room count penalty, connectivity reward, entrance/exit preference | Cost function |
| ⚛️ **QAOA Circuit** | Quantum superposition + cost/mixer layers | Parameterized circuit |
| 🔧 **COBYLA Optimizer** | Classical tuning of quantum parameters γ, β | Optimal angles |
| 📏 **Measurement** | Collapses quantum state to classical bitstring | Binary room layout |
| ✅ **Connectivity Check** | Validates all rooms are reachable via flood-fill | Pass/retry |
| 🏰 **Room Assigner** | Places Entrance, Exit, Boss, Treasure, Enemy | Typed layout |
| 🎨 **Visualizer** | Renders ASCII and Matplotlib graphics | PNG output |

---

## 🗂️ Project Structure

| File | Description |
|------|-------------|
| 📁 `src/` | |
| ├── `dungeon.py` | DungeonGrid class, RoomType enum, connectivity check, room assignment |
| ├── `quantum_core.py` | QuantumDungeonSolver, QUBO builder, QAOA runner |
| ├── `visualizer.py` | print_dungeon(), plot_dungeon(), color schemes |
| └── `__init__.py` | Package exports |
| 📁 `output/` | Generated dungeon images (.png) |
| `main.py` | Entry point with formatted console output |
| `test_solver.py` | Quick testing and debugging |
| `requirements.txt` | Qiskit, NumPy, Matplotlib |
| `README.md` | Documentation |
| `.gitignore` | Excludes venv, __pycache__, output images |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
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

| Step | Operation | Description |
|------|-----------|-------------|
| 1 | **Hadamard (H)** | Creates superposition of all 2^n possible dungeon layouts |
| 2 | **Cost Layer U(γ,C)** | Applies dungeon constraints as phase rotations |
| 3 | **Mixer Layer U(β,B)** | Enables exploration of the solution space |
| 4 | **Repeat** | Multiple cost-mixer layers improve solution quality |
| 5 | **COBYLA Optimizer** | Classical optimizer tunes γ, β parameters to minimize cost |
| 6 | **Measurement** | Collapses superposition to optimal dungeon layout |

**Circuit:** `|0⟩ → [H] → [Cost] → [Mixer] → [Cost] → [Mixer] → [Measure]`

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

**Generated Dungeon:**

| | | | | Legend |
|:-:|:-:|:-:|:-:|:--|
| E | ■ | ■ | · | **E** = Entrance |
| ■ | ■ | · | · | **■** = Room |
| ! | ■ | $ | · | **!** = Enemy |
| · | B | X | · | **$** = Treasure |
| | | | | **B** = Boss |
| | | | | **X** = Exit |
