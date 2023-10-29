from scheduling.models.schedule import Schedule, Solution


def solve(schedule: Schedule) -> list:
    """Solves the given schedule and returns a new schedule with the solution"""

    solutions = []
    for course in schedule.courses:
        for room in schedule.rooms:
            if room.capacity >= course.n_students:
                solutions.append(Solution(course.id, room.id, 1, 1))
                break

    return solutions
