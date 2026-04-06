"""
QAOA solver for dungeon generation.
Encodes dungeon constraints as a QUBO problem.
"""

from dataclasses import dataclass
from typing import Any
import numpy as np

from qiskit_optimization import QuadraticProgram
from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit_algorithms import QAOA
from qiskit_algorithms.optimizers import COBYLA
from qiskit.primitives import StatevectorSampler


@dataclass
class SolverResult:
    best_energy: float
    room_layout: np.ndarray
    raw_result: Any


class QuantumDungeonSolver:
    def __init__(self, dungeon, qaoa_reps: int = 2, seed: int = 42):
        self.dungeon = dungeon
        self.qaoa_reps = qaoa_reps
        self.seed = seed
        self.num_cells = dungeon.rows * dungeon.cols

    def _build_qubo(self) -> QuadraticProgram:
        qp = QuadraticProgram("dungeon")

        for i in range(self.num_cells):
            qp.binary_var(f"x_{i}")

        target = self.dungeon.target_rooms
        penalty = 10.0

        linear = {}
        quadratic = {}

        # CONSTRAINT 1: Target room count
        for i in range(self.num_cells):
            linear[f"x_{i}"] = -2 * target * penalty + penalty

        for i in range(self.num_cells):
            for j in range(i + 1, self.num_cells):
                quadratic[(f"x_{i}", f"x_{j}")] = 2 * penalty

        # CONSTRAINT 2: Reward connectivity
        connectivity_reward = -8.0

        for i in range(self.num_cells):
            row, col = self.dungeon.index_to_cell(i)
            for nr, nc in self.dungeon.get_neighbors(row, col):
                j = self.dungeon.cell_to_index(nr, nc)
                if i < j:
                    key = (f"x_{i}", f"x_{j}")
                    quadratic[key] = quadratic.get(key, 0) + connectivity_reward

        # CONSTRAINT 3: Entrance (top row) and Exit (bottom row)
        entrance_reward = -5.0  # Strong reward for rooms in first row
        exit_reward = -5.0  # Strong reward for rooms in last row

        # Top row - entrance zone
        for col in range(self.dungeon.cols):
            i = self.dungeon.cell_to_index(0, col)
            linear[f"x_{i}"] += entrance_reward

        # Bottom row - exit zone
        for col in range(self.dungeon.cols):
            i = self.dungeon.cell_to_index(self.dungeon.rows - 1, col)
            linear[f"x_{i}"] += exit_reward

        qp.minimize(linear=linear, quadratic=quadratic)
        return qp

    def solve(self) -> SolverResult:
        qp = self._build_qubo()

        np.random.seed(self.seed)
        sampler = StatevectorSampler(seed=self.seed)
        optimizer = COBYLA(maxiter=100)
        initial_point = np.full(2 * self.qaoa_reps, np.pi / 4)
        qaoa = QAOA(sampler=sampler, optimizer=optimizer, reps=self.qaoa_reps, initial_point=initial_point)

        solver = MinimumEigenOptimizer(qaoa)
        result = solver.solve(qp)

        layout = np.array([
            int(result.variables_dict[f"x_{i}"])
            for i in range(self.num_cells)
        ])
        layout = layout.reshape((self.dungeon.rows, self.dungeon.cols))

        return SolverResult(
            best_energy=result.fval,
            room_layout=layout,
            raw_result=result
        )

    def get_circuit_diagram(self, save_path: str = None):
        """Visualize the QAOA circuit."""
        from qiskit.circuit.library import QAOAAnsatz
        from qiskit_optimization.converters import QuadraticProgramToQubo

        qp = self._build_qubo()

        # Convert to Ising Hamiltonian
        converter = QuadraticProgramToQubo()
        qubo = converter.convert(qp)

        # Get the operator
        operator, offset = qubo.to_ising()

        # Build QAOA circuit
        ansatz = QAOAAnsatz(operator, reps=self.qaoa_reps)

        # Draw circuit
        fig = ansatz.decompose().draw('mpl', style='iqp', fold=80)

        if save_path:
            fig.savefig(save_path, dpi=150, bbox_inches='tight', facecolor='white')
            print(f"Circuit saved: {save_path}")

        return fig