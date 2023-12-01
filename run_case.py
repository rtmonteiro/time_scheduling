import multiprocessing as mp
import itertools
from main import main

from scheduling.models.params import Params

def run_case():
    arr_params = generate_params()

    processes = []
    for params in arr_params:
        p = mp.Process(target=main, args=(params,))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()
    print("###### Finished ######")


    

def generate_params() -> list[Params]:
    max_iters = [100]
    max_perturb = [100]
    max_success = [20, 30, 50]
    initial_temp = [30, 50, 80]
    alpha = [0.9, 0.95, 0.99]
    max_time = 238

    params_list = []

    for combination in itertools.product(max_iters, max_perturb, max_success, initial_temp, alpha):
        params = Params(dict(max_iter=combination[0], 
                        max_perturb=combination[1], 
                        max_success=combination[2], 
                        initial_temp=combination[3],
                        alpha=combination[4],
                        max_time=max_time))
        params_list.append(params)

    return params_list    


if __name__ == "__main__":
    run_case()
