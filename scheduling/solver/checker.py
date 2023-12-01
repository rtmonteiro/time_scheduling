import logging
import numpy as np
from scheduling.models.matrix import Matrix
from scheduling.models.schedule import Schedule
from scheduling.utils import is_element_absent, search_lectures, search_subarray_in_matrix

def init_matrix(schedule: Schedule) -> Matrix:
    """Initializes a matrix of rooms by day_period of course_indices to -1."""

    return np.full((schedule.rooms_size, schedule.n_days*schedule.n_periods), -1)


def check_constraints(solution: Matrix, schedule: Schedule) -> int:
    """Returns the fitness of the given solution"""

    weights = [1, 1, 1, 1, 1, 5, 2, 1]

    score = 0
    ## Hard Constraints ##

    # 1. Lectures: All lectures of a course must be scheduled, and they must be assigned to distinct periods. A violation occurs if a lecture is not scheduled.
    score = check_lectures(solution, schedule) * weights[0]

    # 2. RoomOccupancy: Two lectures cannot take place in the same room in the same period. Two lectures in the same room at the same period represent one violation. Any extra lecture in the same period and room counts as one more violation.
    score = check_room_occupancy(solution, schedule) * weights[1]
    
    # 3. Conflicts: Lectures of courses in the same curriculum or taught by the same teacher must be all scheduled in different periods. Two conflicting lectures in the same period represent one violation. Three conflicting lectures count as 3 violations: one for each pair.
    score = check_conflicts(solution, schedule) * weights[2]

    # 4. Availabilities: If the teacher of the course is not available to teach that course at a given period, then no lectures of the course can be scheduled at that period. Each lecture in a period unavailable for that course is one violation.
    score = check_availabilities(solution, schedule) * weights[3]

    ## Soft Constraints ##

    # 5. RoomCapacity: For each lecture, the number of students that attend the course must be less or equal than the number of seats of all the rooms that host its lectures.Each student above the capacity counts as 1 point of penalty.
    score += check_room_capacity(solution, schedule) * weights[4]
    
    # 6. MinimumWorkingDays: The lectures of each course must be spread into the given minimum number of days. Each day below the minimum counts as 5 points of penalty.
    score += check_minimun_word_days(solution, schedule) * weights[5]

    # 7. CurriculumCompactness: Lectures belonging to a curriculum should be adjacent to each other (i.e., in consecutive periods). For a given curriculum we account for a violation every time there is one lecture not adjacent to any other lecture within the same day. Each isolated lecture in a curriculum counts as 2 points of penalty.
    score += check_curriculum_compactness(solution, schedule) * weights[6]

    # 8. RoomStability: All lectures of a course should be given in the same room. Each distinct room used for the lectures of a course, but the first, counts as 1 point of penalty
    score += check_room_stability(solution, schedule) * weights[7]

    logging.debug(f"Score: {score}")
    return score

def check_lectures(matrix_solution: Matrix, schedule: Schedule) -> int:
    """Returns the number of violations of the lectures constraint
    
    All lectures of a course must be scheduled, and they must be assigned to distinct periods. A violation occurs if a lecture is not scheduled
    """
    score = 0
    for course_index, course in enumerate(schedule.courses):
        counter = 0
        for period in range(schedule.rooms_size*schedule.n_days*schedule.n_periods):
            if matrix_solution[period // (schedule.n_days * schedule.n_periods)]\
                [period % (schedule.n_days * schedule.n_periods)] == course_index:
                counter += 1
        if counter != course.n_lectures:
            score += course.n_lectures - counter

    return score

    
def check_room_occupancy(matrix_solution: Matrix, schedule: Schedule) -> int:
    """Returns the number of violations of the room occupancy constraint
    
    Two lectures cannot take place in the same room in the same period. Two lectures in the same room at the same period represent one violation. Any extra lecture in the same period and room counts as one more violation.
    """
    # score = 0
    # for room_index in range(schedule.rooms_size):
    #     for day_period in range(schedule.n_days*schedule.n_periods):
    #         course_indices = [matrix_solution[room_index][day_period]]
    #         if course_indices[0] == -1:
    #             continue
    #         # Check if there are more than one course in the same room and period
    #         for other_room_index in range(room_index+1, schedule.rooms_size):
    #             if matrix_solution[other_room_index][day_period] == course_indices[0]:
    #                 course_indices.append(matrix_solution[other_room_index][day_period])
    #         # Check if there are more than one course in the same room and period
    #         if len(course_indices) > 1:
    #             score += len(course_indices) - 1
    return 0

def check_conflicts(matrix_solution: Matrix, schedule: Schedule) -> int:
    """Returns the number of violations of the conflicts constraint
    
    Lectures of courses in the same curriculum or taught by the same teacher must be all scheduled in different periods.  Two conflicting lectures in the same period represent one violation. Three conflicting lectures count as 3 violations: one for each pair.
    """
    score = 0
    for room in matrix_solution:
        for course_index in room:
            if course_index == -1:
                continue
            course = schedule.courses[course_index]
            # Check if there are more than one course of the same curriculum or teacher in the same period in other rooms
            for other_room in matrix_solution:
                for other_course_index in other_room:
                    if other_course_index == -1 \
                        or other_course_index == course_index:
                        continue
                    other_course = schedule.courses[other_course_index]
                    is_same_curriculum = False
                    for curriculum in schedule.curricula:
                        if course.id in curriculum.members:
                            if other_course.id in curriculum.members:
                                is_same_curriculum = True
                    if is_same_curriculum or course.teacher_id == other_course.teacher_id:
                        score += 1
    
    return score

def check_availabilities(matrix_solution: Matrix, schedule: Schedule) -> int:
    """Returns the number of violations of the availabilities constraint
    
    If the teacher of the course is not available to teach that course at a given period, then no lectures of the course can be scheduled at that period. Each lecture in a period unavailable for that course is one violation.
    """
    score = 0
    for room in matrix_solution:
        for day_period, course_index in enumerate(room):
            if course_index == -1:
                continue
            course = schedule.courses[course_index]
            day = day_period % schedule.n_periods
            period = day_period // schedule.n_periods
            score += sum(1 for constraint in course.constraints \
                            if constraint.day == day \
                            and constraint.day_period == period)

    return score

def check_room_capacity(matrix_solution: Matrix, schedule: Schedule) -> int:
    """Returns the number of violations of the room capacity constraint
    
    For each lecture, the number of students that attend the course must be less or equal than the number of seats of all the rooms that host its lectures. Each student above the capacity counts as 1 point of penalty.
    """
    score = 0
    for room_index, room in enumerate(matrix_solution):
        for course_index in room:
            if course_index == -1:
                continue
            course = schedule.courses[course_index]
            students_above_capacity = course.n_students - schedule.rooms[room_index].capacity
            score += students_above_capacity if students_above_capacity > 0 else 0
    return score

def check_minimun_word_days(matrix_solution: Matrix, schedule: Schedule) -> int:
    """Returns the number of violations of the minimum working days constraint
    
    The lectures of each course must be spread into the given minimum number of days. Each day below the minimum counts as 5 points of penalty.
    """
    score = 0
    for course_index, course in enumerate(schedule.courses):
        if is_element_absent(matrix_solution, course_index):
            continue
        # Get the periods where there is a lecture of the course
        periods = search_lectures(matrix_solution, course_index)
        # Get the days where there is a lecture of the course
        days = set(period % schedule.n_periods for _, period in periods)
        if len(days) < course.min_working_days:
            score += (course.min_working_days - len(days))
    return score

def check_curriculum_compactness(matrix_solution: Matrix, schedule: Schedule) -> int:
    """Returns the number of violations of the curriculum compactness constraint
    
    Lectures belonging to a curriculum should be adjacent to each other (i.e., in consecutive periods). For a given curriculum we account for a violation every time there is one lecture not adjacent to any other lecture within the same day. Each isolated lecture in a curriculum counts as 2 points of penalty.
    """
    score = 0
    for curriculum in schedule.curricula:
        # For each course in a curriculum
        for course_id in curriculum.members:
            course_index = schedule.courses.index(course_id)
            courses_same_curriculum_indexes = [schedule.courses.index(other_course_id) for other_course_id in curriculum.members]
            if is_element_absent(matrix_solution, course_index):
                continue
            # Get the periods where there is a lecture of the course
            periods = search_lectures(matrix_solution, course_index)
            # Check if the adjacent lectures are from the same curriculum
            for room_index, period in periods:
                day_period = period % schedule.n_periods
                # At the beginning of the day, cannot check the previous period
                if day_period == 0:
                    if matrix_solution[room_index][period+1] in courses_same_curriculum_indexes:
                        continue
                # At the end of the day, cannot check the next period
                elif day_period == (schedule.n_periods - 1):
                    if matrix_solution[room_index][period-1] in courses_same_curriculum_indexes:
                        continue
                # In the middle of the day, check the previous and next periods
                else:
                    if matrix_solution[room_index][period-1] in courses_same_curriculum_indexes \
                        and matrix_solution[room_index][period+1] in courses_same_curriculum_indexes:
                        continue
                score += 1
    return score

def check_room_stability(matrix_solution: Matrix, schedule: Schedule) -> int:
    """Returns the number of violations of the room stability constraint
    
    Lectures of a course should be all assigned to the same room. Each lecture in a different room counts as 1 point of penalty.
    """
    score = 0
    for course_index in range(schedule.courses_size):
        if is_element_absent(matrix_solution, course_index):
            continue
        course_rooms = 0
        for room in matrix_solution:
            if course_index in room:
                course_rooms += 1
        if course_rooms > 1:
            score += course_rooms - 1
    return score
