from copy import deepcopy
from math import exp
from random import random
from scheduling.mapper import mapper
from scheduling.models.matrix import Matrix
from scheduling.models.schedule import Course, Schedule, Assignment
from scheduling.solver.checker import check_constraints, init_matrix
from scheduling.utils import insert_into_slice, is_all_zeros
from scheduling.logger import log_solution


def solve(schedule: Schedule) -> list[Assignment]:
    """Solves the given schedule and returns the list of solutions"""

    # Generate initial solution
    solution = generate_solution(schedule)
    # Apply simulated annealing
    solution = simulated_annealing(initial_solution = solution,
                                    max_iter = 100,
                                    max_perturb = 100,
                                    max_success = 100,
                                    alpha = 0.9,
                                    schedule = schedule)

    return mapper(schedule, solution)

def calculate_conflicts(course_tuple: tuple[int, Course], schedule: Schedule) -> int:
    """Calculates the number of conflicts for the given course"""
    course_index = course_tuple[0]
    course = course_tuple[1]

    n_curricula = sum(1 for curriculum in schedule.curricula if course.id in curriculum.members)
    return len(course.constraints) + course.n_lectures - course.min_working_days + n_curricula

def generate_solution(schedule: Schedule) -> Matrix:
    """Generates all possible solutions for the given schedule"""

    solution = init_matrix(schedule)

    # Set of all lectures to be assigned
    lectures = [course.n_lectures*[course_index] for course_index, course in \
                sorted(enumerate(schedule.courses), key = lambda x: calculate_conflicts(x, schedule), reverse=True)]
    lectures = [item for sublist in lectures for item in sublist]
    
    log_solution(solution)
    return solution

def simulated_annealing(initial_solution: Matrix,
                         max_iter: int,
                         max_perturb: int,
                         max_success:int,
                         alpha: float,
                         schedule: Schedule) -> Matrix:
    """Simulated Annealing algorithm"""
    solution = initial_solution
    temperature = initial_temperature()
    j = 1
    while True:
        i = 1
        success = 0
        while True:
            new_solution = perturb(solution)
            new_score = f(new_solution, schedule)
            old_score = f(solution, schedule)
            delta = new_score - old_score
            success_rate = delta < 0
            luck = random() < exp(-delta/temperature)
            if success_rate or luck:
                # print("luck" if luck else "success")
                solution = new_solution
                # print(f"Found better solution with fitness {old_score} -> {new_score}")
                # print(solution)
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
