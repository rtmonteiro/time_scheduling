from scheduling.models.schedule import Schedule, Solution


def write_file(solutions: list[Solution], file_path: str):
    with open(file_path, "w") as file:
        for solution in solutions:
            file.write(str(solution) + "\n")

def write_json(schedule: Schedule, file_path: str):
    with open(file_path, "w") as file:
        file.write(schedule.toJson())
