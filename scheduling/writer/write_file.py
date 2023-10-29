def write_file(solutions, file_path):
    with open(file_path, "w") as file:
        for solution in solutions:
            file.write(str(solution) + "\n")
