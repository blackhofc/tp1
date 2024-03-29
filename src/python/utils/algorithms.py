from typing import *
import json

BIG_NUMBER = 1e10 # Check if needed.

def e(x: float, y: float):
    
    return

def y(x: Tuple[float, float], y: Tuple[float,float]):
    
    return

def line(t_prime, y_prime, t_double_prime, y_double_prime, t):
    """
    Calcula la recta que une dos puntos dados.
    """
    
    return ((y_double_prime - y_prime) / (t_double_prime - t_prime)) * (t - t_prime) + y_prime

def absolut_error(xi, yi, t_prime, y_prime, t_double_prime, y_double_prime):
    """
    Calcula el error absoluto de aproximación por la recta en el punto xi.
    """
    y_predicho = line(t_prime, y_prime, t_double_prime, y_double_prime, xi)
    return abs(yi - y_predicho)


def error_minimo_func(datos: Dict[str, any], tupla_valores: List[Tuple[float, float]]) -> float:
		res: float = 0
		# print(tupla_valores)
		for punto_x_pos in range(0, len(datos["x"])): # Modificar el for para que itere sobre los valores que esten entre tupla_valores[0])[0] y tupla_valores[len(tupla_valores)-1])[0]+1, que si no me equivoco son el primer y ultimo valor de X del conjunto de datos
			#Calcular la funcion de estimacion
			for valor in range(0, len(tupla_valores)-1):
				if datos["x"][punto_x_pos] > tupla_valores[valor][0] and datos["x"][punto_x_pos] <= tupla_valores[valor+1][0]:
					cociente: float = (tupla_valores[valor+1][1]-tupla_valores[valor][1])/(tupla_valores[valor+1][0]-tupla_valores[valor][0])
					estimacion_y: float = cociente*(datos["x"][punto_x_pos]-tupla_valores[valor][0]) + tupla_valores[valor][1]
					res += abs(datos["y"][punto_x_pos] - estimacion_y)
		return res

def brute_force(datos: Dict[str, any], discretizacion_x: List[float], discretizacion_y: List[float], K: int, pos_analizar_x: int, tupla_x_y_solucion: List[Tuple[float, float]]) -> float:
	global solucion_temp
	global error_minimo_hallado
	min_error: float = BIG_NUMBER
	if K == 0:
		if error_minimo_func(datos, tupla_x_y_solucion) < error_minimo_hallado:
			error_minimo_hallado = error_minimo_func(datos, tupla_x_y_solucion)
			solucion_temp = list(tupla_x_y_solucion)
			return error_minimo_hallado
		return min_error
	
	elif K > len(discretizacion_x) - pos_analizar_x:
		return min_error

	#print(pos_analizar_x, "posicion x")
	error_no_tomando_x = brute_force(datos, discretizacion_x, discretizacion_y, K, pos_analizar_x + 1, tupla_x_y_solucion)
	for pos_y in range(0, len(discretizacion_y)):
		tupla_x_y_solucion_temp: List[Tuple[float, float]] = list(tupla_x_y_solucion)
		tupla_x_y_solucion_temp.append((discretizacion_x[pos_analizar_x], discretizacion_y[pos_y]))
		#discretizacion_x_temp: List[float] = list(discretizacion_x)
		#discretizacion_x_temp.pop(pos_analizar_x)
		# Arreglar para tener en cuenta que SI O SI tienen que estar la primera y ultima posicion de la discretizacion de x (casi seguro)
		error_tomando_x = brute_force(datos, discretizacion_x, discretizacion_y, K-1, pos_analizar_x + 1, tupla_x_y_solucion_temp)
		error_minimo_hallado = min(error_minimo_hallado, error_tomando_x, error_no_tomando_x)
	# fuerza_bruta(datos, discretizacion_x_temp, discretizacion_y, K-1, pos_analizar_x+1, pos_analizar_y, tupla_x_y_solucion_temp)
  
	return min_error



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