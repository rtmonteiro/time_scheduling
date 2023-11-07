from scheduling.models.schedule import Schedule, Assignment


def write_file(solutions: list[Assignment], file_path: str):
    with open(file_path, "w") as file:
        for solution in solutions:
            file.write(str(solution) + "\n")

def write_json(schedule: Schedule, file_path: str):
    with open(file_path, "w") as file:
        file.write(schedule.toJson())
