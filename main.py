from scheduling.reader.reader import read_file
from scheduling.results import Results
from scheduling.solver.solver import solve
from scheduling.writer.write_file import write_file, write_results
import sys
import logging


def main():

    logging.basicConfig(level=logging.DEBUG)
    logging.debug('Starting main.py')
    if len(sys.argv) < 2:
        logging.error("Usage: python main.py <file_path>")
        return
    file_path = sys.argv[1]
    schedule = read_file(file_path)
    solved_schedule = solve(schedule)

    write_results(Results().getResults(), "out/results1.txt")
        

    solution_path = "out/solution.ctt"
    write_file(solved_schedule, solution_path)


if __name__ == "__main__":
    main()
