from scheduling.reader.reader import read_file
from scheduling.solver.solver import solve
from scheduling.writer.write_file import write_file
import sys


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <file_path>")
        return
    file_path = sys.argv[1]
    schedule = read_file(file_path)
    solved_schedule = solve(schedule)

    # print(solved_schedule.solution())
    solution_path = "solution.ctt"
    if len(sys.argv) == 3:
        solution_path = sys.argv[2]
    write_file(solved_schedule, solution_path)


if __name__ == "__main__":
    main()
