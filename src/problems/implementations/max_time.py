from typing import List
from pulp import LpProblem, LpVariable, lpSum, LpMaximize
from src.problems.abstract_problem import AbstractProblem
from src.entities.people import People
from src.entities.sexual_position import SexualPosition


class MaxTime(AbstractProblem):
    def __init__(self, peoples: List[People], positions: List[SexualPosition]):
        super().__init__(peoples, positions)

    def objective_function(self):
        return lpSum([self.X[i] for i in range(len(self.N))])

    def constraints(self):
        constraints = []

        # Después de cada postura, la energía disminuye de manera proporcional al tiempo que se permanezca en ella
        for i in range(1, len(self.N)):
            for j in range(len(self.J)):
                constraints.append(
                    self.A[i][j] == self.A[i - 1][j] - self.C[i][j] * self.X[i]
                )

        # Después de cada postura, el placer de cada participante aumenta de manera proporcional al tiempo que permanezca en ella
        for i in range(1, len(self.N)):
            for j in range(len(self.J)):
                constraints.append(
                    self.P[i][j] == self.P[i - 1][j] + self.Pa[i][j] * self.X[i]
                )

        # En todo momento la energía es mayor igual que cero
        for i in range(len(self.N)):
            for j in range(len(self.J)):
                constraints.append(self.A[i][j] >= 0)

        # El placer después del acto sexual es mayor o igual al placer necesario para alcanzar el orgasmo
        for j in range(len(self.J)):
            constraints.append(self.P[-1][j] >= self.P_t[j])

        return constraints

    def solve(self):
        problem = LpProblem("MaxTime", LpMaximize)
        self.X = [LpVariable(f"X{i}", lowBound=0) for i in range(len(self.N))]

        self.A = [
            [LpVariable(f"A{i}{j}", lowBound=0) for j in range(len(self.J))]
            for i in range(len(self.N))
        ]
        self.P = [
            [LpVariable(f"P{i}{j}", lowBound=0) for j in range(len(self.J))]
            for i in range(len(self.N))
        ]

        problem += self.objective_function()

        for constraint in self.constraints():
            problem += constraint

        solution = problem.solve()

        return solution
