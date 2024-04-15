import json
import numpy as np
from typing import List, Tuple, Dict
import matplotlib.pyplot as plt

BIG_NUMBER = 1e10 # Revisar si es necesario.

def error_minimo_func(datos: Dict[str, any], tupla_valores: List[Tuple[float, float]]) -> float:
		
		res: float = abs(datos['y'][0] - tupla_valores[0][1])  # Error del primer punto
		
		for punto_x_pos in range(0, len(datos["x"])): #Modificar el for para que itere sobre los valores que esten entre tupla_valores[0])[0] y tupla_valores[len(tupla_valores)-1])[0]+1, que si no me equivoco son el primer y ultimo valor de X del conjunto de datos
			#Calcular la funcion de estimacion
			for valor in range(0, len(tupla_valores)-1):
				if datos["x"][punto_x_pos] > tupla_valores[valor][0] and datos["x"][punto_x_pos] <= tupla_valores[valor+1][0]:
					cociente: float = (tupla_valores[valor+1][1]-tupla_valores[valor][1])/(tupla_valores[valor+1][0]-tupla_valores[valor][0])
					estimacion_y: float = cociente*(datos["x"][punto_x_pos]-tupla_valores[valor][0]) + tupla_valores[valor][1]
					res += abs(datos["y"][punto_x_pos] - estimacion_y)
		return res


tensor: List[List[List[Tuple[(float, int, int)]]]] = []

def dynamic_programming(datos: Dict[str, any], discretizacion_x: List[float], discretizacion_y: List[float], K: int, pos_to_analize_x: int, pos_value_in_y: int, sol) -> float:
		error_minimo_hallado = sol['min_found']
		sol.update({"recursion": sol["recursion"]+1})
		
		if K == 1:
			error_min: float = BIG_NUMBER
			best_y_pos: int = None
			for pos_y in range(0, len(discretizacion_y)):
				tupla_x_y_solucion_temp: List[Tuple[float, float]] = []
				tupla_x_y_solucion_temp.append((discretizacion_x[0], discretizacion_y[pos_y]))
				tupla_x_y_solucion_temp.append((discretizacion_x[pos_to_analize_x], discretizacion_y[pos_value_in_y]))
				error: float = error_minimo_func(datos, tupla_x_y_solucion_temp)
				
				if error < error_min:
					error_min = error
					best_y_pos = pos_y
			
			sol.update({"min_found": error_min})
			tensor[pos_to_analize_x][pos_value_in_y][K-1] = (error_min, 0, best_y_pos) # best_x_pos es 0 siempre porque es el caso base
			return error_min
		
		elif pos_to_analize_x == 1 and K > 1: #pos_to_analize_x == 1 and K > 0: deberia ser K > 1 porque cambie el if de arriba
			return BIG_NUMBER

		
		elif tensor[pos_to_analize_x][pos_value_in_y][K-1] != None:
			sol.update({"precalculado": sol["precalculado"]+1})
			return tensor[pos_to_analize_x][pos_value_in_y][K-1][0]
		
		else:
			best_x_pos: int = None
			best_y_pos: int = None
			for pos_x in range(1, pos_to_analize_x):
				for pos_y in range(0, len(discretizacion_y)):
					tupla_x_y_solucion_temp: List[Tuple[float, float]] = []
					tupla_x_y_solucion_temp.append((discretizacion_x[pos_x], discretizacion_y[pos_y]))
					tupla_x_y_solucion_temp.append((discretizacion_x[pos_to_analize_x], discretizacion_y[pos_value_in_y]))
					error_first_point: float = abs(datos['y'][0] - tupla_x_y_solucion_temp[0][1])
					error_of_sub_problem = error_minimo_func(datos, tupla_x_y_solucion_temp) - error_first_point + dynamic_programming(datos, discretizacion_x, discretizacion_y, K-1, pos_x, pos_y, sol)
					
					if error_of_sub_problem < error_minimo_hallado:
						best_x_pos = pos_x
						best_y_pos = pos_y
						error_minimo_hallado = error_of_sub_problem
					
					sol.update({"min_found": error_minimo_hallado})
			
			tensor[pos_to_analize_x][pos_value_in_y][K-1] = (sol["min_found"], best_x_pos, best_y_pos)
			return error_minimo_hallado

def found_best_initial_y(datos: Dict[str, any], discretizacion_x: List[float], discretizacion_y: List[float], K: int, sol) -> float:
		res: float = BIG_NUMBER
		min_y: int = None
		for i in range(0, len(discretizacion_x)):
			tensor.append([])
			for j in range(0, len(discretizacion_y)):
				tensor[i].append([])
				for k in range(1, K+1):
					tensor[i][j].append(None)
		for pos_y in range(0, len(discretizacion_y)):
			valor: float = dynamic_programming(datos, discretizacion_x, discretizacion_y, K, len(discretizacion_x)-1, pos_y, sol)
			if valor < res:
				res = valor
				min_y = pos_y
		
		return min_y
	
def reconstruct_solution(discretizacion_x: List[float], discretizacion_y: List[float], K: int, best_pos_y_last_x: int) -> List[Tuple[int, int]]:
		res: List[Tuple[int, int]] = []
		pos_x: int = len(discretizacion_x)-1
		pos_y: int = best_pos_y_last_x
		value_K: int = K
		res.append((discretizacion_x[pos_x], discretizacion_y[pos_y]))
		while value_K > 0:
			new_pos_x = tensor[pos_x][pos_y][value_K-1][1]
			new_pos_y = tensor[pos_x][pos_y][value_K-1][2]
			value_K = value_K - 1
			pos_x = new_pos_x
			pos_y = new_pos_y
			res.append((discretizacion_x[pos_x], discretizacion_y[pos_y]))
		res.reverse()
		return res