import os
from scheduling.models.schedule import Schedule, Assignment


def write_file(solutions: list[Assignment], file_path: str):
    # if directory doesn't exist, create it
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))
    
    # write solutions to file
    with open(file_path, "w") as file:
        for solution in solutions:
            file.write(str(solution) + "\n")

def write_json(schedule: Schedule, file_path: str):
    # write schedule to file
    with open(file_path, "w") as file:
        file.write(schedule.toJson())
