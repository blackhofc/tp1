from typing import *
import json

BIG_NUMBER = 1e10 # Check if needed.

def e(x: float, y: float):
    
    return

def y(x: Tuple[float, float], y: Tuple[float,float]):
    
    return

def line(t_prime, y_prime, t_double_prime, y_double_prime, t):
    '''
    Calcula la recta que une dos puntos dados.
    '''
    
    return ((y_double_prime - y_prime) / (t_double_prime - t_prime)) * (t - t_prime) + y_prime

def absolut_error(xi, yi, t_prime, y_prime, t_double_prime, y_double_prime):
    '''
    Calcula el error absoluto de aproximación por la recta en el punto xi.
    '''
    y_predicho = line(t_prime, y_prime, t_double_prime, y_double_prime, xi)
    return abs(yi - y_predicho)


def calculate_min_error(instance:json, tupla_valores: List[Tuple[float, float]]) -> float:
		res: float = 0
		#print(tupla_valores)
		for punto_x_pos in range(0, len(instance["x"])): #Modificar el for para que itere sobre los valores que esten entre tupla_valores[0])[0] y tupla_valores[len(tupla_valores)-1])[0]+1, que si no me equivoco son el primer y ultimo valor de X del conjunto de datos
			#Calcular la funcion de estimacion
			for valor in range(0, len(tupla_valores)-1):
				if instance["x"][punto_x_pos] > tupla_valores[valor][0] and instance["x"][punto_x_pos] <= tupla_valores[valor+1][0]:
					cociente: float = (tupla_valores[valor+1][1]-tupla_valores[valor][1])/(tupla_valores[valor+1][0]-tupla_valores[valor][0])
					estimacion_y: float = cociente*(instance["x"][punto_x_pos]-tupla_valores[valor][0]) + tupla_valores[valor][1]
					res += abs(instance["y"][punto_x_pos] - estimacion_y)
		return res

def brute_force(instance:json, grid_x: List[float], grid_y: List[float], K: int, pos_x: int, temp_solution: List[Tuple[float, float]], solution) -> float:

    # TODO: PREV |grid_x| < k (hacer prev y post)
    min_error_found = solution['min_found']
    #print('K', K)
    if K == 0:
        current_min = calculate_min_error(instance, temp_solution)
        if current_min < min_error_found and temp_solution[0][0] == grid_x[0] and temp_solution[len(temp_solution)-1][0] == grid_x[len(grid_x)-1]:
            min_error_found = calculate_min_error(instance, temp_solution)
            solution.update({'solution': temp_solution.copy(), 'min_found': min_error_found})
            return min_error_found
        return BIG_NUMBER
	
    elif K > len(grid_x) - pos_x:
        return BIG_NUMBER

    else:
        error_without_x = brute_force(instance, grid_x, grid_y, K, pos_x+1, temp_solution, solution)
        for pos_y in range(0, len(grid_y)):
            current_sol: List[Tuple[float, float]] = list(temp_solution)
            current_sol.append((grid_x[pos_x], grid_y[pos_y]))
            # TODO: Arreglar para tener en cuenta que SI O SI tienen que estar la primera y ultima posicion de la discretizacion de x (casi seguro)
            error_with_x = brute_force(instance, grid_x, grid_y, K-1, pos_x+1, current_sol, solution)
            min_error_found = min(min_error_found, error_with_x, error_without_x)
            solution.update({'min_found': min_error_found})

    return min_error_found



'''
Para el primer segmento, 1 = 595, r2 = 787, y la pieza f1(t) se obtiene mediante la función lineal 
que une los puntos (595,0.601) y (787,0.601), siguiendo la ecuación (1). Análogamente, la pieza f2(t) 
tiene dominio [r2, r3] = [787, 883] y la función f2(t) se obtiene aplicando la ecuación (1) tomando
como referencia los puntos (787, 0.601) y (883, 1.228). Notar que una función continua PWL
puede ser definida en términos de K puntos dados por (rk, fk(rk)) para k = 1, . . . , K - 1 y
(rK, fK-1(rK)).
Finalmente, analizamos el error de la aproximación. Dada una pieza fk(t) definida por los
breakpoints (rk, zk) y (rk+1, zk+1) y los puntos (xi
, yi), i = 1, . . . , n, definimos el error de
aproximación de la pieza k-ésima como la suma de los errores de los puntos (xi
, yi) tal que
xi ∈ (rk, rk+1], es decir,

'''

def brute(instance: json) -> List[Tuple[int, int]]:
    for x, y in zip(instance['x'], instance['y']):
        # error = absolut_error(xi, yi, t_prime, y_prime, t_double_prime, y_double_prime)

        print('X: {} Y: {}'.format(x, y))
    return [(0, 0), (1, 0), (2, 0), (3, 2), (4, 0), (5, 0)]

def backtrack(instance: json) -> List[Tuple[int, int]]:
    return []

def dynamic(instance: json) -> List[Tuple[int, int]]:
    return []