# Here will be placed a class to solve linear programming problems
# using the simplex method
from src.entities.people import People
from src.entities.sexual_position import SexualPosition
from pulp import LpProblem, LpVariable, lpSum, LpMaximize


class ProblemsTypes:
    MAX_TIME = "Maximizar la duración del acto sexual."
    MAX_MIN_PLEASURE = (
        "Maximizar el placer del que menor placer alcance al finalizar el acto sexual."
    )
    MINIMIZE_MAX_TIRED = "Minimizar el cansancio del participante con mayor cansancio al finalizar el acto sexual"
    MINIMIZE_INITIAL_ENERGY = "Minimizar la energía inicial de todos los participantes de forma que al terminar todos hayan alcanzado el orgasmo y tengan la misma energía"
    MAX_INITIAL_PLEASURE = "Maximizar el placer inicial de un participante específico, de forma tal que todos los participantes, excepto el específico, alcancen el orgasmo."


class AbstractProblem:
    def __init__(self, peoples: list[People], positions: list[SexualPosition]):
        self.J = peoples
        self.N = positions
        self.P_t = [people.orgasm_pleasure for people in peoples]
        self.C = self._build_C()
        self.Pa = self._build_P()

    def _build_C(self) -> list[list[int]]:
        C = [[0 for _ in range(len(self.J))] for _ in range(len(self.N))]

        for i, position in enumerate(self.N):
            for j, people in enumerate(self.J):
                C[i][j] = people.get_hardness_of_position(position.name)

        return C

    def _build_P(self) -> list[list[int]]:
        P = [[0 for _ in range(len(self.J))] for _ in range(len(self.N))]

        for i, position in enumerate(self.N):
            for j, people in enumerate(self.J):
                P[i][j] = people.get_pleasure_of_position(position.name)

        return P

    def objective_function(self):
        """
        The objective function of the problem to solve
        """
        raise NotImplementedError("objective_function method must be implemented")

    def constraints(self):
        """
        The constraints of the problem to solve
        """
        raise NotImplementedError("constraints method must be implemented")

    def solve(self):
        """
        Solve the problem
        """
        raise NotImplementedError("solve method must be implemented")
