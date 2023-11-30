from scheduling.models.params import Params
from scheduling.reader.reader import read_file
from scheduling.results import Results
from scheduling.solver.solver import solve
from scheduling.writer.write_file import write_file, write_results
import sys
import logging
from os import path


def main():

    logging.basicConfig(level=logging.DEBUG)
    logging.debug('Starting main.py')
    if len(sys.argv) < 2:
        logging.error("Usage: python main.py <file_path>")
        return
    file_path = sys.argv[1]
    schedule = read_file(file_path)

    params = get_params()
    solved_schedule = solve(schedule, params)

    filename = path.basename(file_path)
    write_results(Results().getResults(), f"out/scores_{filename}.txt")
        
    solution_path = "out/solution.ctt"
    if len(sys.argv) > 2:
        solution_path = sys.argv[2]
    write_file(solved_schedule, solution_path)

def get_params():

    # Expectation: 
    # --max_iter <int>
    # --max_perturb <int>
    # --max_success <int>
    # --alpha <float>
    # --max_time <int>
    params = [(param, sys.argv[param_index + 1]) for param_index, param in enumerate(sys.argv) if param.startswith("--")]
    return Params(dict(params))



if __name__ == "__main__":
    main()
