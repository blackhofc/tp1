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

def calculate_error(instance:Dict, solution:Dict) -> float:
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


def brute_force_bis(instance: Dict, grid_x: List[float], grid_y: List[float], K: int, pos_x: int, temp_solution: List, solution: Dict) -> float:
    '''
    Función recursiva llamada por brute_force.
    
    Esta función busca exhaustivamente las posibles combinaciones de puntos en el espacio definido por las grillas grid_x y grid_y
    para encontrar la solución óptima que minimice el error absoluto, teniendo en cuenta un límite K de breakpoints.
    
    Parámetros:
        - instance: Diccionario con la instancia del problema.
        - grid_x: Lista de puntos en el eje x.
        - grid_y: Lista de puntos en el eje y.
        - K: Número máximo de breakpoints permitidos.
        - pos_x: Índice para la grilla x (inicializado en 0).
        - temp_solution: Solución temporal que se va construyendo.
        - solution: Solución óptima que será la óptima al terminar la recursión.
        
    Retorna:
        El error mínimo encontrado.
    '''

    # Inicializamos el error mínimo encontrado hasta el momento.
    min_error_found = solution['min_found']

    # Si hemos alcanzado el final de la grilla x, hemos considerado todas las opciones para los breakpoints.
    if pos_x == len(grid_x):
        # Caso base 2: Si no quedan breakpoints por asignar, calculamos el error absoluto de la solución actual.
        if K == 0:
            current_min = calculate_error(instance, temp_solution)
            # Si el error actual es menor que el mínimo encontrado hasta el momento y la solución cumple ciertas condiciones,
            # Actualizamos la solución óptima.
            if (current_min < min_error_found) and (temp_solution[0][0] == grid_x[0]) and (temp_solution[-1][0] == grid_x[-1]):
                solution.update({'solution': temp_solution.copy(), 'min_found': current_min})
                return current_min
            return BIG_NUMBER  # Un valor grande para indicar que no es una solución válida.
        elif K > 0:
            return BIG_NUMBER  # Un valor grande para indicar que no es una solución válida.

    # Caso recursivo: Consideramos agregar o no la coordenada de x actual (x_1) a la solución.
    else:
        # Calculamos el error sin incluir la coordenada actual de x en la solución.
        error_without_x = brute_force_bis(instance, grid_x, grid_y, K, pos_x + 1, temp_solution, solution)
        
        # Iteramos sobre todas las posibles coordenadas en y para la coordenada actual de x.
        for pos_y in range(len(grid_y)):
            current_sol = list(temp_solution)
            current_sol.append((grid_x[pos_x], grid_y[pos_y]))

            # Calculamos el error incluyendo la coordenada actual de x en la solución.
            error_with_x = brute_force_bis(instance, grid_x, grid_y, K - 1, pos_x + 1, current_sol, solution)
            
            # Actualizamos el error mínimo encontrado hasta el momento.
            min_error_found = min(min_error_found, error_with_x, error_without_x)
            solution.update({'min_found': min_error_found})

    return min_error_found

def brute_force(instance: Dict, grid_x: List[float], grid_y: List[float], K: int) -> Dict:
    '''
    Toma un conjunto de instancias, una discretización en X y en Y, y una cantidad K >= 2 de breakpoints.
    Devuelve un diccionario con una lista de K breakpoints pertenecientes a la discretización, de modo que se minimice el error absoluto al armar una función continua piecewise linear con esos breakpoints.
    
    Parámetros:
        - instance: Diccionario con la instancia del problema.
        - grid_x: Lista de puntos en el eje x.
        - grid_y: Lista de puntos en el eje y.
        - K: Número de breakpoints requeridos (K >= 2).
        
    Retorna:
        Un diccionario con la solución óptima que minimiza el error absoluto.
    '''
    
    # Inicializamos el valor de BIG_NUMBER para comparaciones.
    solution = { 'min_found': BIG_NUMBER }

    # Inicializamos la función recursiva auxiliar.
    brute_force_bis(instance, grid_x, grid_y, K, 0, [], solution)
    
    return solution


def back_tracking_bis(instance: Dict, grid_x: List[float], grid_y: List[float], K: int, pos_x: int, temp_solution: List, solution: Dict) -> float:
    '''
    Función recursiva llamada por back_tracking.
    
    Esta función implementa un algoritmo de backtracking para encontrar la solución óptima que minimice el error absoluto al armar una función continua piecewise linear con una cantidad limitada de breakpoints.
    
    Parámetros:
        - instance: Diccionario con la instancia del problema.
        - grid_x: Lista de puntos en el eje x.
        - grid_y: Lista de puntos en el eje y.
        - K: Número máximo de breakpoints permitidos.
        - pos_x: Índice para la grilla x (inicializado en 0).
        - temp_solution: Solución temporal que se va construyendo.
        - solution: Solución óptima que será la óptima al terminar la recursión.
        
    Retorna:
        El error mínimo encontrado.
    '''

    # Inicializamos el error mínimo encontrado hasta el momento.
    min_error_found = solution['min_found']
    
    # Poda de factibilidad: Si no quedan breakpoints por asignar, calculamos el error absoluto de la solución actual.
    if K == 0:
        current_min = calculate_error(instance, temp_solution)
        
        # Si el error actual es menor que el mínimo encontrado hasta el momento y la solución cumple ciertas condiciones,
        # Actualizamos la solución óptima.
        if (current_min < min_error_found and temp_solution[0][0] == grid_x[0] and temp_solution[-1][0] == grid_x[-1]):
            solution.update({'solution': temp_solution.copy(), 'min_found': current_min})
            return current_min
        return BIG_NUMBER  # Un valor grande para indicar que no es una solución válida.
    
    # Poda de factibilidad: Si se requieren más breakpoints de los que se pueden asignar, se devuelve un error muy grande para indicar que no hay un ajuste compatible con los parámetros tomados.
    elif K > len(grid_x) - pos_x:
        return BIG_NUMBER
    
    # Poda de factibilidad: Si la solución temporal no empieza desde el primer punto de la grilla x, se devuelve un error muy grande.
    elif pos_x > 0 and len(temp_solution) > 0 and temp_solution[0][0] != grid_x[0]:
        return BIG_NUMBER
    
    # Poda de optimalidad: Si el error actual supera al mínimo encontrado hasta el momento, se devuelve un error muy grande.
    elif len(temp_solution) > 0 and calculate_error(instance, temp_solution) > min_error_found: 
        return BIG_NUMBER

    else:
        # Calculamos el error sin incluir la coordenada actual de x en la solución.
        error_without_x = back_tracking_bis(instance, grid_x, grid_y, K, pos_x + 1, temp_solution, solution)
        
        # Iteramos sobre todas las posibles coordenadas en y para la coordenada actual de x.
        for pos_y in range(len(grid_y)):
            current_sol = list(temp_solution)
            current_sol.append((grid_x[pos_x], grid_y[pos_y]))

            # Calculamos el error incluyendo la coordenada actual de x en la solución.
            error_with_x = back_tracking_bis(instance, grid_x, grid_y, K - 1, pos_x + 1, current_sol, solution)
            
            # Actualizamos el error mínimo encontrado hasta el momento.
            min_error_found = min(min_error_found, error_with_x, error_without_x)
            solution.update({'min_found': min_error_found})

    return min_error_found

def back_tracking(instance: Dict, grid_x: List[float], grid_y: List[float], K: int) -> Dict:
    '''
    Toma un conjunto de instancias, una discretización en X y en Y, y una cantidad K >= 2 de breakpoints.
    Devuelve un diccionario con una lista de K breakpoints pertenecientes a la discretización, de modo que se minimice el error absoluto al armar una función continua piecewise linear con esos breakpoints.
    
    Parámetros:
        - instance: Diccionario con la instancia del problema.
        - grid_x: Lista de puntos en el eje x.
        - grid_y: Lista de puntos en el eje y.
        - K: Número de breakpoints requeridos (K >= 2).
        
    Retorna:
        Un diccionario con la solución óptima que minimiza el error absoluto.
    '''

    # Inicializamos el valor de BIG_NUMBER para comparaciones.
    solution = { 'min_found': BIG_NUMBER }

    # Llamamos a la función recursiva auxiliar.
    back_tracking_bis(instance, grid_x, grid_y, K, 0, [], solution)
    
    return solution


def reconstruct_solution(grid_x: List[float], grid_y: List[float], K: int, min_y: int, memo: List, solution: Dict) -> Dict:
    '''
    Reconstruye la solución óptima a partir del tensor de memorización (memo) generada durante la búsqueda de la solución.
    
    Parámetros:
        - grid_x: Lista de puntos en el eje x.
        - grid_y: Lista de puntos en el eje y.
        - K: Número de breakpoints requeridos.
        - min_y: Índice mínimo de la grilla y.
        - memo: Tensor de memorización generado durante la búsqueda de la solución.
        - solution: Solución que se actualizará con la lista de breakpoints reconstruida.
        
    Retorna:
        La solución actualizada con la lista de breakpoints reconstruida.
    '''
    
    # Inicializamos las posiciones iniciales en x y y.
    pos_x = len(grid_x) - 1
    pos_y = min_y

    # Lista para almacenar los breakpoints reconstruidos.
    res = [(grid_x[pos_x], grid_y[pos_y])]
    
    # Reconstrucción de la solución iterando a través del tensor de memorización.
    while K > 0:
        # Obtenemos las nuevas posiciones x e y a partir del tensor de memorización.
        pos_x, pos_y = memo[pos_x][pos_y][K - 1][1], memo[pos_x][pos_y][K - 1][2]
        K -= 1
        # Agregamos el nuevo breakpoint reconstruido a la lista.
        res.append((grid_x[pos_x], grid_y[pos_y]))

    # Invertimos la lista de breakpoints para que estén en el orden correcto.
    res.reverse()
    
    # Actualizamos la solución con la lista de breakpoints reconstruida.
    solution.update({ 'solution': res })
    
    return solution

def handle_base_case(instance: Dict, grid_x: List[float], grid_y: List[float], pos_x: int, pos_y: int, memo: List, solution: Dict) -> float:
    '''
    Maneja el caso base en el tensor de memorización (memo) cuando no hay breakpoints restantes por asignar.
    
    Parámetros:
        - instance: Diccionario con la instancia del problema.
        - grid_x: Lista de puntos en el eje x.
        - grid_y: Lista de puntos en el eje y.
        - pos_x: Índice de la grilla x.
        - pos_y: Índice de la grilla y.
        - memo: Tensor de memorización que se actualizará con la información del caso base.
        - solution: Solución que se actualizará si se encuentra un nuevo error mínimo.
        
    Retorna:
        El error mínimo encontrado en el caso base.
    '''

    # Inicializamos el error mínimo como un valor grande.
    error_min = BIG_NUMBER
    best_y_pos = -1  # Índice de la mejor posición de y.

    # Iteramos sobre todas las posiciones de y en la grilla y.
    for i, y in enumerate(grid_y):

        # Creamos una solución temporal con el primer punto en x y el punto actual en y.
        temp_sol = [(grid_x[0], y), (grid_x[pos_x], grid_y[pos_y])]

        # Calculamos el error absoluto de la solución temporal.
        error = calculate_error(instance, temp_sol)
        
        # Actualizamos el error mínimo y la mejor posición de y si encontramos un nuevo mínimo.
        if error < error_min:
            error_min = error
            best_y_pos = i

    # Actualizamos el tensor de memorización con la información del caso base.
    memo[pos_x][pos_y][0] = (error_min, 0, best_y_pos)

    return error_min

def handle_recursive_case(instance: Dict, grid_x: List[float], grid_y: List[float], K: int, pos_x: int, pos_y: int, memo: List, solution: Dict) -> float:
    '''
    Maneja el caso recursivo en el tensor de memorización (memo) durante la búsqueda de la solución.
    
    Parámetros:
        - instance: Diccionario con la instancia del problema.
        - grid_x: Lista de puntos en el eje x.
        - grid_y: Lista de puntos en el eje y.
        - K: Número de breakpoints restantes por asignar.
        - pos_x: Índice de la grilla x.
        - pos_y: Índice de la grilla y.
        - memo: Tensor de memorización que se actualizará con la información del caso recursivo.
        - solution: Solución que se actualizará si se encuentra un nuevo error mínimo.
        
    Retorna:
        El error mínimo encontrado en el caso recursivo.
    '''

    # Inicializamos el error mínimo, las mejores posiciones de x e y como valores iniciales.
    min_error_found = BIG_NUMBER
    best_x_pos = -1
    best_y_pos = -1

    # Iteramos sobre todas las posiciones de x anteriores a la posición actual.
    for i in range(1, pos_x):
        for j in range(len(grid_y)):
            # Creamos una solución temporal con el punto en x e y actuales.
            temp_solution = [(grid_x[i], grid_y[j]), (grid_x[pos_x], grid_y[pos_y])]

            # Calculamos el error del primer punto respecto al valor objetivo y el error de la sub-problema recursiva.
            error_first_point = abs(instance['y'][0] - temp_solution[0][1])
            sub_problem_error = calculate_error(instance, temp_solution) - error_first_point + dynamic_bis(instance, grid_x, grid_y, K-1, i, j, memo, solution)

            # Actualizamos el error mínimo y las mejores posiciones de x e y si encontramos un nuevo mínimo.
            if sub_problem_error < min_error_found:
                best_x_pos = i
                best_y_pos = j
                min_error_found = sub_problem_error
    
    # Actualizamos el tensor de memorización con la información del caso recursivo.
    memo[pos_x][pos_y][K - 1] = (min_error_found, best_x_pos, best_y_pos)
    
    return min_error_found

def find_best_initial_y(instance: Dict, grid_x: List[float], grid_y: List[float], K: int, solution: Dict) -> Tuple[int, List[List[List[Tuple[float, int, int]]]]]:
    '''
    Encuentra la mejor posición inicial en y para iniciar la búsqueda de la solución óptima.
    
    Parámetros:
        - instance: Diccionario con la instancia del problema.
        - grid_x: Lista de puntos en el eje x.
        - grid_y: Lista de puntos en el eje y.
        - K: Número de breakpoints requeridos.
        - solution: Solución que se actualizará con el costo mínimo encontrado.
        
    Retorna:
        La mejor posición inicial en y y el tensor de memorización utilizada durante la búsqueda.
    '''

    # Inicializamos el costo mínimo y la posición inicial en y como valores iniciales.
    min_cost = BIG_NUMBER
    min_pos_y = -1

    # Inicializamos el tensor de memorización.
    memo = [[[None for _ in range(K)] for _ in grid_y] for _ in grid_x]

    # Iteramos sobre todas las posibles posiciones iniciales en y.
    for pos_y, _ in enumerate(grid_y):
        # Calculamos el costo utilizando el algoritmo de programación dinámica.
        cost = dynamic_bis(instance, grid_x, grid_y, K, len(grid_x) - 1, pos_y, memo, solution)

        # Actualizamos el costo mínimo y la posición inicial en y si encontramos un nuevo mínimo.
        if cost < min_cost:
            min_cost = cost
            min_pos_y = pos_y

    # Actualizamos la solución con el costo mínimo encontrado.
    solution.update({ 'min_found': min_cost }) 
    
    # Retornamos la mejor posición inicial en y y el tensor de memorización.
    return min_pos_y, memo

def dynamic_bis(instance: Dict, grid_x: List[float], grid_y: List[float], K: int, pos_x: int, pos_y: int, memo: List, solution: Dict) -> float:
    '''
    Implementa el algoritmo de programación dinámica para resolver el problema de manera eficiente.
    
    Parámetros:
        - instance: Diccionario con la instancia del problema.
        - grid_x: Lista de puntos en el eje x.
        - grid_y: Lista de puntos en el eje y.
        - K: Número de breakpoints restantes por asignar.
        - pos_x: Índice de la grilla x.
        - pos_y: Índice de la grilla y.
        - memo: Tensor de memorización que almacena los resultados de subproblemas ya resueltos.
        - solution: Solución que se actualizará con el costo mínimo encontrado.
        
    Retorna:
        El costo mínimo para el subproblema definido por los parámetros dados.
    '''

    # Caso base: Si solo queda un breakpoint por asignar.
    if K == 1:
        return handle_base_case(instance, grid_x, grid_y, pos_x, pos_y, memo, solution)

    # Si el número de breakpoints restantes es mayor que la posición actual en x, no es posible seleccionar K puntos de una lista de longitud pos_x.
    elif K > pos_x:
        return BIG_NUMBER

    # Si el subproblema ya se ha resuelto, devuelve el resultado almacenado en el tensor de memorización.
    elif memo[pos_x][pos_y][K - 1] is not None:
        return memo[pos_x][pos_y][K - 1][0]

    # Caso recursivo: Llama a la función para manejar el caso recursivo.
    else:
        return handle_recursive_case(instance, grid_x, grid_y, K, pos_x, pos_y, memo, solution)
	
def dynamic(instance: Dict, grid_x: List[float], grid_y: List[float], K: int) -> Dict:
    '''
    Resuelve el problema utilizando el enfoque de programación dinámica para encontrar la solución óptima que minimice el error absoluto.
    
    Parámetros:
        - instance: Diccionario con la instancia del problema.
        - grid_x: Lista de puntos en el eje x.
        - grid_y: Lista de puntos en el eje y.
        - K: Número de breakpoints requeridos (K >= 2).
        
    Retorna:
        Un diccionario con la solución óptima que minimiza el error absoluto.
    '''

    # Inicializamos el diccionario de solución con un valor grande para el error mínimo.
    solution: Dict = { 'min_found': BIG_NUMBER }

    # Encontramos la mejor posición inicial en y para iniciar la búsqueda de la solución.
    min_y, memo = find_best_initial_y(instance, grid_x, grid_y, K-1, solution)
    
    # Reconstruimos la solución óptima a partir del tensor de memorización.
    reconstruct_solution(grid_x, grid_y, K-1, min_y, memo, solution)
    
    # Retornamos la solución óptima.
    return solution