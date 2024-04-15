from typing import *
import json

BIG_NUMBER = 1e10  # Check if needed.
HUGE_NUMBER = 1e20

def e(x: float, y: float):

    return


def y(x: Tuple[float, float], y: Tuple[float, float]):

    return


def line(t_prime, y_prime, t_double_prime, y_double_prime, t):
    """
    Calcula la recta que une dos puntos dados.
    """

    return ((y_double_prime - y_prime) / (t_double_prime - t_prime)) * (
        t - t_prime
    ) + y_prime


def absolut_error(xi, yi, t_prime, y_prime, t_double_prime, y_double_prime):
    """
    Calcula el error absoluto de aproximación por la recta en el punto xi.
    """
    y_predicho = line(t_prime, y_prime, t_double_prime, y_double_prime, xi)
    return abs(yi - y_predicho)


def calculate_min_error(instance: json, solution: List[Tuple[float, float]]) -> float:
    """Toma un conjunto de datos y una lista de breakpoints y devuelve el error total del ajuste picewise lienar correspondiente.
    Requiere un conjunto de datos no vacío y al menos 2 breakpoints.
    """
    # TODO: Use absolut_error, line functions and replace this one
    # print(tupla_valores)

    min_error: float = abs(instance["y"][0] - solution[0][1])  # Error del primer punto

    for point in range(0, len(instance["x"])):

        for sol_index in range(0, len(solution) - 1):
            if (
                instance["x"][point] > solution[sol_index][0]
                and instance["x"][point] <= solution[sol_index + 1][0]
            ):
                # Calcula el error absoluto de cada partición entre r_k < x <= r_k+1
                # como el valor absoluto de la diferencia entre el dato y la estimación dada por la función f_k
                delta: float = (solution[sol_index + 1][1] - solution[sol_index][1]) / (
                    solution[sol_index + 1][0] - solution[sol_index][0]
                )
                estimacion_y: float = (
                    delta * (instance["x"][point] - solution[sol_index][0])
                    + solution[sol_index][1]
                )
                # Se acumula el error absoluto total
                min_error += abs(instance["y"][point] - estimacion_y)

    return min_error


def brute_force_bis(
    instance: json,
    grid_x: List[float],
    grid_y: List[float],
    K: int,
    pos_x: int,
    temp_solution: List[Tuple[float, float]],
    solution,
) -> float:
    """Función recursiva llamada por brute_force.
    Toma los mismos requerimientos junto con un índice para la grilla x (inicializado en 0), una solución temporal que se va construyendo
    y una solución óptima que será efectivamente la óptima al terminar la recursión."""

    min_error_found = solution["min_found"]
    solution["recursion"] += 1

    # TODO: COMENTAR
    if pos_x == len(grid_x):

        # Caso base 2, si ya no hay breakpoints que asignar, ya se tiene armada la solución final.
        # Basta con calcular el error absoluto correspondiente a la solución actual y ver si es menor que el de la solución óptima hasta el momento.
        if K == 0:
            current_min = calculate_min_error(instance, temp_solution)
            if (
                (current_min < min_error_found)
                and (temp_solution[0][0] == grid_x[0])
                and (
                    temp_solution[len(temp_solution) - 1][0] == grid_x[len(grid_x) - 1]
                )
            ):
                solution.update(
                    {"solution": temp_solution.copy(), "min_found": current_min}
                )
                return current_min
            return BIG_NUMBER

        elif K > 0:
            return BIG_NUMBER

    # Caso recursivo, se considera agregar o no la coordenada de x actual (x_1) a la solución.
    # En caso de agregarse, considero todos los puntos de la forma (x_1, *) donde * es un valor perteneciente a la grilla y.
    # Se consideran entonces todas las posibles coordenadas válidas en x_1 como parte de la solución. Se recursan n+1 veces siendo n el tamaño de la grilla y.
    else:
        error_without_x = brute_force_bis(
            instance, grid_x, grid_y, K, pos_x + 1, temp_solution, solution
        )
        for pos_y in range(0, len(grid_y)):
            current_sol: List[Tuple[float, float]] = list(temp_solution)
            current_sol.append((grid_x[pos_x], grid_y[pos_y]))

            error_with_x = brute_force_bis(
                instance, grid_x, grid_y, K - 1, pos_x + 1, current_sol, solution
            )
            min_error_found = min(min_error_found, error_with_x, error_without_x)

            solution.update({"min_found": min_error_found})

    return min_error_found


def brute_force(
    instance: json, grid_x: List[float], grid_y: List[float], K: int
) -> json:
    """Toma un conjunto de datos, una discretización en X y en Y, y una cantidad K >= 2 de breakpoints.
    Devuelve un json con una lista con K breakpoints pertenecientes a la discretización tal que se minimice el error absoluto al armar una función continua picewise linear en función a los breakpoints.
    """
    solution = {"min_found": BIG_NUMBER, "recursion": 0}

    # Inicializo la función recursiva auxiliar.
    brute_force_bis(instance, grid_x, grid_y, K, 0, [], solution)
    return solution


def backtrack_bis(
    instance: json,
    grid_x: List[float],
    grid_y: List[float],
    K: int,
    pos_x: int,
    temp_solution: List[Tuple[float, float]],
    solution,
) -> float:

    min_error_found = solution["min_found"]
    solution["recursion"] += 1
    # Poda factibilidad
    if K == 0:
        current_min = calculate_min_error(instance, temp_solution)
        if (
            current_min < min_error_found
            and temp_solution[0][0] == grid_x[0]
            and temp_solution[len(temp_solution) - 1][0] == grid_x[len(grid_x) - 1]
        ):
            solution.update(
                {"solution": temp_solution.copy(), "min_found": current_min}
            )
            return current_min
        return BIG_NUMBER

    # Si se requieren más breakpoints de los que se pueden asignar, se devuelve un error muy grande para indicar que no hay un ajuste compatible con los parámetros tomados.
    # Poda factibilidad
    elif K > len(grid_x) - pos_x:
        return BIG_NUMBER

    # Poda factibilidad
    elif pos_x > 0 and len(temp_solution) > 0 and temp_solution[0][0] != grid_x[0]:
        return BIG_NUMBER

    # Poda optimalidad
    elif (
        len(temp_solution) > 0
        and calculate_min_error(instance, temp_solution) > min_error_found
    ):
        return BIG_NUMBER

    else:
        error_without_x = backtrack_bis(
            instance, grid_x, grid_y, K, pos_x + 1, temp_solution, solution
        )
        for pos_y in range(0, len(grid_y)):
            current_sol: List[Tuple[float, float]] = list(temp_solution)
            current_sol.append((grid_x[pos_x], grid_y[pos_y]))

            error_with_x = backtrack_bis(
                instance, grid_x, grid_y, K - 1, pos_x + 1, current_sol, solution
            )
            min_error_found = min(min_error_found, error_with_x, error_without_x)

            solution.update({"min_found": min_error_found})

    return min_error_found


def backtrack(instance: json, grid_x: List[float], grid_y: List[float], K: int) -> json:
    """Toma un conjunto de datos, una discretización en X y en Y, y una cantidad K >= 2 de breakpoints.
    Devuelve un json con una lista con K breakpoints pertenecientes a la discretización tal que se minimice el error absoluto al armar una función continua picewise linear en función a los breakpoints.
    """
    solution = {"min_found": BIG_NUMBER, "recursion": 0}

    # Inicializo la función recursiva auxiliar.
    backtrack_bis(instance, grid_x, grid_y, K, 0, [], solution)
    return solution


def dynamic_error(instance: json, solution: List[Tuple[float, float]]) -> float:
    """Toma un conjunto de datos y una lista de breakpoints y devuelve el error total del ajuste picewise lienar correspondiente.
    Requiere un conjunto de datos no vacío y al menos 2 breakpoints.
    """
    error = 0
    if solution[0][0] == instance["x"][0]:
        error += abs(instance["y"][0] - solution[0][1])

    for point in range(0, len(instance["x"])):
        if (
            instance["x"][point] > solution[0][0]
            and instance["x"][point] <= solution[1][0]
        ):
            # Calcula el error absoluto de cada partición entre r_k < x <= r_k+1
            # como el valor absoluto de la diferencia entre el dato y la estimación dada por la función f_k
            delta: float = (solution[1][1] - solution[0][1]) / (
                solution[1][0] - solution[0][0]
            )
            estimacion_y: float = (
                delta * (instance["x"][point] - solution[0][0]) + solution[0][1]
            )
            # Se acumula el error absoluto total
            error += abs(instance["y"][point] - estimacion_y)

    return error


def dynamic(instance: json, grid_x: List[float], grid_y: List[float], K: int) -> float:
    # Definimos memo como un tensor con dimensiones k, i, y j, tales que
    # memo[k][i][j] = F_[k+1] (grid_x[i], grid_y[j])
    memo = []
    for k in range(0, K - 1):
        memo.append([])
        for i in range(0, len(grid_x)):
            memo[k].append([])
            for j in range(0, len(grid_y)):
                memo[k][i].append([BIG_NUMBER, []])

    # Inicializo con caso base M = 1, sin tener en cuenta cuando el eje candidato es == al eje evaluado
    for i in range(1, len(grid_x)):
        for j in range(0, len(grid_y)):
            # para todos los puntos le calculo el F1 como el menor error entre el punto (xi, yj) y algun (x0, yl)
            temp_min = BIG_NUMBER
            minIndex = -1
            for yCandidate in range(0, len(grid_y)):
                temp_solution = [
                    (grid_x[0], grid_y[yCandidate]),
                    (grid_x[i], grid_y[j]),
                ]

                error = dynamic_error(instance, temp_solution)

                if error < temp_min:
                    temp_min = error
                    minIndex = yCandidate

            memo[0][i][j][0] = temp_min
            memo[0][i][j][1] = (0, minIndex)

    # Con esto me armé los casos bases GOOOOD (asumo)

    # Ahora encaro el armado más molesto
    for k in range(1, K - 1):
        for i in range(2, len(grid_x)):
            for j in range(0, len(grid_y)):
                # para todos los puntos le calculo el F_M como
                temp_min = BIG_NUMBER
                minIndex = [-1, -1]
                for xCandidate in range(1, i):
                    for yCandidate in range(0, len(grid_y)):
                        temp_solution = [
                            (grid_x[xCandidate], grid_y[yCandidate]),
                            (grid_x[i], grid_y[j]),
                        ]
                        tempF = (
                            dynamic_error(instance, temp_solution)
                            + memo[k - 1][xCandidate][yCandidate][0]
                        )

                        if tempF < temp_min:
                            temp_min = tempF
                            minIndex = [xCandidate, yCandidate]

                memo[k][i][j][0] = temp_min
                memo[k][i][j][1] = (minIndex[0], minIndex[1])

    absoluteMin = BIG_NUMBER
    for yCandidate in range(0, len(grid_y)):
        absoluteMin = min(absoluteMin, memo[K - 2][len(grid_x) - 1][yCandidate][0])

    # Reconstruyo la solución
    solution = {}
    solution["min_error"] = absoluteMin
    solution["x"] = [0] * K
    solution["y"] = [0] * K

    # El último breakpoint se consigue fácil
    currentMin = BIG_NUMBER
    for j in range(0, len(grid_y)):
        currentValue = memo[K - 2][len(grid_x) - 1][j][0]
        if currentValue < currentMin:
            currentMin = currentValue
            solIndexY = j

    solution["x"][K - 1] = grid_x[len(grid_x) - 1]
    solution["y"][K - 1] = grid_y[solIndexY]

    # Recupero el resto
    k_index = K - 1
    solIndexX = len(grid_x) - 1
    while k_index > 0:
        indexes = memo[k_index - 1][solIndexX][solIndexY][1]
        print(indexes)
        solution["x"][k_index - 1] = grid_x[indexes[0]]
        solution["y"][k_index - 1] = grid_y[indexes[1]]
        solIndexY = indexes[1]
        solIndexX = indexes[0]
        k_index -= 1

    print(solution)

    return absoluteMin


"""
The algorithm includes conditional statements to avoid exploring certain branches of the search space that are known not to lead to optimal solutions.
For example, when K == 0, it checks whether the current solution is potentially better than the previously found optimal solution before continuing the exploration. This avoids unnecessary recursion in cases where the current solution cannot improve upon the best solution found so far.
Pure brute force would typically explore all possible combinations without such early termination conditions.
"""


def dynamic_programming(datos: Dict[str, any], discretizacion_x: List[float], discretizacion_y: List[float], K: int, pos_to_analize_x: int, pos_value_in_y: int, sol, tensor: List[List[List[Tuple[(float, int, int)]]]]) -> float:
		error_minimo_hallado = sol['min_found']
		
		if K == 1:
			error_min: float = BIG_NUMBER
			best_y_pos: int = None
			for pos_y in range(0, len(discretizacion_y)):
				tupla_x_y_solucion_temp: List[Tuple[float, float]] = []
				tupla_x_y_solucion_temp.append((discretizacion_x[0], discretizacion_y[pos_y]))
				tupla_x_y_solucion_temp.append((discretizacion_x[pos_to_analize_x], discretizacion_y[pos_value_in_y]))
				error: float = calculate_min_error(datos, tupla_x_y_solucion_temp)
				
				if error < error_min:
					error_min = error
					best_y_pos = pos_y
			
			sol.update({"min_found": error_min})
			tensor[pos_to_analize_x][pos_value_in_y][K-1] = (error_min, 0, best_y_pos) # best_x_pos es 0 siempre porque es el caso base
			return error_min
		
		elif K > pos_to_analize_x: #pos_to_analize_x == 1 and K > 1:
			return BIG_NUMBER

		
		elif tensor[pos_to_analize_x][pos_value_in_y][K-1] != None:
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
					error_of_sub_problem = calculate_min_error(datos, tupla_x_y_solucion_temp) - error_first_point + dynamic_programming(datos, discretizacion_x, discretizacion_y, K-1, pos_x, pos_y, sol, tensor)
					
					if error_of_sub_problem < error_minimo_hallado:
						best_x_pos = pos_x
						best_y_pos = pos_y
						error_minimo_hallado = error_of_sub_problem
					
					sol.update({"min_found": error_minimo_hallado})
			
			tensor[pos_to_analize_x][pos_value_in_y][K-1] = (sol["min_found"], best_x_pos, best_y_pos)
			return error_minimo_hallado

def found_best_initial_y(datos: Dict[str, any], discretizacion_x: List[float], discretizacion_y: List[float], K: int, sol) -> Tuple[float, List[List[List[Tuple[(float, int, int)]]]]]:
    res: float = BIG_NUMBER
    min_y: int = None

    tensor: List[List[List[Tuple[(float, int, int)]]]] = []

    for i in range(0, len(discretizacion_x)):
        tensor.append([])
        for j in range(0, len(discretizacion_y)):
            tensor[i].append([])
            for k in range(1, K+1):
                tensor[i][j].append(None)

    for pos_y in range(0, len(discretizacion_y)):
        valor: float = dynamic_programming(datos, discretizacion_x, discretizacion_y, K, len(discretizacion_x)-1, pos_y, sol, tensor)
        if valor < res:
            res = valor
            min_y = pos_y

    return (min_y, tensor)

def reconstruct_solution(discretizacion_x: List[float], discretizacion_y: List[float], K: int, tuple_best_pos_y_and_tensor: Tuple[float, List[List[List[Tuple[(float, int, int)]]]]], solution) -> json:
    res: List[Tuple[int, int]] = []
    pos_x: int = len(discretizacion_x) - 1
    pos_y: int = tuple_best_pos_y_and_tensor[0]
    value_K: int = K
    tensor: List[List[List[Tuple[(float, int, int)]]]] = tuple_best_pos_y_and_tensor[1]

    res.append((discretizacion_x[pos_x], discretizacion_y[pos_y]))

    while value_K > 0:
        new_pos_x = tensor[pos_x][pos_y][value_K - 1][1]
        new_pos_y = tensor[pos_x][pos_y][value_K - 1][2]
        value_K = value_K - 1
        pos_x = new_pos_x
        pos_y = new_pos_y
        res.append((discretizacion_x[pos_x], discretizacion_y[pos_y]))

    res.reverse()
    solution.update({"solution": res.copy()})

    return solution
