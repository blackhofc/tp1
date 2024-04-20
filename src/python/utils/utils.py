import json
from typing import List
import matplotlib.pyplot as plt


def readJSON(instance: str) -> json:
    """
    Lee un archivo JSON que contiene los datos de la instancia del problema a partir del nombre del mismo.

    Retorna:
        Los datos de la instancia en formato JSON.
    """
    with open("../../data/{}.json".format(instance)) as f:
        instance = json.load(f)
        return instance


def saveJSON(instance: str, data: json):
    """
    Guarda los datos en formato JSON.
    """
    with open("./solutions/{}.json".format(instance), "w") as f:
        json.dump(data, f)


def plot_pwl(solution, color="g"):
    """
    Grafica función continua piecewise linear dada una solución en el formato retornado por los algoritmos implementados,
    en el color que se prefiera.
    """
    for i in range(solution["n"] - 1):
        plt.plot(
            [solution["x"][i], solution["x"][i + 1]],
            [solution["y"][i], solution["y"][i + 1]],
            color=color,
        )


def plot_data(data, color="k"):
    """
    Muestra en un gráfico de puntos el conjunto de datos de la instancia cargada.
    """
    plt.plot(data["x"], data["y"], ".", color=color)
