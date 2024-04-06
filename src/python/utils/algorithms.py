from typing import *
import json

BIG_NUMBER = 1e10  # Check if needed.


def e(x: float, y: float):

    return


def y(x: Tuple[float, float], y: Tuple[float, float]):

    return


def line(t_prime, y_prime, t_double_prime, y_double_prime, t):
    '''
    Calcula la recta que une dos puntos dados.
    '''

    return ((y_double_prime - y_prime) / (t_double_prime - t_prime)) * (
        t - t_prime
    ) + y_prime


def absolut_error(xi, yi, t_prime, y_prime, t_double_prime, y_double_prime):
    '''
    Calcula el error absoluto de aproximación por la recta en el punto xi.
    '''
    y_predicho = line(t_prime, y_prime, t_double_prime, y_double_prime, xi)
    return abs(yi - y_predicho)


def calculate_min_error(instance: json, solution: List[Tuple[float, float]]) -> float:
    '''Toma un conjunto de datos y una lista de breakpoints y devuelve el error total del ajuste picewise lienar correspondiente.
    Requiere un conjunto de datos no vacío y al menos 2 breakpoints.
    '''
    # TODO: Use absolut_error, line functions and replace this one
    # print(tupla_valores)

    min_error: float = abs(instance['y'][0] - solution[0][1])  # Error del primer punto

    for point in range(0, len(instance['x'])):

        for sol_index in range(0, len(solution) - 1):
            if (
                instance['x'][point] > solution[sol_index][0]
                and instance['x'][point] <= solution[sol_index + 1][0]
            ):
                # Calcula el error absoluto de cada partición entre r_k < x <= r_k+1
                # como el valor absoluto de la diferencia entre el dato y la estimación dada por la función f_k
                delta: float = (solution[sol_index + 1][1] - solution[sol_index][1]) / (
                    solution[sol_index + 1][0] - solution[sol_index][0]
                )
                estimacion_y: float = (
                    delta * (instance['x'][point] - solution[sol_index][0])
                    + solution[sol_index][1]
                )
                # Se acumula el error absoluto total
                min_error += abs(instance['y'][point] - estimacion_y)

    return min_error


def brute_force_bis(
    instance: json,
    grid_x: List[float],
    grid_y: List[float],
    K: int,
    pos_x: int,
    temp_solution: List[Tuple[float, float]],
    solution) -> float:
    '''Función recursiva llamada por brute_force.
    Toma los mismos requerimientos junto con un índice para la grilla x (inicializado en 0), una solución temporal que se va construyendo
    y una solución óptima que será efectivamente la óptima al terminar la recursión.'''

    min_error_found = solution['min_found']
    solution['recursion'] +=1
    
    # TODO: COMENTAR
    if pos_x == len(grid_x):
        
        # Caso base 2, si ya no hay breakpoints que asignar, ya se tiene armada la solución final.
        # Basta con calcular el error absoluto correspondiente a la solución actual y ver si es menor que el de la solución óptima hasta el momento.
        if K == 0:
            current_min = calculate_min_error(instance, temp_solution)
            if ((current_min < min_error_found) and (temp_solution[0][0] == grid_x[0]) and (temp_solution[len(temp_solution) - 1][0] == grid_x[len(grid_x) - 1])):
                solution.update({ 'solution': temp_solution.copy(), 'min_found': current_min })
                return current_min
            return BIG_NUMBER

        elif K > 0:
            return BIG_NUMBER
        
    # Caso recursivo, se considera agregar o no la coordenada de x actual (x_1) a la solución.
    # En caso de agregarse, considero todos los puntos de la forma (x_1, *) donde * es un valor perteneciente a la grilla y.
    # Se consideran entonces todas las posibles coordenadas válidas en x_1 como parte de la solución. Se recursan n+1 veces siendo n el tamaño de la grilla y.
    else:
        error_without_x = brute_force_bis(instance, grid_x, grid_y, K, pos_x + 1, temp_solution, solution)
        for pos_y in range(0, len(grid_y)):
            current_sol: List[Tuple[float, float]] = list(temp_solution)
            current_sol.append((grid_x[pos_x], grid_y[pos_y]))

            error_with_x = brute_force_bis(
                instance, grid_x, grid_y, K - 1, pos_x + 1, current_sol, solution
            )
            min_error_found = min(min_error_found, error_with_x, error_without_x)

            solution.update({ 'min_found': min_error_found })

    return min_error_found


def brute_force(instance: json, grid_x: List[float], grid_y: List[float], K: int) -> json:
    '''Toma un conjunto de datos, una discretización en X y en Y, y una cantidad K >= 2 de breakpoints.
    Devuelve un json con una lista con K breakpoints pertenecientes a la discretización tal que se minimice el error absoluto al armar una función continua picewise linear en función a los breakpoints.
    '''
    solution = {'min_found': BIG_NUMBER, 'recursion': 0}
    
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
    solution) -> float:

    min_error_found = solution['min_found']
    solution['recursion'] += 1
    # Poda factibilidad
    if K == 0:
        current_min = calculate_min_error(instance, temp_solution)
        if (current_min < min_error_found and temp_solution[0][0] == grid_x[0] and temp_solution[len(temp_solution) - 1][0] == grid_x[len(grid_x) - 1]):
            solution.update(
                {'solution': temp_solution.copy(), 'min_found': current_min}
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
    elif len(temp_solution) > 0 and calculate_min_error(instance, temp_solution) > min_error_found:
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

            solution.update({'min_found': min_error_found})

    return min_error_found


def backtrack(instance: json, grid_x: List[float], grid_y: List[float], K: int) -> json:
    '''Toma un conjunto de datos, una discretización en X y en Y, y una cantidad K >= 2 de breakpoints.
    Devuelve un json con una lista con K breakpoints pertenecientes a la discretización tal que se minimice el error absoluto al armar una función continua picewise linear en función a los breakpoints.
    '''
    solution = {'min_found': BIG_NUMBER, 'recursion': 0}
    
    # Inicializo la función recursiva auxiliar.
    backtrack_bis(instance, grid_x, grid_y, K, 0, [], solution)
    return solution


def dynamic(instance: json) -> List[Tuple[int, int]]:
    return []

'''
The algorithm includes conditional statements to avoid exploring certain branches of the search space that are known not to lead to optimal solutions.
For example, when K == 0, it checks whether the current solution is potentially better than the previously found optimal solution before continuing the exploration. This avoids unnecessary recursion in cases where the current solution cannot improve upon the best solution found so far.
Pure brute force would typically explore all possible combinations without such early termination conditions.
'''