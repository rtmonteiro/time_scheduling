from os import system
import subprocess, sys
import itertools

from scheduling.models.params import Params

def run_case():
    arr_params = generate_params()

    for params in arr_params:
        params_str = ' '.join(f'--{k} {v}' for k, v in vars(params).items())
        datapath = 'data/comp00.ctt'
        outpath = 'out/comp00.ctt'
        command = 'python main.py ' + datapath + ' ' + outpath + ' ' + params_str
        print(command)
        system(command)
    

def generate_params() -> list[Params]:
    max_iters = [100, 200, 300]
    max_perturb = [50, 100, 200]
    max_success = [20, 30, 50]
    alpha = [0.5, 0.7, 0.9]
    max_time = 238

    params_list = []

    for combination in itertools.product(max_iters, max_perturb, max_success, alpha):
        params = Params(dict(max_iter=combination[0], 
                        max_perturb=combination[1], 
                        max_success=combination[2], 
                        alpha=combination[3], 
                        max_time=max_time))
        params_list.append(params)

    return params_list    


if __name__ == "__main__":
    run_case()
