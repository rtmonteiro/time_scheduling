from schedule import Schedule, Course, Room, Curricula, Constraint


def read_file(file_path):
    schedule = None
    with open(file_path, "r") as f:
        # Read name, courses_size, rooms_size, n_days, n_periods, curricula_size, constraints_size
        name = f.readline().split(" ")[1]
        courses_size = int(f.readline().split(" ")[1])
        rooms_size = int(f.readline().split(" ")[1])
        n_days = f.readline().split(" ")[1]
        n_periods = f.readline().split(" ")[1]
        curricula_size = int(f.readline().split(" ")[1])
        constraints_size = int(f.readline().split(" ")[1])
        schedule = Schedule(
            name,
            n_days,
            n_periods,
        )

        # Read courses
        f.readline()  # Skip line
        f.readline()  # Skip Title
        for _ in range(courses_size):
            course = f.readline().split(" ")
            schedule.courses.append(
                Course(course[0], course[1], course[2], course[3], course[4])
            )

        # Read rooms
        f.readline()  # Skip line
        f.readline()  # Skip Title
        for _ in range(rooms_size):
            room = f.readline().split(" ")
            schedule.rooms.append(Room(room[0], room[1]))

        # Read curricula
        f.readline()  # Skip line
        f.readline()  # Skip Title
        for _ in range(curricula_size):
            curricula = f.readline().split(" ")
            schedule.curricula.append(
                Curricula(curricula[0], curricula[2:-1])
            )

        # Read constraints
        f.readline()  # Skip line
        f.readline()  # Skip Title
        for _ in range(constraints_size):
            constraint = f.readline().split(" ")
            schedule.constraints.append(
                Constraint(constraint[0], constraint[1], constraint[2])
            )

    return schedule
