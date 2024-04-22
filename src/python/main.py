import utils.algorithms as algorithms
import utils.utils as utils
import matplotlib.pyplot as plt
import numpy as np
import json, time, sys, threading

# Conjuntos de datos disponibles
DATA: json = {
    'ASPEN': 'aspen_simulation',
    'ETHANOL': 'ethanol_water_vle',
    'OPTIMISTIC': 'optimistic_instance',
    'SONGS': 'songs_per_year',
    'TITANIUM': 'titanium',
    'TOY': 'toy_instance',
}


# Auxiliar para graficar
def graph(instance: json, solution, m: int, n: int):
    grid_x = np.linspace(min(instance['x']), max(instance['x']), num=m, endpoint=True)
    grid_y = np.linspace(min(instance['y']), max(instance['y']), num=n, endpoint=True)

    print('\nX: {}\nY: {}'.format(grid_x, grid_y))

    sol = {
        'n': len(solution['solution']),
        'x': [point[0] for point in solution['solution']],
        'y': [point[1] for point in solution['solution']],
    }

    print('\n\nSOLUTION\nX: {}\nY: {}'.format(sol['x'], sol['y']))

    plt.title('Instance with PWL')
    plt.grid(True, which='both', linestyle='--', linewidth=0.5, color='gray', alpha=0.7)
    plt.xticks(grid_x)
    plt.yticks(grid_y)

    utils.plot_data(instance)
    utils.plot_pwl(sol, 'g')

    plt.show()


def get_sol(instance, grid_x, grid_y, k, algo):
    if algo=='bf':
        return algorithms.brute_force(instance, grid_x, grid_y, k)
    elif algo == 'bt':
        return algorithms.back_tracking(instance, grid_x, grid_y, k)
    return algorithms.dynamic(instance, grid_x, grid_y, k)

def main():
    # Tutorial de ejecución para la implementación

    # Cargar la instancia deseada con su clave en DATA.
    # (ASPEN, ETANOL, OPTIMISTIC, SONGS, TITANIUM o TOY)
    instance = utils.readJSON(DATA['ETHANOL'])

    # Definir valores para m1 (grilla horizontal), m2 (grilla vertical) y K breakpoints
    if len(sys.argv) != 5:
        print('Usage: python main.py m1 m2 k (bf || bt || dp)')
        sys.exit(1)

    # Parse command-line arguments
    m1 = int(sys.argv[1])
    m2 = int(sys.argv[2])
    k  = int(sys.argv[3])
    algo  = sys.argv[4]
    
    if algo not in ['bf', 'bt', 'dp']:
        print('{} not found, please use bf || bt || dp'.format(algo))
        sys.exit(1)

    # Se arma la discretización
    grid_x = np.linspace(min(instance['x']), max(instance['x']), num=m1, endpoint=True)
    grid_y = np.linspace(min(instance['y']), max(instance['y']), num=m2, endpoint=True)

    # Variable to hold the result
    solution = []

    # Function to execute your algorithm within a thread
    def execute_algorithm():
        nonlocal solution
        start_time = time.time()
        solution = get_sol(instance, grid_x, grid_y, k, algo)
        end_time = time.time()
        print('\nFinished in {}s m1: {} m2: {} K: {} Algorithm: {}'.format(round(end_time-start_time, 5), m1, m2, k, algo))
        with open('python_dynamic.json', 'w') as f:
            json.dump(solution, f)

    # Create a thread for executing the algorithm
    algorithm_thread = threading.Thread(target=execute_algorithm)

    # Start the thread
    algorithm_thread.start()

    # Create a timer to stop the script if it runs longer than 5 minutes
    timer = threading.Timer(60*5, stop_script)
    timer.start()

    # Wait for the thread to finish
    algorithm_thread.join()

    # Cancel the timer as the thread has finished
    timer.cancel()

    # Graficar la solución
    graph(instance=instance, solution=solution, m=m1, n=m2)
    
def stop_script():
    print('Execution timed out after 5 minutes.')
    sys.exit(1)


if __name__ == '__main__':
    main()
