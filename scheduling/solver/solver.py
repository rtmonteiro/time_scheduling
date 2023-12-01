from copy import deepcopy
import logging
from math import exp
from random import random
from time import time
from scheduling.mapper import mapper
from scheduling.models.matrix import Matrix
from scheduling.models.params import Params
from scheduling.models.schedule import Schedule, Assignment
from scheduling.results import Results
from scheduling.solver.checker import check_constraints
from scheduling.solver.generate_solution import generate_solution


def solve(schedule: Schedule, params: Params) -> list[Assignment]:
    """Solves the given schedule and returns the list of solutions"""

    # Generate initial solution
    logging.info("Generating first solution")
    solution = generate_solution(schedule)
    # Apply simulated annealing
    logging.info("Starting solving with metaheuristic")
    solution = simulated_annealing(
        initial_solution=solution,
        schedule=schedule,
        max_iter=params.max_iter,
        max_perturb=params.max_perturb,
        max_success=params.max_success,
        alpha=params.alpha,
        max_time=params.max_time,
    )

    return mapper(schedule, solution)


def simulated_annealing(
    initial_solution: Matrix,
    schedule: Schedule,
    max_iter: int,
    max_perturb: int,
    max_success: int,
    alpha: float,
    max_time: int = 1000,
) -> Matrix:
    """
    Applies the simulated annealing algorithm to find an optimal solution for the given problem.

    Args:
        initial_solution (Matrix): The initial solution for the problem.
        schedule (Schedule): The schedule for the problem.
        max_iter (int): The maximum number of iterations.
        max_perturb (int): The maximum number of perturbations per iteration.
        max_success (int): The maximum number of successful perturbations per iteration.
        alpha (float): The cooling rate for the temperature.
        time_limit (int, optional): The maximum time limit in milliseconds. Defaults to 1000.

    Returns:
        Matrix: The optimal solution found by the algorithm.
    """
    solution = initial_solution
    temperature = initial_temperature()
    j = 1
    start = time()
    while max_time > time() - start:
        i = 1
        success = 0
        while max_time > time() - start:
            new_solution = perturb(solution)
            new_score = f(new_solution, schedule)
            old_score = f(solution, schedule)
            delta = new_score - old_score
            success_rate = delta < 0
            try :
                luck = random() < exp(-delta / temperature)
            except OverflowError:
                luck = False
            if success_rate or luck:
                Results().addResult((j, i, temperature, new_score))
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


def initial_temperature() -> float:
    """Returns the initial temperature for the simulated annealing algorithm"""
    return 30.0


def perturb(solution: Matrix) -> Matrix:
    """Perturbs the given solution"""
    new_solution = deepcopy(solution)

    # Select a random room and them find another random room
    room1 = int(random() * len(solution))
    room2 = int(random() * len(solution))

    # Try to find a random day period that is not -1 (no lecture) in 10 attempts
    # and them find another random day period
    day_period1 = int(random() * len(solution[0]))
    counter = 0
    while solution[room1][day_period1] == -1 and counter < 10:
        counter += 1
        day_period1 = int(random() * len(solution[0]))
    day_period2 = int(random() * len(solution[0]))

    # Swap the lectures
    new_solution[room1][day_period1], new_solution[room2][day_period2] = (
        new_solution[room2][day_period2],
        new_solution[room1][day_period1],
    )
    return new_solution


def f(solution: Matrix, schedule: Schedule) -> int:
    """Returns the fitness of the given solution"""
    return check_constraints(solution, schedule)
