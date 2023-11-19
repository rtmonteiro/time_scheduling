from scheduling.models.matrix import Matrix
from scheduling.models.schedule import Schedule
from scheduling.utils import is_element_absent, search_subarray_in_matrix

def init_matrix(schedule: Schedule) -> Matrix:
    """Initializes a matrix of rooms by day_period of course_indices to -1."""
    
    return [[-1 for _ in range(schedule.n_days*schedule.n_periods)] \
            for _ in range(schedule.rooms_size)]

    

def check_constraints(solution: Matrix, schedule: Schedule) -> int:
    """Returns the fitness of the given solution"""

    ## Hard Constraints ##
    score = 0
    # 1. Lectures: All lectures of a course must be scheduled, and they must be assigned to distinct periods. A violation occurs if a lecture is not scheduled.
    score += check_lectures(solution, schedule)

    # 2. RoomOccupancy: Two lectures cannot take place in the same room in the same period. Two lectures in the same room at the same period represent one violation. Any extra lecture in the same period and room counts as one more violation.
    score += check_room_occupancy(solution, schedule)
    
    # 3. Conflicts: Lectures of courses in the same curriculum or taught by the same teacher must be all scheduled in different periods. Two conflicting lectures in the same period represent one violation. Three conflicting lectures count as 3 violations: one for each pair.
    score += check_conflicts(solution, schedule)

    # 4. Availabilities: If the teacher of the course is not available to teach that course at a given period, then no lectures of the course can be scheduled at that period. Each lecture in a period unavailable for that course is one violation.

    ## Soft Constraints ##

    # 5. RoomCapacity: For each lecture, the number of students that attend the course must be less or equal than the number of seats of all the rooms that host its lectures.Each student above the capacity counts as 1 point of penalty.

    # 6. MinimumWorkingDays: The lectures of each course must be spread into the given minimum number of days. Each day below the minimum counts as 5 points of penalty.

    # 7. CurriculumCompactness: Lectures belonging to a curriculum should be adjacent to each other (i.e., in consecutive periods). For a given curriculum we account for a violation every time there is one lecture not adjacent to any other lecture within the same day. Each isolated lecture in a curriculum counts as 2 points of penalty.

    return score

def check_lectures(matrix_solution: Matrix, schedule: Schedule) -> int:
    """Returns the number of violations of the lectures constraint
    
    All lectures of a course must be scheduled, and they must be assigned to distinct periods. A violation occurs if a lecture is not scheduled
    """
    score = 0

    # Check if any course is not scheduled
    score += check_course_not_schedule(matrix_solution, schedule)
    
    # Check if all the lectures of a course are scheduled
    score += check_lecture_not_schedule(matrix_solution, schedule)

    return score

def check_lecture_not_schedule(matrix_solution: Matrix, schedule: Schedule) -> int:
    """Returns the number of violations of a lecture not scheduled"""

    # TODO - Score based of each lecture not scheduled

    score = 0
    for course_index, course in enumerate(schedule.courses):
        if is_element_absent(matrix_solution, course_index):
            continue
        row_index, index = search_subarray_in_matrix(matrix_solution, [course_index]*course.n_lectures)
        if row_index == -1:
            score += 1
    return score


def check_course_not_schedule(matrix_solution: Matrix, schedule: Schedule) -> int:
    """Returns the number of violations of a course not scheduled"""
    return sum(1 for course_index in range(schedule.courses_size)\
                 if is_element_absent(matrix_solution, course_index))
    
def check_room_occupancy(matrix_solution: Matrix, schedule: Schedule) -> int:
    """Returns the number of violations of the room occupancy constraint
    
    Two lectures cannot take place in the same room in the same period. Two lectures in the same room at the same period represent one violation. Any extra lecture in the same period and room counts as one more violation.
    """
    score = 0
    for room_index in range(schedule.rooms_size):
        for day_period in range(schedule.n_days*schedule.n_periods):
            course_indices = [matrix_solution[room_index][day_period]]
            if course_indices[0] == -1:
                continue
            # Check if there are more than one course in the same room and period
            for other_room_index in range(room_index+1, schedule.rooms_size):
                if matrix_solution[other_room_index][day_period] == course_indices[0]:
                    course_indices.append(matrix_solution[other_room_index][day_period])
            # Check if there are more than one course in the same room and period
            if len(course_indices) > 1:
                score += len(course_indices) - 1
    return score

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
