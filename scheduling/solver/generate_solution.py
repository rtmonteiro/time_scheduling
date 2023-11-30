from copy import copy
from math import sqrt
from functools import reduce
from scheduling.models.conflict import CourseData
from scheduling.models.matrix import Matrix
from scheduling.models.schedule import Course, Schedule
import numpy as np

def calculate_nhv(course_index: int, schedule: Schedule, solution: Matrix) -> int:
    """Calculates the number of periods available for the given course"""

    periods_available = range(schedule.n_days * schedule.n_periods * schedule.rooms_size)

    course = schedule.courses[course_index]

    # remove the periods that is in a room with less capacity than the course
    periods_available = [period for period in periods_available \
                            if course.n_students <= schedule.rooms[period // (schedule.n_days * schedule.n_periods)].capacity]

    # remove the periods that is already allocated
    periods_available = [period for period in periods_available \
                         if solution[period // (schedule.n_days * schedule.n_periods)]\
                            [period % (schedule.n_days * schedule.n_periods)] == -1]
    
    # remove the periods that are in the course constraints
    periods_available = [period for period in periods_available \
                            if not any(constraint.day == period % schedule.n_periods \
                                        and constraint.day_period == period // schedule.n_periods \
                                        for constraint in course.constraints)]
    
    # remove the periods that have lectures of courses in the same curriculum
    # find the curriculum that has the course, and then take the course from the members, and then put in a set to remove duplicates
    other_courses_same_curriculum = set([copy(curriculum.members).pop(curriculum.members.index(course.id)) \
                                        for curriculum in schedule.curricula if course.id in curriculum.members ])
    courses_indices = [schedule.courses.index(course) for course in other_courses_same_curriculum]
    periods_available = [period for period in periods_available \
                            if not solution[period // (schedule.n_days * schedule.n_periods)]\
                                [period % (schedule.n_days * schedule.n_periods)] in courses_indices]
    
    return len(periods_available)


def calculate_naa(course_index: int, lectures_pool: list[int]) -> int:
    """Calculates the number of lectures still to be assigned"""
    return lectures_pool.count(course_index)

def calculate_nhsv(course_index: int, schedule: Schedule, solution: Matrix) -> int:
    """Calculates the number of pairs of periods and rooms available for the given course"""
    # TODO entender o que significa pares horário/sala disponíveis
    return 1

def calculate_presence(course_index: int, schedule: Schedule, solution: Matrix) -> int:
    """Calculates the number of curricula that the course belongs to"""
    course = schedule.courses[course_index]
    return sum(1 for curriculum in schedule.curricula if course.id in curriculum.members)

def calculate_concurrency(course_index: int, period: int, schedule: Schedule, solution: Matrix) -> int:
    """Calculates the number of lectures that can also be allocated to the period/room"""
    course = schedule.courses[course_index]
    room = period // (schedule.n_days * schedule.n_periods)
    day_period = period % (schedule.n_days * schedule.n_periods)

    # find the curriculum that has the course, and then take the course from the members, and then put in a set to remove duplicates
    other_courses_same_curriculum = set([copy(curriculum.members).pop(curriculum.members.index(course.id)) \
                                        for curriculum in schedule.curricula if course.id in curriculum.members ])
    courses_indices = [schedule.courses.index(course) for course in other_courses_same_curriculum]

    # find the courses that are in the same period and room
    other_courses_same_period = [course for course in courses_indices \
                                    if solution[room][day_period] == course]

    return len(other_courses_same_period)


def calculate_conflicts_lecture(course_index: int, period: int, schedule: Schedule, solution: Matrix) -> int:
    """Calculates the number of conflicts for the given lecture and period"""

    BETA = 1 # Lu & Hao
    GAMMA = 0.5 # Lu & Hao
    # number of lectures that can also be allocated to the period/room
    n_periods_to_invalidate = calculate_concurrency(course_index, period, schedule, solution)
    # custo de alocação da aula c' no horário/sala h
    cost = caculate_cost_lecture_period(course_index, period, schedule, solution)

    return BETA*n_periods_to_invalidate + GAMMA*cost



def get_worst_course_conflict(lectures_pool: list[int], schedule: Schedule, solution: Matrix) -> int:
    """Returns the course with the most conflicts"""

    course_pool = set(lectures_pool)

    score_course = [CourseData(
        course_index, 
        calculate_nhv(course_index, schedule, solution),
        calculate_naa(course_index, lectures_pool)) \
                    for course_index in course_pool]

    def reducer(worst_course: CourseData, course: CourseData):
        if worst_course.course_index == -1:
            return course
        if course.naa == 0:
            return worst_course
        
        new_score = course.nhv / sqrt(course.naa)
        old_score = worst_course.nhv / sqrt(worst_course.naa)
        if new_score == old_score:
            course.nhsv = calculate_nhsv(course.course_index, schedule, solution)
            worst_course.nhsv = calculate_nhsv(worst_course.course_index, schedule, solution)
            new_score = course.nhsv / sqrt(course.nhsv)
            old_score = worst_course.nhsv / sqrt(worst_course.nhsv)
            if new_score == old_score:
                new_score = calculate_presence(course.course_index, schedule, solution)
                old_score = calculate_presence(worst_course.course_index, schedule, solution)
        return course if new_score > old_score else worst_course

    empty = CourseData(-1, -1, -1)

    worst_course_index = reduce(reducer, score_course, empty).course_index


    return lectures_pool.pop(lectures_pool.index(worst_course_index))


def generate_solution(schedule: Schedule) -> Matrix:
    """Generates an initial solution"""

    # Initialize the solution matrix with zeros
    solution = np.full((schedule.rooms_size, schedule.n_days * schedule.n_periods), -1)

    # Initialize the list of lectures to be assigned
    lectures_pool = [course.n_lectures*[course_index] for course_index, course in enumerate(schedule.courses)]
    # Flatten the list
    lectures_pool = [item for sublist in lectures_pool for item in sublist]

    # While there are lectures to be assigned
    while len(lectures_pool) > 0:
        
        # Get the lecture with the most conflicts
        lecture_with_most_conflicts = get_worst_course_conflict(lectures_pool, schedule, solution)

        # For all the possible periods available in solution get the number of conflicts for the lecture
        periods = [(day_period, calculate_conflicts_lecture(lecture_with_most_conflicts, day_period, schedule, solution)) \
                    for day_period in range(schedule.n_days * schedule.n_periods * schedule.rooms_size)]
        
        best_period = min(periods, key = lambda x: x[1])[0]

        solution[best_period // (schedule.n_days * schedule.n_periods)]\
            [best_period % (schedule.n_days * schedule.n_periods)] = lecture_with_most_conflicts

    return solution

def caculate_cost_lecture_period(course_index: int, period: int, schedule: Schedule, solution: Matrix) -> int:
    """Calculates the cost of allocating the lecture to the given period"""

    return 0
