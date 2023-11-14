from scheduling.models.schedule import Assignment, Schedule
from scheduling.solver.checker import Matrix, init_matrix


def mapper(schedule: Schedule, solution: list[Assignment]) -> Matrix:
    """Maps a schedule to a list of lists of integers.

    Args:
        schedule (Schedule): The schedule to be mapped.

    Returns:
        Matrix: The mapped schedule.
    """
    mapped_schedule = init_matrix(schedule)

    for assignment in solution:
        room_index = schedule.rooms.index(assignment.room_id)
        day_index = assignment.day
        period_index = assignment.period

        mapped_schedule[room_index][day_index * schedule.n_periods + period_index] = assignment.course_id

    return mapped_schedule

def mapper(schedule: Schedule, matrix: Matrix) -> list[Assignment]:
    """Maps a matrix of rooms by day_period of course_indices to a schedule.

    Args:
        schedule (Schedule): The schedule to be mapped.
        matrix (Matrix): The matrix to be mapped.

    Returns:
        list[Assignment]: The mapped schedule.
    """
    mapped_schedule = []

    for room_index in range(schedule.rooms_size):
        for day_index in range(schedule.n_days):
            for period_index in range(schedule.n_periods):
                course_index = matrix[room_index][day_index * schedule.n_periods + period_index]

                course_id = None if course_index == -1 else schedule.courses[course_index - 1].id

                if course_id is not None:
                    mapped_schedule.append(Assignment(course_id, schedule.rooms[room_index].id, day_index, period_index))

    return mapped_schedule
