from math import exp
from random import random
from scheduling.models.schedule import Schedule, Solution
from scheduling.solver.checker import check_constraints


def solve(schedule: Schedule) -> list[Solution]:
    """Solves the given schedule and returns the list of solutions"""

    solutions = generate_solutions(schedule)

    solutions = simulated_annealing(solutions, 100, 100, 100, 0.9)



    return solutions

def generate_solutions(schedule: Schedule) -> list[Solution]:
    """Generates all possible solutions for the given schedule"""

    solutions = []
    for course in schedule.courses:
        for room in schedule.rooms:
            if room.capacity >= course.n_students:
                for day in range(1, schedule.n_days + 1):
                    for period in range(1, schedule.n_periods + 1):
                        solutions.append(Solution(course.id, room.id, day, period))
                break

    return solutions

def simulated_annealing(initial_solution: list[Solution],
                         max_iter: int,
                         max_perturb: int,
                         max_success:int,
                         alpha: float ):
    """Simulated Annealing algorithm"""
    solution = initial_solution
    temperature = initial_temperature()
    j = 1
    while True:
        i = 1
        success = 0
        while True:
            new_solution = perturb(solution)
            delta = f(new_solution) - f(solution)
            if delta <= 0 or random() < exp(-delta/temperature):
                solution = new_solution
                success += 1
            i += 1
            if success >= max_success or i >= max_perturb:
                break
        temperature = alpha * temperature
        j += 1
        if success == 0 or j >= max_iter:
            break
    return solution

def initial_temperature():
    """Returns the initial temperature for the simulated annealing algorithm"""
    return 30

def perturb(solution: list[Solution]) -> list[Solution]:
    """Perturbs the given solution"""
    return solution

def f(solution: list[Solution]) -> int:
    """Returns the fitness of the given solution"""
    return check_constraints(solution)


"""
Pseudo-Código Simulated Annealing
Inicio
/* Entradas do Algoritmo */
Ler (S0, M, P, L, α)
/* Inicialização das variáveis */
S = S0
T0 = TempInicial()
T = T0
j = 1
/*Loop principal – Verifica se foram atendidas as condições de termino do algoritmo*/
Repita
i = 1
nSucesso = 0
/*Loop Interno – Realização de perturbação em uma iteração*/
Repita
Si = Perturba(S)
∆Fi = f(Si) – f(S)
/*Teste de aceitação de uma nova solução*/
Se (∆fi ≤ 0) ou (exp(-∆fi/T) > Randomiza()) então
S= Si
nSucesso = nSucesso + 1
Fim-se
i = i + 1
Até (nSucesso ≥ L) ou (i > P)
/*Actualização da Temperatura*/
T = α.T
/*Actualização do Contador de iterações*/
j = j + 1
Até (nSucesso = 0) ou (j > M)
/*Saída do Algoritmo*/
Imprima(S)
"""
