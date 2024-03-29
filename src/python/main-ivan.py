import json
import numpy as np
from typing import List, Tuple, Dict
import matplotlib.pyplot as plt

BIG_NUMBER = 1e10 # Revisar si es necesario.
error_minimo_hallado = float("inf")
solucion_temp: List[Tuple[float, float]] = []

def main():

	# Ejemplo para leer una instancia con json
	instance_name = "titanium.json"
	filename = "./data/" + instance_name
	with open(filename) as f:
		instance = json.load(f)
	
	K = instance["n"]
	m = 6
	n = 6
	N = 5
	
	# Ejemplo para definir una grilla de m x n.
	grid_x = np.linspace(min(instance["x"]), max(instance["x"]), num=m, endpoint=True)
	grid_y = np.linspace(min(instance["y"]), max(instance["y"]), num=n, endpoint=True)

	def error_minimo_func(datos: Dict[str, any], tupla_valores: List[Tuple[float, float]]) -> float:
		res: float = 0
		#print(tupla_valores)
		for punto_x_pos in range(0, len(datos["x"])): #Modificar el for para que itere sobre los valores que esten entre tupla_valores[0])[0] y tupla_valores[len(tupla_valores)-1])[0]+1, que si no me equivoco son el primer y ultimo valor de X del conjunto de datos
			#Calcular la funcion de estimacion
			for valor in range(0, len(tupla_valores)-1):
				if datos["x"][punto_x_pos] > tupla_valores[valor][0] and datos["x"][punto_x_pos] <= tupla_valores[valor+1][0]:
					cociente: float = (tupla_valores[valor+1][1]-tupla_valores[valor][1])/(tupla_valores[valor+1][0]-tupla_valores[valor][0])
					estimacion_y: float = cociente*(datos["x"][punto_x_pos]-tupla_valores[valor][0]) + tupla_valores[valor][1]
					res += abs(datos["y"][punto_x_pos] - estimacion_y)
		return res

	def fuerza_bruta(datos: Dict[str, any], discretizacion_x: List[float], discretizacion_y: List[float], K: int, pos_analizar_x: int, tupla_x_y_solucion: List[Tuple[float, float]]) -> float:
		global solucion_temp
		global error_minimo_hallado
		if K == 0:
			if error_minimo_func(datos, tupla_x_y_solucion) < error_minimo_hallado and tupla_x_y_solucion[0][0] == discretizacion_x[0] and tupla_x_y_solucion[len(tupla_x_y_solucion)-1][0] == discretizacion_x[len(discretizacion_x)-1]:
				error_minimo_hallado = error_minimo_func(datos, tupla_x_y_solucion)
				solucion_temp = list(tupla_x_y_solucion)
				return error_minimo_hallado
			return 99999
		
		elif K > len(discretizacion_x) - pos_analizar_x:
			return 99999
		#elif pos_analizar_y == len(discretizacion_y):
			
			#fuerza_bruta(datos, discretizacion_x, discretizacion_y, K-1, pos_analizar_x+1, 0, tupla_x_y_solucion)
		else:
			error_minimo: float = 99999
			#print(pos_analizar_x, "posicion x")
			error_no_tomando_x = fuerza_bruta(datos, discretizacion_x, discretizacion_y, K, pos_analizar_x+1, tupla_x_y_solucion)
			for pos_y in range(0, len(discretizacion_y)):
				tupla_x_y_solucion_temp: List[Tuple[float, float]] = list(tupla_x_y_solucion)
				tupla_x_y_solucion_temp.append((discretizacion_x[pos_analizar_x], discretizacion_y[pos_y]))
				#discretizacion_x_temp: List[float] = list(discretizacion_x)
				#discretizacion_x_temp.pop(pos_analizar_x)
				#arreglar para tener en cuenta que SI O SI tienen que estar la primera y ultima posicion de la discretizacion de x (casi seguro)
				error_tomando_x = fuerza_bruta(datos, discretizacion_x, discretizacion_y, K-1, pos_analizar_x+1, tupla_x_y_solucion_temp)
				error_minimo_hallado = min(error_minimo_hallado, error_tomando_x, error_no_tomando_x)
			#fuerza_bruta(datos, discretizacion_x_temp, discretizacion_y, K-1, pos_analizar_x+1, pos_analizar_y, tupla_x_y_solucion_temp)
			return error_minimo
		
	discretizacion_x: List[float] = [595,691,787,883,979,1075]
	discretizacion_y: List[float] = [0.601, 0.9146, 1.2282, 1.5418, 1.8554, 2.169]

	#plt.scatter(instance["x"], instance["y"])

	instance_name = "optimistic_instance.json"
	filename = "./data/" + instance_name
	with open(filename) as f:
		instance_optimistic = json.load(f)

	variacion_discretizacion_x: float = (instance_optimistic["x"][instance_optimistic["n"]-1] - instance_optimistic["x"][0])/(6-1)
	variacion_discretizacion_y: float = (instance_optimistic["y"][instance_optimistic["n"]-1] - instance_optimistic["y"][0])/(6-1)
	discretizacion_x_optimistic: List[float] = [instance_optimistic["x"][0] + (x)*variacion_discretizacion_x for x in range(0, 6)]
	discretizacion_y_optimistic: List[float] = [instance_optimistic["y"][0] + (y)*variacion_discretizacion_y for y in range(0, 6)]

	print(discretizacion_x_optimistic, discretizacion_y_optimistic)

	

	print(fuerza_bruta(instance, discretizacion_x, discretizacion_y, 5, 0, []))
	print(solucion_temp, "termino", error_minimo_hallado)

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
	with open('solution_' + instance_name, 'w') as f:
		json.dump(solution, f)

	
if __name__ == "__main__":
	main()