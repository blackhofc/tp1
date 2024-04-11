import json
import numpy as np
from typing import List, Tuple, Dict
import matplotlib.pyplot as plt

BIG_NUMBER = 1e10 # Revisar si es necesario.

def main():

	with open('../../data/optimistic_instance.json') as f:
		instance = json.load(f)
	
	K = instance["n"]
	m = 6
	n = 6
	N = 5
	
	# Ejemplo para definir una grilla de m x n.
	grid_x = np.linspace(min(instance["x"]), max(instance["x"]), num=m, endpoint=True)
	grid_y = np.linspace(min(instance["y"]), max(instance["y"]), num=n, endpoint=True)
	print(grid_x)
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

	def fuerza_bruta(datos: Dict[str, any], discretizacion_x: List[float], discretizacion_y: List[float], K: int, pos_analizar_x: int, tupla_x_y_solucion: List[Tuple[float, float]], sol) -> float:
		
		error_minimo_hallado = sol['min_found']

		if K == 0:

			if error_minimo_func(datos, tupla_x_y_solucion) < error_minimo_hallado and tupla_x_y_solucion[0][0] == discretizacion_x[0] and tupla_x_y_solucion[len(tupla_x_y_solucion)-1][0] == discretizacion_x[len(discretizacion_x)-1]:
				error_minimo_hallado = error_minimo_func(datos, tupla_x_y_solucion)
				sol.update({'temp_sol': tupla_x_y_solucion.copy(), 'min_found': error_minimo_hallado})
				return error_minimo_hallado

			return BIG_NUMBER
		
		elif K > len(discretizacion_x) - pos_analizar_x:
			return BIG_NUMBER

		else:
			error_no_tomando_x = fuerza_bruta(datos, discretizacion_x, discretizacion_y, K, pos_analizar_x+1, tupla_x_y_solucion, sol)
			for pos_y in range(0, len(discretizacion_y)):
				tupla_x_y_solucion_temp: List[Tuple[float, float]] = list(tupla_x_y_solucion)
				tupla_x_y_solucion_temp.append((discretizacion_x[pos_analizar_x], discretizacion_y[pos_y]))
				# TODO: Arreglar para tener en cuenta que SI O SI tienen que estar la primera y ultima posicion de la discretizacion de x (casi seguro)
				error_tomando_x = fuerza_bruta(datos, discretizacion_x, discretizacion_y, K-1, pos_analizar_x+1, tupla_x_y_solucion_temp, sol)
				error_minimo_hallado = min(error_minimo_hallado, error_tomando_x, error_no_tomando_x)
				sol.update({'min_found': error_minimo_hallado})
    
			return error_minimo_hallado 
		
	discretizacion_x: List[float] = [595,691,787,883,979,1075]
	discretizacion_y: List[float] = [0.601, 0.9146, 1.2282, 1.5418, 1.8554, 2.169]
 
	sol = {'min_found': BIG_NUMBER}
	print(fuerza_bruta(instance, grid_x, grid_y, 5, 0, [], sol))
	print(sol['temp_sol'], "termino", sol['min_found'])
 

	dict_of_errors: Dict[Tuple[int, int], float] = dict()
	tensor: List[List[List[Tuple[(float, int, int)]]]] = []

	def dynamic_programming(datos: Dict[str, any], discretizacion_x: List[float], discretizacion_y: List[float], K: int, pos_to_analize_x: int, pos_value_in_y: int, sol) -> float:
			error_minimo_hallado = sol['min_found']
			#print(sol)
			sol.update({"recursion": sol["recursion"]+1})
			if K == 1: # es pos_to_analize_x >= 0 o pos_to_analize_x > 0
				error_min: float = BIG_NUMBER
				for pos_y in range(0, len(discretizacion_y)):
					tupla_x_y_solucion_temp: List[Tuple[float, float]] = []
					tupla_x_y_solucion_temp.append((discretizacion_x[0], discretizacion_y[pos_y]))
					tupla_x_y_solucion_temp.append((discretizacion_x[pos_to_analize_x], discretizacion_y[pos_value_in_y]))
					error: float = error_minimo_func(datos, tupla_x_y_solucion_temp)
					error_min = min(error_min, error)
				#dict_of_errors[(pos_to_analize_x, pos_value_in_y)] = error_min
				#if best_y_pos != None:
					#print(discretizacion_x[0], discretizacion_y[best_y_pos], "caso base")
				sol.update({"min_found": error_min})
				#tensor[pos_to_analize_x][pos_value_in_y][K-1] = (error_min, 0, best_y_pos) # best_x_pos es 0 siempre porque es el caso base
				return error_min
			
			elif pos_to_analize_x == 1 and K > 1: #pos_to_analize_x == 1 and K > 0: deberia ser K > 1 porque cambie el if de arriba
				return BIG_NUMBER

			#elif (pos_to_analize_x, pos_value_in_y) in dict_of_errors.keys():
				#sol.update({"precalculado": sol["precalculado"]+1})
				#return dict_of_errors[(pos_to_analize_x, pos_value_in_y)]
			
			elif tensor[pos_to_analize_x][pos_value_in_y][K-1] != None:
				sol.update({"precalculado": sol["precalculado"]+1})
				return tensor[pos_to_analize_x][pos_value_in_y][K-1][0]
			
			else:
				for pos_x in range(1, pos_to_analize_x):
					for pos_y in range(0, len(discretizacion_y)):
						tupla_x_y_solucion_temp: List[Tuple[float, float]] = []
						tupla_x_y_solucion_temp.append((discretizacion_x[pos_x], discretizacion_y[pos_y]))
						tupla_x_y_solucion_temp.append((discretizacion_x[pos_to_analize_x], discretizacion_y[pos_value_in_y]))
						error_first_point: float = abs(datos['y'][0] - tupla_x_y_solucion_temp[0][1])
						error_of_sub_problem = error_minimo_func(datos, tupla_x_y_solucion_temp) - error_first_point + dynamic_programming(datos, discretizacion_x, discretizacion_y, K-1, pos_x, pos_y, sol)
						error_minimo_hallado = min(error_minimo_hallado, error_of_sub_problem)
						sol.update({"min_found": error_minimo_hallado})
				#dict_of_errors[(pos_x, pos_y)] = sol["min_found"]
				#if best_x_pos != None and best_y_pos != None:
					#print(discretizacion_x, discretizacion_y[best_y_pos], "else")
					#sol.update({"list_sol": sol["list_sol"].copy().append((discretizacion_x[best_x_pos], discretizacion_y[best_y_pos]))})
				#tensor[pos_to_analize_x][pos_value_in_y][K-1] = (sol["min_found"], best_x_pos, best_y_pos)
				return error_minimo_hallado

	def found_best_initial_y(datos: Dict[str, any], discretizacion_x: List[float], discretizacion_y: List[float], K: int, sol) -> float:
			res: float = BIG_NUMBER
			for i in range(0, len(discretizacion_x)):
				tensor.append([])
				for j in range(0, len(discretizacion_y)):
					tensor[i].append([])
					for k in range(1, K+1):
						tensor[i][j].append(None)
			for pos_y in range(0, len(discretizacion_y)):
				valor: float = dynamic_programming(datos, discretizacion_x, discretizacion_y, K, len(discretizacion_x)-1, pos_y, sol)
				res = min(res, valor)
			return res
		
	def reconstruct_solution(discretizacion_x: List[float], K: int, best_pos_y_last_x: int) -> List[Tuple[int, int]]:
			res: List[Tuple[int, int]] = []
			pos_x: int = len(discretizacion_x)-1
			pos_y: int = best_pos_y_last_x
			value_K: int = K
			while pos_x >= 0:
				res.append((pos_x, pos_y))
				new_pos_x = tensor[pos_x][pos_y][value_K][1]
				new_pos_x = tensor[pos_x][pos_y][value_K][1]
				value = K - 1
				pos_x = new_pos_x
				pos_y = pos_x

			return res



	#plt.scatter(instance["x"], instance["y"])
	#plt.show()

	#instance_name = "optimistic_instance.json"
	#filename = "./data/" + instance_name
	#with open(filename) as f:
		#instance_optimistic = json.load(f)

	#m: int = 10
	#n: int = 20

	#variacion_discretizacion_x: float = (instance["x"][instance["n"]-1] - instance["x"][0])/(n-1)
	#variacion_discretizacion_y: float = (instance["y"][instance["n"]-1] - instance["y"][0])/(m-1)
	#discretizacion_x_optimistic: List[float] = [instance["x"][0] + (x)*variacion_discretizacion_x for x in range(0, n)]
	#discretizacion_y_optimistic: List[float] = [instance["y"][0] + (y)*variacion_discretizacion_y for y in range(0, m)]

	print(grid_x, grid_y)

	solution = {'min_found': BIG_NUMBER, "precalculado": 0, "recursion": 0, "list_sol": []}

	print(found_best_initial_y(instance, grid_x, grid_y, 4, solution))
	print(solution)
	print(reconstruct_solution(grid_x, grid_y, 4, 0))
	#print(reconstruct_solution())
	#print(dict_of_errors[(discretizacion_x[len(discretizacion_x)-1], discretizacion_y[0])])
	#print(fuerza_bruta(instance, discretizacion_x, discretizacion_y, 5, 0, []))
	#print(solucion_temp, "termino", error_minimo_hallado)

	#plt.scatter(instance_optimistic["x"], instance_optimistic["y"])
	#plt.plot([solucion_temp[1][0], solucion_temp[2][0]], [solucion_temp[1][1], solucion_temp[2][1]], color = "red")
	#plt.show()

	

	#print(error_minimo_func(instance, [(595, 0.601), (691, 0.601), (787, 0.601), (883, 1.2282), (979, 0.601), (1075, 0.601)]))

	best = {}
	best['sol'] = [None]*(N+1)
	best['obj'] = BIG_NUMBER
	
	# Posible ejemplo (para la instancia titanium) de formato de solucion, y como exportarlo a JSON.
	# La solucion es una lista de tuplas (i,j), donde:
	# - i indica el indice del punto de la discretizacion de la abscisa
	# - j indica el indice del punto de la discretizacion de la ordenada.
	best['sol'] = [(0, 0), (1, 0), (2, 0), (3, 2), (4, 0), (5, 0)]
	best['obj'] = 5.927733333333335

	# Represetnamos la solucion con un diccionario que indica:
	# - n: cantidad de breakpoints
	# - x: lista con las coordenadas de la abscisa para cada breakpoint
	# - y: lista con las coordenadas de la ordenada para cada breakpoint
	solution = {}
	solution['n'] = len(best['sol'])
	solution['x'] = [grid_x[x[0]] for x in best['sol']]
	solution['y'] = [grid_y[x[1]] for x in best['sol']]
	solution['obj'] = best['obj']

	# Se guarda el archivo en formato JSON
	#with open('solution_' + instance, 'w') as f:
		#json.dump(solution, f)

	
if __name__ == "__main__":
	main()