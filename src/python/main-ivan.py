import json, time
import numpy as np
from typing import List, Tuple, Dict
import matplotlib.pyplot as plt

BIG_NUMBER = 1e10 # Revisar si es necesario.

dict_of_errors: Dict[Tuple[int, int], float] = dict()

def error_minimo_func(datos: Dict[str, any], tupla_valores: List[Tuple[float, float]]) -> float:
    
	res: float = abs(datos['y'][0] - tupla_valores[0][1])  # Error del primer punto
	#print(tupla_valores)
	for punto_x_pos in range(0, len(datos['x'])): #Modificar el for para que itere sobre los valores que esten entre tupla_valores[0])[0] y tupla_valores[len(tupla_valores)-1])[0]+1, que si no me equivoco son el primer y ultimo valor de X del conjunto de datos
		#Calcular la funcion de estimacion
		for valor in range(0, len(tupla_valores)-1):
			if datos['x'][punto_x_pos] > tupla_valores[valor][0] and datos['x'][punto_x_pos] <= tupla_valores[valor+1][0]:
				cociente: float = (tupla_valores[valor+1][1]-tupla_valores[valor][1])/(tupla_valores[valor+1][0]-tupla_valores[valor][0])
				estimacion_y: float = cociente*(datos['x'][punto_x_pos]-tupla_valores[valor][0]) + tupla_valores[valor][1]
				res += abs(datos['y'][punto_x_pos] - estimacion_y)
	return res


#  MIN_ERROR 5.927733333333335
def dynamic_programming(datos: Dict[str, any], discretizacion_x: List[float], discretizacion_y: List[float], K: int, pos_to_analize_x: int, pos_value_in_y: int, solution) -> float:
		global dict_of_errors
		solution.update({ 'recursion': solution['recursion'] + 1 })
  
		min_error = solution['min_found']
  
		if K == 1 and pos_to_analize_x > 0:
			error_min: float = BIG_NUMBER
			for pos_y in range(0, len(discretizacion_y)):
				tupla_x_y_solucion_temp = []
				tupla_x_y_solucion_temp.append((discretizacion_x[0], discretizacion_y[pos_y]))
				tupla_x_y_solucion_temp.append((discretizacion_x[pos_to_analize_x], discretizacion_y[pos_value_in_y]))
    
				error_min = min(error_min, error_minimo_func(datos, tupla_x_y_solucion_temp))
				dict_of_errors[(pos_to_analize_x, pos_y)] = min_error
	
			return error_min
		
		elif pos_to_analize_x == 0 and K > 0:
			return BIG_NUMBER

		elif (pos_to_analize_x, pos_value_in_y) in dict_of_errors.keys(): # Return pre-calculated value (x, y) = min_error
			solution.update({ 'precalculado': solution['precalculado'] + 1 })
			return dict_of_errors[(pos_to_analize_x, pos_value_in_y)]
		
		else:
			for pos_x in range(0, pos_to_analize_x):
				for pos_y in range(0, len(discretizacion_y)):
					tupla_x_y_solucion_temp: List[Tuple[float, float]] = []
					tupla_x_y_solucion_temp.append((discretizacion_x[pos_x], discretizacion_y[pos_y]))
					tupla_x_y_solucion_temp.append((discretizacion_x[pos_to_analize_x], discretizacion_y[pos_value_in_y]))
					first_point_error:float = abs(datos['y'][0] - tupla_x_y_solucion_temp[0][1])
					error_of_sub_problem = error_minimo_func(datos, tupla_x_y_solucion_temp)-first_point_error + dynamic_programming(datos, discretizacion_x, discretizacion_y, K-1, pos_x, pos_y, solution)
					min_error = min(min_error, error_of_sub_problem)
					solution.update({'min_found': min_error})
			
			dict_of_errors[(pos_x, pos_y)] = min_error
			return min_error


def found_best_initial_y(datos: Dict[str, any], discretizacion_x: List[float], discretizacion_y: List[float], K: int, solution) -> float:
	res: float = BIG_NUMBER
	for pos_y in range(0, len(discretizacion_y)):
		res = min(res, dynamic_programming(datos, discretizacion_x, discretizacion_y, K, len(discretizacion_x)-1, pos_y, solution))
	return res


def main():
	with open('../../data/titanium.json') as f:
		instance = json.load(f)
	
	m = 6
	n = 6
	K = 5
	
	start = time.time()
	# Ejemplo para definir una grilla de m x n.
	grid_x = np.linspace(min(instance['x']), max(instance['x']), num=m, endpoint=True)
	grid_y = np.linspace(min(instance['y']), max(instance['y']), num=n, endpoint=True)
		
	solution = { 'min_found': BIG_NUMBER, 'precalculado': 0, 'recursion': 0}
	print(found_best_initial_y(instance, grid_x, grid_y, K, solution))
	end = time.time()

	print('elapsed', end - start)
 
	print(solution)

	
if __name__ == '__main__':
	main()