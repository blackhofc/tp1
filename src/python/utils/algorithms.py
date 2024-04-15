from typing import *
import json, time

BIG_NUMBER = 1e20  # Check if needed.


def line(t_prime, y_prime, t_double_prime, y_double_prime, t):
    '''
    Calcula la recta que une dos puntos dados.
    '''

    return ((y_double_prime - y_prime) / (t_double_prime - t_prime)) * (t - t_prime) + y_prime


def absolute_error(xi, yi, t_prime, y_prime, t_double_prime, y_double_prime):
    '''
    Calcula el error absoluto de aproximación por la recta en el punto xi.
    '''
    y_predict = line(t_prime, y_prime, t_double_prime, y_double_prime, xi)
    return abs(yi - y_predict)


def calculate_min_error(instance: json, solution: List[Tuple[float, float]]) -> float:
    '''
    Toma un conjunto de instance y una lista de breakpoints y devuelve el error total del ajuste picewise lienar correspondiente.
    Requiere un conjunto de instance no vacío y al menos 2 breakpoints.
    '''
    # TODO: Use absolut_error, line functions and replace this one
    # print(tupla_valores)

    # Error del primer punto
    min_error = abs(instance['y'][0] - solution[0][1])  

    for point in range(1, len(instance['x'])):
        xi = instance['x'][point]
        yi = instance['y'][point]

        for sol_index in range(len(solution) - 1):
            t_prime, y_prime = solution[sol_index]
            t_double_prime, y_double_prime = solution[sol_index + 1]

            if t_prime < xi <= t_double_prime:
                error = absolute_error(xi, yi, t_prime, y_prime, t_double_prime, y_double_prime)
                min_error += error
                break

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
    '''Función recursiva llamada por brute_force.
    Toma los mismos requerimientos junto con un índice para la grilla x (inicializado en 0), una solución temporal que se va construyendo
    y una solución óptima que será efectivamente la óptima al terminar la recursión.'''

    min_error_found = solution['min_found']

    # TODO: COMENTAR
    if pos_x == len(grid_x):

        # Caso base 2, si ya no hay breakpoints que asignar, ya se tiene armada la solución final.
        # Basta con calcular el error absoluto correspondiente a la solución actual y ver si es menor que el de la solución óptima hasta el momento.
        if K == 0:
            current_min = calculate_min_error(instance, temp_solution)
            if ((current_min < min_error_found)
                and (temp_solution[0][0] == grid_x[0])
                and (temp_solution[len(temp_solution) - 1][0] == grid_x[len(grid_x) - 1])):
                
                solution.update({ 'solution': temp_solution.copy(), 'min_found': current_min })
                return current_min
            return BIG_NUMBER

        elif K > 0:
            return BIG_NUMBER

    # Caso recursivo, se considera agregar o no la coordenada de x actual (x_1) a la solución.
    # En caso de agregarse, considero todos los puntos de la forma (x_1, *) donde * es un value perteneciente a la grilla y.
    # Se consideran entonces todas las posibles coordenadas válidas en x_1 como parte de la solución. Se recursan n+1 veces siendo n el tamaño de la grilla y.
    else:
        error_without_x = brute_force_bis(instance, grid_x, grid_y, K, pos_x + 1, temp_solution, solution)
        for pos_y in range(0, len(grid_y)):
            current_sol = list(temp_solution).extend((grid_x[pos_x], grid_y[pos_y]))

            error_with_x = brute_force_bis(instance, grid_x, grid_y, K - 1, pos_x + 1, current_sol, solution)
            min_error_found = min(min_error_found, error_with_x, error_without_x)

            solution.update({ 'min_found': min_error_found })

    return min_error_found


def brute_force(instance: json, grid_x: List[float], grid_y: List[float], K: int) -> json:
    '''Toma un conjunto de instance, una discretización en X y en Y, y una cantidad K >= 2 de breakpoints.
    Devuelve un json con una lista con K breakpoints pertenecientes a la discretización tal que se minimice el error absoluto al armar una función continua picewise linear en función a los breakpoints.
    '''
    solution = { 'min_found': BIG_NUMBER }

    # Inicializo la función recursiva auxiliar.
    brute_force_bis(instance, grid_x, grid_y, K, 0, [], solution)
    return solution


def back_tracking_bis(
    instance: json,
    grid_x: List[float],
    grid_y: List[float],
    K: int,
    pos_x: int,
    temp_solution: List[Tuple[float, float]],
    solution,
) -> float:

    min_error_found = solution['min_found']
    
    # Poda factibilidad
    if K == 0:
        current_min = calculate_min_error(instance, temp_solution)
        if (current_min < min_error_found and temp_solution[0][0] == grid_x[0] and temp_solution[len(temp_solution) - 1][0] == grid_x[len(grid_x) - 1]):
            solution.update({'solution': temp_solution.copy(), 'min_found': current_min})
            return current_min
        return BIG_NUMBER
    # Si se requieren más breakpoints de los que se pueden asignar, se devuelve un error muy grande para indicar que no hay un ajuste compatible con los parámetros tomados.
    # Poda factibilidad
    elif K > len(grid_x) - pos_x:
        return BIG_NUMBER

    # Poda factibilidad
    elif pos_x > 0 and len(temp_solution) > 0 and temp_solution[0][0] != grid_x[0]:
        return BIG_NUMBER

    elif (len(temp_solution) > 0 and calculate_min_error(instance, temp_solution) > min_error_found): 
        return BIG_NUMBER

    else:
        error_without_x = back_tracking_bis(instance, grid_x, grid_y, K, pos_x + 1, temp_solution, solution)
        for pos_y in range(0, len(grid_y)):
            current_sol: List[Tuple[float, float]] = list(temp_solution)
            current_sol.append((grid_x[pos_x], grid_y[pos_y]))

            error_with_x = back_tracking_bis(instance, grid_x, grid_y, K - 1, pos_x + 1, current_sol, solution)
            
            min_error_found = min(min_error_found, error_with_x, error_without_x)
            solution.update({'min_found': min_error_found})

    return min_error_found


def back_tracking(instance: json, grid_x: List[float], grid_y: List[float], K: int) -> json:
    '''
    Toma un conjunto de instance, una discretización en X y en Y, y una cantidad K >= 2 de breakpoints.
    Devuelve un json con una lista con K breakpoints pertenecientes a la discretización tal que se minimice el error absoluto al armar una función continua picewise linear en función a los breakpoints.
    '''
    solution = { 'min_found': BIG_NUMBER }

    # Inicializo la función recursiva auxiliar.
    back_tracking_bis(instance, grid_x, grid_y, K, 0, [], solution)
    return solution


def dynamic_bis(instance: Dict, grid_x: List[float], grid_y: List[float], K: int, pos_x: int, pos_y: int, memo, solution: Dict) -> float:
    # Base case: K = 1
    if K == 1:
        return handle_base_case(instance, grid_x, grid_y, pos_x, pos_y, memo, solution)

    # If K is greater than pos_x, it's not possible to select K points from a list of length pos_x.
    elif K > pos_x:
        return BIG_NUMBER

    # If the subproblem has already been solved, return the stored result.
    elif memo[pos_x][pos_y][K - 1] is not None:
        solution.update({'precalculated': solution['precalculated']+1})
        return memo[pos_x][pos_y][K - 1][0]

    # Recursive case
    else:
        solution.update({ 'recursion': solution['recursion']+1 })
        return handle_recursive_case(instance, grid_x, grid_y, K, pos_x, pos_y, memo, solution)

def handle_base_case(instance: Dict, grid_x: List[float], grid_y: List[float], pos_x: int, pos_y: int, memo, solution: Dict) -> float:
    error_min = BIG_NUMBER
    best_y_pos = -1
    
    for i, y in enumerate(grid_y):
        temp_sol = [(grid_x[0], y), (grid_x[pos_x], grid_y[pos_y])]
        error = calculate_min_error(instance, temp_sol)
        
        if error < error_min:
            error_min = error
            best_y_pos = i

    if error_min < solution['min_found']:
        solution['min_found'] = error_min

    memo[pos_x][pos_y][0] = (error_min, 0, best_y_pos)
    return error_min

def handle_recursive_case(instance: Dict, grid_x: List[float], grid_y: List[float], K: int, pos_x: int, pos_y: int, memo, solution: Dict) -> float:
    min_error_found = solution['min_found']
    best_x_pos = 0
    best_y_pos = 0
    
    for i in range(1, pos_x):
        for j, y in enumerate(grid_y):
            temp_sol = [(grid_x[i], y), (grid_x[pos_x], grid_y[pos_y])]
            
            error_first_point = abs(instance['y'][0] - temp_sol[0][1])
            error_of_sub_problem = calculate_min_error(instance, temp_sol) - error_first_point + dynamic_bis(instance, grid_x, grid_y, K-1, i, j, memo, solution)

            if error_of_sub_problem < min_error_found:
                best_x_pos = i
                best_y_pos = j
                min_error_found = error_of_sub_problem

            solution['min_found'] = min_error_found

    memo[pos_x][pos_y][K - 1] = (min_error_found, best_x_pos, best_y_pos)
    return min_error_found

def found_best_initial_y(instance: Dict, grid_x: List[float], grid_y: List[float], K: int, solution: Dict) -> int:
    # Initialize variables
    min_cost = BIG_NUMBER
    min_pos_y = -1

    # Create a memoization table
    memo = [[[None for _ in range(K + 1)] for _ in grid_y] for _ in grid_x]

    # Iterate over possible y positions
    for pos_y, _ in enumerate(grid_y):
        # Calculate cost using dynamic programming
        cost = dynamic_bis(instance, grid_x, grid_y, K, len(grid_x) - 1, pos_y, memo, solution)
        # Update minimum cost and position if necessary
        if cost < min_cost:
            min_cost = cost
            min_pos_y = pos_y

    return min_pos_y, memo
	
def dynamic(instance: json, grid_x: List[float], grid_y: List[float], K: int) -> json:
    '''
    Toma un conjunto de instance, una discretización en X y en Y, y una cantidad K >= 2 de breakpoints.
    Devuelve un json con una lista con K breakpoints pertenecientes a la discretización tal que se minimice el error absoluto al armar una función continua picewise linear en función a los breakpoints.
    '''
    
    solution:json = { 'min_found': BIG_NUMBER, 'recursion': 0, 'precalculated': 0 }

    min_y, memo = found_best_initial_y(instance, grid_x, grid_y, K, solution)
    
    reconstruct_solution(grid_x, grid_y, K, min_y, memo, solution)
    
    return solution

 
def reconstruct_solution(grid_x: List[float], grid_y: List[float], K: int, min_y, memo, solution) -> json:
    res = []
    pos_x:int = len(grid_x) - 1
    pos_y:int = min_y
    res.append((grid_x[pos_x], grid_y[pos_y]))
    while K > 0:
        print('memo[{}][{}][{}]'.format(pos_x, pos_y, K-1))
        new_pos_x = memo[pos_x][pos_y][K - 1][1]
        new_pos_y = memo[pos_x][pos_y][K - 1][2]
        print('new_pos_x {} new_pos_y {}'.format(new_pos_x, new_pos_y))
        
        K -= 1
        pos_x = new_pos_x
        pos_y = new_pos_y
        res.append((grid_x[pos_x], grid_y[pos_y]))

    res.reverse()
    solution.update({'solution': res.copy()})