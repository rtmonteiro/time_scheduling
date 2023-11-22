import logging
from scheduling.models.matrix import Matrix
import pandas as pd

def log_solution(matrix_solution: Matrix):
    df = pd.DataFrame(matrix_solution)
    df.columns = [f"Day {i//10} Period {i%10}" for i in range(df.shape[1])]
    df.index = [f"Room {i}" for i in range(df.shape[0])]
    logging.debug(df)
