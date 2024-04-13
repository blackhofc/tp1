import utils.algorithms as algorithms
import utils.utils as utils
import matplotlib.pyplot as plt
import numpy as np
import json, random, time

INSTANCES: json = {
    "ASPEN":      "aspen_simulation",
    "ETHANOL":    "ethanol_water_vle",
    "OPTIMISTIC": "optimistic_instance",
    "TITANIUM":   "titanium",
    "SONGS":      "songs_per_year",
}

def get_experiment():
    x = random.randint(30, 30)
    y = random.randint(30, 30)
    K = random.randint(15, x)  # Ensures k is less than or equal to x
    return x, y, K


def save_experiment(data, file_path, encoding='utf-8'):
    try:
        with open(file_path, 'w', encoding=encoding) as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving JSON data: {e}")
        return False


def execute_algorithm(algorithm:str, params, instance):
    print('run {} with {}'.format(algorithm, params))
    
    grid_x = np.linspace(min(instance['x']), max(instance['x']), num=params['x'], endpoint=True)
    grid_y = np.linspace(min(instance['y']), max(instance['y']), num=params['y'], endpoint=True)
 
    start = time.time()
    if algorithm == 'brute_force':
        algorithms.brute_force(instance, grid_x, grid_y, params['K'])
    
    elif algorithm =='back_tracking':
        algorithms.back_tracking(instance, grid_x, grid_y, params['K'])
        
    elif algorithm == 'dynamic':
        algorithms.dynamic(instance, grid_x, grid_y, params['K'])
    else:
        return 0.0
    
    end = time.time()
    
    return end - start

algos = ['dynamic']

if __name__ == '__main__':
    print('experiments.py')
    
    experiments = {}
    
    params = {}
    for i in range(1, 6):
        x, y, K = get_experiment()
        params['{}:{}:{}'.format(x,y,K)] = {'x': x, 'y': y, 'K': K}
        
    
    for instance in INSTANCES:
        instanceData: json = utils.readJSON(INSTANCES[instance])

        experiments.setdefault(instance, [])
        
        for param in params:

            function = { }
            for algo in algos:
                runtime:float = execute_algorithm(algo, params[param], instanceData)
                function[algo] = { 'runtime': runtime }

            experiments[instance].append( { 'iteration': i, 'algorithms': function, 'params': params[param] })
                
                
            save_experiment(experiments, './files/experiments.json')
    