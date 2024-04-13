import utils.algorithms as algorithms
import utils.utils as utils
import matplotlib.pyplot as plt
import numpy as np
import json, time, math, random


'''
Dada una instancia todas las combinaciones posibles 
'''

INSTANCES: json = {
    "ASPEN":      "aspen_simulation",
    "ETHANOL":    "ethanol_water_vle",
    "OPTIMISTIC": "optimistic_instance",
    #"TITANIUM":   "titanium",
    #"SONGS":      "songs_per_year",
}


def save_experiment(data, file_path, encoding='utf-8'):
    try:
        with open(file_path, 'w', encoding=encoding) as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving JSON data: {e}")
        return False


def execute_algorithm(algorithm:str, params, instance):    
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


def root(val, e=-1):
    if int(math.sqrt(val)) == 2:
        return 2
    return max(int(math.sqrt(val)), 2)

def makeCombinations(iSize:int):
    #random.randint(2, root(iSize))
    
    m1 = {
        'low':     random.randint(2, root(iSize)),
        'medium':  random.randint(root(iSize), int(iSize/2)),
        'high:':   random.randint(int(iSize/2), iSize)
    }
    
    m2 = {
        'low':     random.randint(2, root(iSize)),
        'medium:': random.randint(root(iSize), int(iSize/2)),
        'high':    random.randint(int(iSize/2), iSize)
    }
    
    komb = {}    
    for mode in ['low', 'medium', 'high']:
        for value in m1:
            k = 0
            if mode == 'low':
                k = random.randint(2, root(m1[value], 2))
            elif mode =='medium': 
                k = random.randint(root(m1[value]), int(m1[value]/2))
            else:
                k = random.randint(int(m1[value]/2), m1[value])
                
            komb['{}_{}'.format(value, mode)] = {
                'n': m1[value],
                'k': k
            }
                
    return komb

if __name__ == '__main__':
    print('EXP_1_instance.py')
    
    experiments = {}
    
    instanceName:str = 'OPTIMISTIC'
    
    instanceData: json = utils.readJSON(INSTANCES[instanceName])
    instanceSize: float = instanceData['n']
    
    combinations = makeCombinations(instanceSize)

    save_experiment(combinations, './files/1_instance.json')