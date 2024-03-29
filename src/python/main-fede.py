import json
import numpy as np

BIG_NUMBER = 1e10  # Revisar si es necesario.


def main():

    # Ejemplo para leer una instancia con json
    instance_name = "titanium.json"
    filename = "data/" + instance_name
    with open(filename) as f:
        instance = json.load(f)

    m = 6
    n = 6
    N = 5

    # Ejemplo para definir una grilla de m x n.
    grid_x = np.linspace(min(instance["x"]), max(instance["x"]), num=m, endpoint=True)
    grid_y = np.linspace(min(instance["y"]), max(instance["y"]), num=n, endpoint=True)

    # TODO: aca se deberia ejecutar el algoritmo.
    # Qué quiero que haga el algoritmo:
    # Evaluar todos los posibles breakpoints?
    # MINIMIZAR EL ERROR GLOBAL (solución "única")

    def y_index(grid_y, array):
        diff = array[len(array) - 1][1] - array[len(array) - 2][1]
        if array[len(array) - 1][1] == array[len(array) - 2][1]:
            i = array[len(array) - 1][1]
        elif array[len(array) - 1][1] > array[len(array) - 2][1] and diff >= 0:
            i = diff
        elif array[len(array) - 1][1] < array[len(array) - 2][1] and -diff < len(
            grid_y
        ):
            i = -diff
        return i

    def calculate_error(y2, y1, x2, x1, data):
        x = [x1, x2]
        y = [y1, y2]
        coefficients = np.polyfit(x, y, 1)
        m = coefficients[0]
        b = coefficients[1]

        res = 0
        for i in range(data["n"]):
            if data["x"][i] > x1 and data["x"][i] <= x2:
                res += abs(data["y"][i] - (m * data["x"][i] + b))
        return res

    def pwl_fit_fb(grid_x, grid_y, k, data):
        """Dado una discretización, un conjunto de datos y un número de K breakpoints, genera un .json con un PWL_FIT correspondiente
        Requiere grillas y datos no nulos, y K > 0"""

        current_solution = {"sol": [], "obj": 0}
        best = {"sol": [], "obj": BIG_NUMBER}
        pwl_fit_fb_bis(grid_x, grid_y, k, data, 0, current_solution, best)
        return best

    def pwl_fit_fb_bis(grid_x, grid_y, k, data, index, current_solution, best_solution):
        if k == 0 and len(current_solution["sol"]) == len(grid_x):
            # Analizo si mi solución es óptima para agarrarla
            if current_solution["obj"] < best_solution["obj"]:
                best_solution.update({"obj": current_solution["obj"]})
                best_solution.update({"sol": current_solution["sol"].copy()})
            # Ya tengo la solución armada

        # Caso FINAL
        elif k == 1:
            for i in range(len(grid_y)):
                local_error = calculate_error(
                    grid_y[i],
                    grid_y[
                        current_solution["sol"][len(current_solution["sol"]) - 1][1]
                    ],
                    grid_x[index],
                    grid_x[index - 1],
                    data,
                )
                current_solution["sol"].append((index, i))
                current_solution["obj"] += local_error
                pwl_fit_fb_bis(
                    grid_x,
                    grid_y,
                    k - 1,
                    data,
                    index + 1,
                    current_solution,
                    best_solution,
                )
                current_solution["obj"] -= local_error
                current_solution["sol"].pop()

        # Caso INICIO
        elif index == 0 and k != 0:
            for i in range(len(grid_y)):
                current_solution["obj"] += data["y"][0] - grid_y[0]
                current_solution["sol"].append((0, i))
                pwl_fit_fb_bis(
                    grid_x,
                    grid_y,
                    k - 1,
                    data,
                    index + 1,
                    current_solution,
                    best_solution,
                )
                current_solution["sol"].pop()
                current_solution["obj"] = 0

        # Caso genérico
        elif k > 1 and index != 0:
            # Subcaso: me sobran puntos en la grilla, no incluyo a este x
            if k < len(grid_x) - index:

                if index == 1:
                    y_value = grid_y[current_solution["sol"][0][1]]
                    local_error = calculate_error(
                        y_value, y_value, grid_x[index], grid_x[index - 1], data
                    )
                else:
                    y_value_prev = grid_y[
                        current_solution["sol"][len(current_solution["sol"]) - 1][1]
                    ]
                    y_value = grid_y[y_index(grid_y, current_solution["sol"])]
                    local_error = calculate_error(
                        y_value, y_value_prev, grid_x[index], grid_x[index - 1], data
                    )
                current_solution["obj"] += local_error
                current_solution["sol"].append(
                    (index, y_index(grid_y, current_solution["sol"]))
                )
                pwl_fit_fb_bis(
                    grid_x, grid_y, k, data, index + 1, current_solution, best_solution
                )
                current_solution["obj"] -= local_error
                current_solution["sol"].pop()

            # Si hay o no hay extra, evalúo incluir a este x.
            for i in range(len(grid_y)):

                # Si el anterior x es un breakpoint
                y_value_prev = grid_y[
                    current_solution["sol"][len(current_solution["sol"]) - 1][1]
                ]
                local_error = calculate_error(
                    grid_y[i], y_value_prev, grid_x[index], grid_x[index - 1], data
                )
                current_solution["obj"] += local_error
                current_solution["sol"].append((index, i))
                pwl_fit_fb_bis(
                    grid_x,
                    grid_y,
                    k - 1,
                    data,
                    index + 1,
                    current_solution,
                    best_solution,
                )
                current_solution["obj"] -= local_error
                current_solution["sol"].pop()

    # Posible ejemplo (para la instancia titanium) de formato de solucion, y como exportarlo a JSON.
    # La solucion es una lista de tuplas (i,j), donde:
    # - i indica el indice del punto de la discretizacion de la abscisa
    # - j indica el indice del punto de la discretizacion de la ordenada.

    best = pwl_fit_fb(grid_x, grid_y, N, instance)
    print(best)

    # Represetnamos la solucion con un diccionario que indica:
    # - n: cantidad de breakpoints
    # - x: lista con las coordenadas de la abscisa para cada breakpoint
    # - y: lista con las coordenadas de la ordenada para cada breakpoint
    solution = {}
    solution["n"] = len(best["sol"])
    solution["x"] = [grid_x[x[0]] for x in best["sol"]]
    solution["y"] = [grid_y[x[1]] for x in best["sol"]]
    solution["obj"] = best["obj"]

    # Se guarda el archivo en formato JSON
    with open("solution_" + instance_name, "w") as f:
        json.dump(solution, f)


if __name__ == "__main__":
    main()
