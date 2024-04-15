import utils.algorithms as algorithms
import utils.utils as utils
import matplotlib.pyplot as plt
import numpy as np
import json, random, time

"""
Posible ejemplo (para la instancia titanium) de formato de solucion, y como exportarlo a JSON.
La solucion es una lista de tuplas (i,j), donde:
	i: indica el indice del punto de la discretizacion de la abscisa.
	j: indica el indice del punto de la discretizacion de la ordenada.
 
----------------------------------------------------------------------------------------------

Representamos la solucion con un diccionario que indica:
    n: Cantidad de breakpoints.
    x: Lista con las coordenadas de la abscisa para cada breakpoint.
    y: Lista con las coordenadas de la ordenada para cada breakpoint.
    
----------------------------------------------------------------------------------------------

Cada punto rk se los denomina breakpoint.
Cada función fk : [rk, rk+1] −→ R se la denomina pieza.
"""

DATA: json = {
    "ASPEN": "aspen_simulation",
    "ETHANOL": "ethanol_water_vle",
    "OPTIMISTIC": "optimistic_instance",
    "TITANIUM": "titanium",
    "TOY": "toy_instance",
}


def graph(instance: json, solution, m: int, n: int):
    grid_x = np.linspace(min(instance["x"]), max(instance["x"]), num=m, endpoint=True)
    grid_y = np.linspace(min(instance["y"]), max(instance["y"]), num=n, endpoint=True)

    print("\nX: {}\nY: {}".format(grid_x, grid_y))

    
    sol = {
        "n": len(solution["solution"]),
        "x": [point[0] for point in solution["solution"]],
        "y": [point[1] for point in solution["solution"]],
    }

    print("\n\nSOLUTION\nX: {}\nY: {}".format(sol["x"], sol["y"]))

    plt.title("Instance with PWL")
    plt.grid(True, which="both", linestyle="--", linewidth=0.5, color="gray", alpha=0.7)
    plt.xticks(grid_x)
    plt.yticks(grid_y)

    utils.plot_data(instance)
    utils.plot_pwl(sol, "g")

    plt.show()


def main():
    instance: json = utils.readJSON(DATA["OPTIMISTIC"])
    m = 15
    n = 15
    k = 3
    grid_x = np.linspace(min(instance["x"]), max(instance["x"]), num=m, endpoint=True)
    grid_y = np.linspace(min(instance["y"]), max(instance["y"]), num=n, endpoint=True)
    solutiondict = {'min_found': algorithms.BIG_NUMBER, "recursion": 0, "solution": []}
    inicio = time.time()
    best_y = algorithms.found_best_initial_y(instance, grid_x, grid_y, k, solutiondict)
    solution = algorithms.reconstruct_solution(grid_x, grid_y, k, best_y, solutiondict)
    #solution = algorithms.backtrack(instance, grid_x, grid_y, k+1)
    #solution = algorithms.brute_force(instance, grid_x, grid_y, k+1)
    final = time.time()
   
    with open('python.json', 'w') as f:
        json.dump(solution, f)
        
    print("solution", solution)

    graph(instance=instance, solution=solution, m=m, n=n)

    print("Tiempo: ", final-inicio)


if __name__ == "__main__":
    main()
