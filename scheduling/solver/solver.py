from math import exp
from random import random
from scheduling.mapper import mapper
from scheduling.models.schedule import Schedule, Assignment
from scheduling.solver.checker import Matrix, check_constraints, init_matrix
from scheduling.utils import insert_into_slice, is_all_zeros


def solve(schedule: Schedule) -> list[Assignment]:
    """Solves the given schedule and returns the list of solutions"""

    # Generate initial solution
    solution = generate_solution(schedule)
    # Apply simulated annealing
    solution = simulated_annealing(solution, 100, 100, 100, 0.9, schedule)

    return mapper(schedule, solution)

def generate_solution(schedule: Schedule) -> Matrix:
    """Generates all possible solutions for the given schedule"""

    solution = init_matrix(schedule)

    sorted_rooms = sorted(schedule.rooms, key=lambda x: x.capacity)

    for course_index, course in enumerate(schedule.courses):
        found = False
        for room in filter(lambda x: x.capacity >= course.n_students, sorted_rooms):
            if found: break
            room_index = schedule.rooms.index(room)
            for day_period in range(schedule.n_days*schedule.n_periods):
                if is_all_zeros(solution[room_index][day_period:day_period+course.n_lectures]) \
                    and day_period + course.n_lectures <= schedule.n_days*schedule.n_periods:
                    found = True
                    insert_into_slice(solution[room_index], day_period, course.n_lectures, course_index)
                    break

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
            delta = f(new_solution, schedule) - f(solution, schedule)
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

def perturb(solution: Matrix) -> Matrix:
    """Perturbs the given solution"""
    return solution

def f(solution: Matrix, schedule: Schedule) -> int:
    """Returns the fitness of the given solution"""
    return check_constraints(solution, schedule)
