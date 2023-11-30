import logging
from scheduling.models.matrix import Matrix
import pandas as pd

def log_solution(matrix_solution: Matrix, n_period: int):
    df = pd.DataFrame(matrix_solution)
    df.columns = [f"Day {i//n_period} Period {i%n_period}" for i in range(df.shape[1])]
    df.index = [f"Room {i}" for i in range(df.shape[0])]
    logging.debug(df)

def log_matrix(matrix_solution: Matrix):
    df = pd.DataFrame(matrix_solution)
    