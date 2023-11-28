from copy import copy, deepcopy
from math import exp
from random import random
import time
from scheduling.mapper import mapper
from scheduling.models.matrix import Matrix
from scheduling.models.schedule import Course, Schedule, Assignment
from scheduling.solver.checker import check_constraints, init_matrix
from scheduling.solver.generate_solution import generate_solution
from scheduling.utils import insert_into_slice, is_all_zeros
from scheduling.logger import log_solution


def solve(schedule: Schedule) -> list[Assignment]:
    """Solves the given schedule and returns the list of solutions"""

    # Generate initial solution
    solution = generate_solution(schedule)
    # Apply simulated annealing
    solution = simulated_annealing(initial_solution = solution,
                                    schedule = schedule,
                                    max_iter = 100,
                                    max_perturb = 100,
                                    max_success = 100,
                                    alpha = 0.9,
                                    time_limit = 1000)

    return mapper(schedule, solution)

def simulated_annealing(initial_solution: Matrix,
                        schedule: Schedule,
                         max_iter: int,
                         max_perturb: int,
                         max_success:int,
                         alpha: float,
                         time_limit: int = 1000) -> Matrix:
    solution = initial_solution
    temperature = initial_temperature()
    j = 1
    start = time.time()
    while time_limit > time.time() - start:
        i = 1
        success = 0
        while time_limit > time.time() - start:
            new_solution = perturb(solution)
            new_score = f(new_solution, schedule)
            old_score = f(solution, schedule)
            delta = new_score - old_score
            success_rate = delta < 0
            luck = random() < exp(-delta/temperature)
            if success_rate or luck:
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

def perturb(solution: Matrix) -> Matrix:
    """Perturbs the given solution"""
    new_solution = deepcopy(solution)

    # Select a random room and them find another random room
    room1 = int(random() * len(solution))
    room2 = int(random() * len(solution))

    # Select a random day period that is not -1 (no lecture) and them find another random day period that is -1
    day_period1 = int(random() * len(solution[0]))
    day_period2 = int(random() * len(solution[0]))

    # Swap the lectures
    new_solution[room1][day_period1], new_solution[room2][day_period2] = \
        new_solution[room2][day_period2], new_solution[room1][day_period1]

    log_solution(new_solution)
    return new_solution

def f(solution: Matrix, schedule: Schedule) -> int:
    """Returns the fitness of the given solution"""
    return check_constraints(solution, schedule)
