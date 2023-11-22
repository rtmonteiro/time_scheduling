from io import TextIOWrapper
from ..models.schedule import Schedule, Course, Room, Curriculum, Constraint


def read_file(file_path):
    schedule = None
    with open(file_path, "r") as f:
        schedule = read_schedule(f, schedule)

        # Read courses
        f.readline()  # Skip line
        f.readline()  # Skip Title
        read_courses(schedule, f)

        # Read rooms
        f.readline()  # Skip line
        f.readline()  # Skip Title
        read_rooms(schedule, f)

        # Read curricula
        f.readline()  # Skip line
        f.readline()  # Skip Title
        read_curricula(schedule, f)

        # Read constraints
        f.readline()  # Skip line
        f.readline()  # Skip Title
        read_constraints(schedule, f)

    return schedule


def read_constraints(schedule: Schedule, f: TextIOWrapper):
    for _ in range(schedule.constraints_size):
        course_id, constraint = read_constraint(f.readline())
        course_index = schedule.courses.index(course_id)
        schedule.courses[course_index].constraints.append(constraint)


def read_constraint(str_constraint) -> Constraint:
    constraint = str_constraint.split(" ")
    return constraint[0], Constraint(constraint[1], constraint[2])


def read_curricula(schedule: Schedule, f: TextIOWrapper):
    for _ in range(schedule.curricula_size):
        schedule.curricula.append(read_curriculum(f.readline()))


def read_curriculum(str_curricula) -> Curriculum:
    curricula = str_curricula.split(" ")
    return Curriculum(curricula[0], curricula[2:-1])


def read_rooms(schedule: Schedule, f: TextIOWrapper):
    for _ in range(schedule.rooms_size):
        schedule.rooms.append(read_room(f.readline()))


def read_room(str_room) -> Room:
    room = str_room.split(" ")
    return Room(room[0], room[1])


def read_courses(schedule: Schedule, f: TextIOWrapper):
    for _ in range(schedule.courses_size):
        schedule.courses.append(read_course(f.readline()))


def read_course(str_course) -> Course:
    course = str_course.split(" ")
    return Course(course[0], course[1], course[2], course[3], course[4])


def read_schedule(f, schedule):
    # Read name, courses_size, rooms_size, n_days, n_periods, curricula_size, constraints_size
    name = f.readline().split(" ")[1].strip()
    course_size = f.readline().split(" ")[1].strip()
    rooms_size = f.readline().split(" ")[1].strip()
    n_days = f.readline().split(" ")[1].strip()
    n_periods = f.readline().split(" ")[1].strip()
    curricula_size = f.readline().split(" ")[1].strip()
    constraints_size = f.readline().split(" ")[1].strip()
    schedule = Schedule(
        name,
        n_days,
        n_periods,
        course_size,
        rooms_size,
        curricula_size,
        constraints_size,
    )
    return schedule
