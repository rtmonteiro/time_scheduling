class Params():
    def __init__(self, params):
        if "max_iter" in params:
            max_iter = params["max_iter"]
            self.max_iter = int(max_iter) if max_iter is not None else 100
        if "max_perturb" in params:
            max_perturb = params["max_perturb"]
            self.max_perturb = int(max_perturb) if max_perturb is not None else 100
        if "max_success" in params:
            max_success = params["max_success"]
            self.max_success = int(max_success) if max_success is not None else 100
        if "initial_temp" in params:
            initial_temp = params["initial_temp"]
            self.initial_temp = int(initial_temp) if initial_temp is not None else 30
        if "alpha" in params:
            alpha = params["alpha"]
            self.alpha = float(alpha) if alpha is not None else 0.9
        if "max_time" in params:
            max_time = params["max_time"]
            self.max_time = int(max_time) if max_time is not None else 1000
    
    def __str__(self):
        return f"{self.max_iter}, {self.max_perturb}, {self.max_success}, {self.initial_temp}, {self.alpha}, {self.max_time}"
        