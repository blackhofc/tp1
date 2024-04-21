import utils.algorithms as algorithms
import utils.utils as utils
import matplotlib.pyplot as plt
import numpy as np
import json, random, time

INSTANCES: json = {
    #"ASPEN":      "aspen_simulation",
    #"ETHANOL":    "ethanol_water_vle",
    #"OPTIMISTIC": "optimistic_instance",
    #"TITANIUM":   "titanium",
    "SONGS":      "songs_per_year",
}

def get_experiment():
    x = random.randint(2, 20)
    y = random.randint(2, 20)
    K = random.randint(2, x)  # Ensures k is less than or equal to x
    return x, y, K


def save_graph(instance: json, grid_x, grid_y, solution, filename, title):
    print("\nX: {}\nY: {}".format(grid_x, grid_y))

    sol = {
        "n": len(solution["solution"]),
        "x": [point[0] for point in solution["solution"]],
        "y": [point[1] for point in solution["solution"]],
    }

    print("\n\nSOLUTION\nX: {}\nY: {}".format(sol["x"], sol["y"]))

    plt.title(title)
    plt.grid(True, which="both", linestyle="--", linewidth=0.5, color="gray", alpha=0.7)
    plt.xticks(grid_x)
    plt.yticks(grid_y)

    utils.plot_data(instance)
    utils.plot_pwl(sol, "g")

    plt.savefig(filename)
    plt.close()

def save_experiment(data, file_path, encoding='utf-8'):
    try:
        with open(file_path, 'w', encoding=encoding) as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving JSON data: {e}")
        return False


def execute_algorithm(algorithm:str, params, instance, grid_x, grid_y):    
    
    start = time.time()

    sol = {}
    if algorithm == 'brute_force':
        sol = algorithms.brute_force(instance, grid_x, grid_y, params['K'])
    
    elif algorithm =='back_tracking':
        sol = algorithms.back_tracking(instance, grid_x, grid_y, params['K'])
        
    elif algorithm == 'dynamic':
        sol = algorithms.dynamic(instance, grid_x, grid_y, params['K'])
    else:
        return 0.0
    
    end = time.time()
    
    return end - start, sol

algos = ['dynamic']

if __name__ == '__main__':
    print('2_multiple_instances.py')
    
    experiments = {}
    
    params = {}
    for i in range(1, 20):
        x, y, K = get_experiment()
        params['{}:{}:{}'.format(x,y,K)] = { 'x': x, 'y': y, 'K': K }
        
    
    for ins in INSTANCES:
        instance: json = utils.readJSON(INSTANCES[ins])

        instanceSize: float = instance['n']
        
        experiments.setdefault(ins, [])
        
        print('\n----------Running instance -> {}----------'.format(instance))
        for i, param in enumerate(params):

            function = { }
            for algo in algos:
                print('\nRun [{}] with {} iteration {}'.format(algo, params[param], i))
                grid_x = np.linspace(min(instance['x']), max(instance['x']), num=params[param]['x'], endpoint=True)
                grid_y = np.linspace(min(instance['y']), max(instance['y']), num=params[param]['y'], endpoint=True)
                
                algorithm:float = execute_algorithm(algo, params[param], instance, grid_x, grid_y)
                
                solution = algorithm[1]
                
                # instance: json, grid_x, grid_y, solution, filename):
                exp_name = '{}-{}_{}_{}-{}'.format(ins, params[param]['x'], params[param]['y'], params[param]['K'], algo)
                #title ="[{}] n: {} m: {} K: {} err: {} t: {}s alg: {}".format(ins, params[param]['x'], params[param]['y'], params[param]['K'], round(solution['min_found'], 2), round(algorithm[0], 2), algo)
                title ="({}, {}, {}) =>E: {}".format(params[param]['x'], params[param]['y'], params[param]['K'], round(solution['min_found'], 2))
                save_graph(instance, grid_x, grid_y, solution, './files/graphs/giphy-{}.png'.format(i), title)
                
                function[algo] = { 'runtime': algorithm[0], 'solution': solution }
                
                print('Finished in {} seconds.'.format(round(algorithm[0], 4)))

            experiments[ins].append( { 'iteration': i, 'algorithms': function, 'params': params[param] })
                
                
            save_experiment(experiments, './files/test_exp.json')
    