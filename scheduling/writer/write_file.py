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
                  solution_path: str):
    filename, ext = os.path.splitext(os.path.basename(solution_path))
    foldername = os.path.dirname(solution_path)
    results_path = f"{foldername}/scores_{filename}.res"
    if not os.path.exists(os.path.dirname(results_path)):
        os.makedirs(os.path.dirname(results_path))
    with open(results_path, "w") as file:
        file.write(str(params) + "\n")
        for result in results:
            file.write(str(result) + "\n")

def write_json(schedule: Schedule, file_path: str):
    # write schedule to file
    with open(file_path, "w") as file:
        file.write(schedule.toJson())
