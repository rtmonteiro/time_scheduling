import os
import time
from scheduling.models.params import Params
from scheduling.models.schedule import Schedule, Assignment


def write_file(solutions: list[Assignment], file_path: str):
    # if directory doesn't exist, create it
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))
    
    # write solutions to file
    with open(file_path, "w") as file:
        for solution in solutions:
            file.write(str(solution) + "\n")

def write_results(results: list[tuple[int, int, float, int]],
                  params: Params,
                  file_path: str):
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    file_path = file_path + "_" + timestamp + ".txt"
    with open(file_path, "w") as file:
        file.write(str(params) + "\n")
        for result in results:
            file.write(str(result) + "\n")

def write_json(schedule: Schedule, file_path: str):
    # write schedule to file
    with open(file_path, "w") as file:
        file.write(schedule.toJson())
