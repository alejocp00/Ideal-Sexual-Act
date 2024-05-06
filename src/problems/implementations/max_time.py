from pulp import LpProblem, LpVariable, lpSum, LpMaximize
from src.problems.abstract_problem import AbstractProblem
from src.entities.people import People
from src.entities.sexual_position import SexualPosition

"""
User
El objetivo del trabajo, es dadas unas posturas sexuales, y unas personas, donde se conoce el placer que brinda cada postura a cada persona, y la energía que les cuesta la postura, buscar resolver ciertos problemas.

Los datos serían

J = Cojunto de participantes (donde Ji es el participante i-ésimo)
N = Conjunto de posutras (Ni postura i-ésima)
Aij = Energía de la persona j al terminar la postura i para todo i desde 1 hasta |N|
Pij = Placer de la persona j al terminar la postura i, i desde 1 hasta |N|
PTj = Placer necesario para el orgasmo de la persona j
Ti = tiempo empleado en la postura i
Cij = Cantidad de energía que consume la postura i al participante j por unidad de tiempo
Paij = Placer que otorga la postura i al participante j por unidad de tiempo
Xi = Tiempo empleado en la ostura i
Ppak = Placer inicial del participante k, k partenece a J
E0j = Energía inicial del participante j

Restricciones comunes:

- Después de cada postura, la energía dismunuye de manera proporcional al tiempo que se permanezca en ella: Aij = A(i-1) - CijXi para todo i que pertence a N y para toda j que pertence a J

- Después de cada postura, el placer de cada participante aumenta de manera proporcional al tiempo que permanezca en ella: Pij = P(i-1)j + PijXi para todo i que pertence a N y para toda j que pertence a J


- En todo momento la energía es mayor igual que cero: Aij >= 0 para todo i que pertence a N y para toda j que pertence a J

- El placer después del acto sexual es mayor o igual al placer necesario para alcanzar el orgasmo: Pnj >=PTj para todo j que pertenece a J

Problema 1

Encontrar el tiempo que se debe estar en cada postura para que el tiempo del acto sexual sea el mayor posible, resolviendo el problema de: $max(\sum_{i}^{n}Xi$ sujeto a las 4 restricciones antes puestas

"""


class MaxTime(AbstractProblem):
    def __init__(self, peoples: list[People], positions: list[SexualPosition]):
        super().__init__(peoples, positions)

    def objective_function(self):
        return lpSum([self.X[i] for i in range(len(self.N))])

    def constraints(self):
        constraints = []

        # Después de cada postura, la energía dismunuye de manera proporcional al tiempo que se permanezca en ella
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
