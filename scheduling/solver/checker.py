from scheduling.models.schedule import Assignment, Schedule

def transform_matrix(solution: list[Assignment], schedule: Schedule) -> list[list[int]]:
    """Transforms the given solution into a matrix"""
    
    rooms_schedule = [[[0 for _ in range(schedule.n_periods)] for _ in range(schedule.n_days)] for _ in range(schedule.rooms_size)]

    for assignment in solution:
        room_index = schedule.rooms.index(assignment.room_id)
        rooms_schedule[room_index][assignment.day - 1][assignment.period - 1] = assignment.course_id

    return rooms_schedule
    

def check_constraints(solution: list[Assignment], schedule) -> int:
    """Returns the fitness of the given solution"""

    rooms_schedule = transform_matrix(solution, schedule)

    ## Hard Constraints ##
    score = 0
    # 1. Lectures: All lectures of a course must be scheduled, and they must be assigned to distinct periods. A violation occurs if a lecture is not scheduled.
    score += check_lectures(rooms_schedule)

    # 2. RoomOccupancy: Two lectures cannot take place in the same room in the same period. Two lectures in the same room at the same period represent one violation. Any extra lecture in the same period and room counts as one more violation.

    # 3. Conflicts: Lectures of courses in the same curriculum or taught by the same teacher must be all scheduled in different periods. Two conflicting lectures in the same period represent one violation. Three conflicting lectures count as 3 violations: one for each pair.

    # 4. Availabilities: If the teacher of the course is not available to teach that course at a given period, then no lectures of the course can be scheduled at that period. Each lecture in a period unavailable for that course is one violation.

    ## Soft Constraints ##

    # 5. RoomCapacity: For each lecture, the number of students that attend the course must be less or equal than the number of seats of all the rooms that host its lectures.Each student above the capacity counts as 1 point of penalty.

    # 6. MinimumWorkingDays: The lectures of each course must be spread into the given minimum number of days. Each day below the minimum counts as 5 points of penalty.

    # 7. CurriculumCompactness: Lectures belonging to a curriculum should be adjacent to each other (i.e., in consecutive periods). For a given curriculum we account for a violation every time there is one lecture not adjacent to any other lecture within the same day. Each isolated lecture in a curriculum counts as 2 points of penalty.

    return score

def check_lectures(matrix_solution: list[list[int]]) -> int:
    """Returns the number of violations of the lectures constraint"""
    score = 0
    return 0

    
