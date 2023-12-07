from scheduling.models.params import Params
from scheduling.reader.reader import read_file
from scheduling.results import Results
from scheduling.solver.solver import solve
from scheduling.writer.write_file import write_file, write_results
import sys
import logging
from os import path


def main(params_ref: Params = None, file_path_ref: str = None, output_path_ref = None):

    logging.basicConfig(level=logging.INFO)
    logging.info('Starting main.py')
    if len(sys.argv) < 2 and file_path_ref is None:
        logging.error("Usage: python main.py <file_path>")
        return
    file_path = sys.argv[1] if file_path_ref is None else file_path_ref
    schedule = read_file(file_path)

    params = get_params() if params_ref is None else params_ref
    solved_schedule = solve(schedule, params)
        
    solution_path = "out/solution.ctt" if output_path_ref is None else output_path_ref
    if len(sys.argv) > 2:
        solution_path = sys.argv[2]
    write_file(solved_schedule, solution_path)

    write_results(Results().getResults(), params, solution_path)
    logging.info('Finished main.py')

def get_params() -> Params:

    # Expectation: 
    # --max_iter <int>
    # --max_perturb <int>
    # --max_success <int>
    # --initial_temp <int>
    # --alpha <float>
    # --max_time <int>
    params = [(param[2:], sys.argv[param_index + 1]) for param_index, param in enumerate(sys.argv) if param.startswith("--")]
    params = Params(dict(params))
    return params


if __name__ == "__main__":
    main()
