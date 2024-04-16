import json
from typing import List
import matplotlib.pyplot as plt

def readJSON(instance: str) -> json:
    '''
    Lee un archivo JSON que contiene los datos de la instancia del problema.
    
    Parámetros:
        - instance: Nombre de la instancia del problema.
        
    Retorna:
        Los datos de la instancia del problema en formato JSON.
    '''
    with open('../../data/{}.json'.format(instance)) as f:
        instance = json.load(f)
        return instance

def saveJSON(instance: str, data: json):
    '''
    Guarda los datos en formato JSON en un archivo.
    
    Parámetros:
        - instance: Nombre de la instancia del problema.
        - data: Datos a ser guardados en formato JSON.
    '''
    with open('./solutions/{}.json'.format(instance), 'w') as f:
        json.dump(data, f)

def saveSolution(instance: str, x: List[float], y: List[float], best: float):
    '''
    Guarda la solución del problema en algún formato específico.
    
    Parámetros:
        - instance: Nombre de la instancia del problema.
        - x: Lista de puntos en el eje x.
        - y: Lista de puntos en el eje y.
        - best: Mejor resultado obtenido.
    '''
    # Aquí deberías completar el código para guardar la solución en algún formato adecuado.
    pass

def plot_pwl(solution, color='g'):
    '''
    Trazar la solución de una función continua picewise linear.
    
    Parámetros:
        - solution: Diccionario que contiene los puntos de la solución.
        - color: Color de la línea de la solución.
    '''
    for i in range(solution['n'] - 1):
        plt.plot([solution['x'][i], solution['x'][i+1]], [solution['y'][i], solution['y'][i+1]], color=color)

def plot_data(data, color='k'):
    '''
    Trazar los datos del problema.
    
    Parámetros:
        - data: Diccionario que contiene los datos del problema.
        - color: Color de los puntos de datos.
    '''
    plt.plot(data['x'], data['y'],'.', color=color)