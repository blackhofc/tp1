import utils.algorithms as algorithms
import utils.utils as utils
import matplotlib.pyplot as plt
import numpy as np
import json, time

# Conjuntos de datos disponibles
DATA: json = {
    "ASPEN": "aspen_simulation",
    "ETHANOL": "ethanol_water_vle",
    "OPTIMISTIC": "optimistic_instance",
    "SONGS": "songs_per_year",
    "TITANIUM": "titanium",
    "TOY": "toy_instance",
}


# Auxiliar para graficar
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
    # Tutorial de ejecución para la implementación

    # Cargar la instancia deseada con su clave en DATA.
    # (ASPEN, ETANOL, OPTIMISTIC, SONGS, TITANIUM o TOY)
    instance: json = utils.readJSON(DATA["TITANIUM"])

    # Definir valores para m1 (grilla horizontal), m2 (grilla vertical) y K breakpoints
    m1 = 25
    m2 = 25
    k = 4

    # Se arma la discretización
    grid_x = np.linspace(min(instance["x"]), max(instance["x"]), num=m1, endpoint=True)
    grid_y = np.linspace(min(instance["y"]), max(instance["y"]), num=m2, endpoint=True)

    start = time.time()
    # Para cada algoritmo cambiar el nombre a: brute_force(), back_tracking() o dynamic()
    # Todos toman los mismos parámetros para facilitar la alternancia de llamados
    solution = algorithms.dynamic(instance, grid_x, grid_y, k)
    end = time.time()

    # Se mide el tiempo que demoró la ejecución
    print("Finished", end - start)

    # Almacenar la solución obtenida, útil para comparaciones y orden.
    with open("python_dynamic.json", "w") as f:
        json.dump(solution, f)

    print("solution", solution)

    # Graficar la solución
    graph(instance=instance, solution=solution, m=m1, n=m2)


if __name__ == "__main__":
    main()
