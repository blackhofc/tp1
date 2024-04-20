from typing import *

# Para tomar como valor arbitrariamente grande
BIG_NUMBER = 1e20


def line(t_prime, y_prime, t_double_prime, y_double_prime, t):
    """
    Calcula g(t) = ((y'' - y')/(t'' - t')) * (t - t') + y'
    """
    return ((y_double_prime - y_prime) / (t_double_prime - t_prime)) * (
        t - t_prime
    ) + y_prime


def absolute_error(xi, yi, t_prime, y_prime, t_double_prime, y_double_prime):
    """
    Calcula el error absoluto de aproximación por la recta dada en el punto xi con respecto a su observación yi.
    """
    y_predict = line(t_prime, y_prime, t_double_prime, y_double_prime, xi)
    return abs(yi - y_predict)


def calculate_error(instance: Dict, solution: Dict) -> float:
    """
    Toma un conjunto de datos y una lista de breakpoints (ordenada en su coordenada de abscisas) y devuelve el error total del ajuste piecewise linear asociado.
    Requiere una instancia no vacía y asume que |solution| >= 2.
    """
    # Error del primer punto
    min_error = abs(instance["y"][0] - solution[0][1])

    # Se calcula para breakpoint actual < x <= breakpoint siguiente, el error absoluto entre la observación y la aproximación
    # También expresado como la sumatoria para las x_i en el conjunto de datos de |y_i - f(x_i)|, entendiendo a
    # f(x) como la función continua partida compuesta por rectas entre breakpoints.
    for point in range(1, len(instance["x"])):
        xi = instance["x"][point]
        yi = instance["y"][point]

        for sol_index in range(len(solution) - 1):
            t_prime, y_prime = solution[sol_index]
            t_double_prime, y_double_prime = solution[sol_index + 1]

            if t_prime < xi <= t_double_prime:
                error = absolute_error(
                    xi, yi, t_prime, y_prime, t_double_prime, y_double_prime
                )
                min_error += error
                break

    return min_error


def brute_force_bis(
    instance: Dict,
    grid_x: List[float],
    grid_y: List[float],
    K: int,
    pos_x: int,
    temp_solution: List,
    solution: Dict,
):
    """
    Función recursiva llamada por brute_force.

    Genera exhaustivamente las posibles combinaciones de puntos en el espacio definido por las grillas grid_x y grid_y
    para encontrar la solución óptima que minimice el error absoluto,
    teniendo en cuenta una cantidad K de breakpoints y abarcar todos los puntos del conjunto.

    Requiere:
        - instance: diccionario con la instancia del problema.
        - grid_x: lista de puntos en la grilla de discretización en x.
        - grid_y: lista de puntos en la grilla de discretización en y.
        - K: número de breakpoints restantes por asignar.
        - pos_x: índice para la grilla x (inicializado en 0).
        - temp_solution: solución temporal que se va construyendo.
        - solution: contendrá a la óptima al terminar la recursión.
    """

    # Inicializamos el error mínimo encontrado hasta el momento (notar que comienza en BIG_NUMBER al iniciar la recursión).
    min_error_found = solution["min_found"]

    # Caso base
    # Si hemos alcanzado el final de la grilla x, hemos considerado todas las opciones para los breakpoints.
    if pos_x == len(grid_x):
        # Si la solución tiene tamaño K, calculamos el error absoluto de la solución actual como candidata a óptima.
        if K == 0:
            current_min = calculate_error(instance, temp_solution)
            # Si el error de la solución actual es menor que el mínimo encontrado hasta el momento y abarca todo el conjunto de datos,
            # actualizamos la solución óptima con la nueva.
            if (
                (current_min < min_error_found)
                and (temp_solution[0][0] == grid_x[0])
                and (temp_solution[-1][0] == grid_x[-1])
            ):
                solution.update(
                    {"solution": temp_solution.copy(), "min_found": current_min}
                )
                return
            return
        elif K > 0:
            return

    # Paso recursivo: consideramos agregar o no la coordenada de x actual (xi) a la solución (que haya un breakpoint de la forma (xi, *)).
    else:
        # Armamos las posibles soluciones sin considerar los breakpoints de la forma (xi, *).
        brute_force_bis(instance, grid_x, grid_y, K, pos_x + 1, temp_solution, solution)

        # Iteramos sobre todos los posibles breakpoints con coordenada de x en xi.
        for pos_y in range(len(grid_y)):
            current_sol = list(temp_solution)
            current_sol.append((grid_x[pos_x], grid_y[pos_y]))

            # Armamos las posibles soluciones tomando algún breakpoint de la forma (xi, *).
            brute_force_bis(
                instance, grid_x, grid_y, K - 1, pos_x + 1, current_sol, solution
            )
    return


def brute_force(
    instance: Dict, grid_x: List[float], grid_y: List[float], K: int
) -> Dict:
    """
    Requiere:
        - instance: conjunto de datos no vacío.
        - |grid_x| > 1
        - |grid_y| > 0
        - 2 <= K <= |grid_x|

    Devuelve:
        Un diccionario con una lista de breakpoints tales que la función continua piecewise linear
        formada a partir de estos minimiza el error, y el error mínimo asociado.
    """

    # Inicializamos el error en uno muy grande para comparaciones.
    solution = {"min_found": BIG_NUMBER}

    # Inicializamos la función recursiva auxiliar.
    brute_force_bis(instance, grid_x, grid_y, K, 0, [], solution)

    return solution


def back_tracking_bis(
    instance: Dict,
    grid_x: List[float],
    grid_y: List[float],
    K: int,
    pos_x: int,
    temp_solution: List,
    solution: Dict,
):
    """
    Función recursiva llamada por back_tracking.

    Sigue la misma lógica que brute_force, pero implementa podas para reducir el espacio de soluciones generado.

    Requiere:
        - instance: diccionario con la instancia del problema.
        - grid_x: lista de puntos en la grilla de discretización en x.
        - grid_y: lista de puntos en la grilla de discretización en y.
        - K: número de breakpoints restantes por asignar.
        - pos_x: índice para la grilla x (inicializado en 0).
        - temp_solution: solución temporal que se va construyendo.
        - solution: contendrá a la óptima al terminar la recursión.
    """

    # Inicializamos el error mínimo encontrado hasta el momento (notar que comienza en BIG_NUMBER al iniciar la recursión).
    min_error_found = solution["min_found"]

    # Caso base: si no quedan breakpoints por asignar (|temp_solution| = K), calculamos el error absoluto de la solución actual.
    if K == 0:
        current_min = calculate_error(instance, temp_solution)

        # Si el error de la solución actual es menor que el mínimo encontrado hasta el momento y abarca todo el conjunto de datos,
        # actualizamos la solución óptima con la nueva.
        if (
            current_min < min_error_found
            and temp_solution[0][0] == grid_x[0]
            and temp_solution[-1][0] == grid_x[-1]
        ):
            solution.update(
                {"solution": temp_solution.copy(), "min_found": current_min}
            )
            return
        return

    # Poda por factibilidad: se requieren más breakpoints de los que se pueden asignar.
    elif K > len(grid_x) - pos_x:
        return

    # Poda por factibilidad: la solución temporal no contiene al primer punto de la grilla en x
    # (correspondiente al de la primer observación)
    elif pos_x > 0 and len(temp_solution) > 0 and temp_solution[0][0] != grid_x[0]:
        return

    # Poda por optimalidad: el error actual supera al mínimo encontrado hasta el momento.
    elif (
        len(temp_solution) > 0
        and calculate_error(instance, temp_solution) > min_error_found
    ):
        return

    # Paso recursivo: consideramos agregar o no la coordenada de x actual (xi) a la solución (que haya un breakpoint de la forma (xi, *)).
    else:
        # Armamos las posibles soluciones sin considerar los breakpoints de la forma (xi, *).
        back_tracking_bis(
            instance, grid_x, grid_y, K, pos_x + 1, temp_solution, solution
        )

        # Iteramos sobre todos los posibles breakpoints con coordenada de x = xi.
        for pos_y in range(len(grid_y)):
            current_sol = list(temp_solution)
            current_sol.append((grid_x[pos_x], grid_y[pos_y]))

            # Armamos las posibles soluciones tomando algún breakpoint de la forma (xi, *).
            back_tracking_bis(
                instance, grid_x, grid_y, K - 1, pos_x + 1, current_sol, solution
            )

    return


def back_tracking(
    instance: Dict, grid_x: List[float], grid_y: List[float], K: int
) -> Dict:
    """
    Requiere:
        - instance: conjunto de datos no vacío.
        - |grid_x| > 1
        - |grid_y| > 0
        - 2 <= K <= |grid_x|

    Devuelve:
        Un diccionario con una lista de breakpoints tales que la función continua piecewise linear
        formada a partir de estos minimiza el error, y el error mínimo asociado.
    """

    # Inicializamos el error en uno muy grande para comparaciones.
    solution = {"min_found": BIG_NUMBER}

    # Inicializamos la función recursiva auxiliar.
    back_tracking_bis(instance, grid_x, grid_y, K, 0, [], solution)

    return solution


def reconstruct_solution(
    grid_x: List[float],
    grid_y: List[float],
    K: int,
    min_y: int,
    memo: List,
    solution: Dict,
) -> Dict:
    """
    Reconstruye la solución óptima a partir del memo generado durante la búsqueda del error mínimo.

    Devuelve:
        La solución actualizada con la lista de breakpoints reconstruida.
    """

    # Inicializamos las posiciones iniciales para x e y.
    pos_x = len(grid_x) - 1
    pos_y = min_y

    # Almacenamos la solución
    res = [(grid_x[pos_x], grid_y[pos_y])]

    # Reconstrucción de la solución recorriendo memo.
    while K > 0:
        # Recuperamos las coordenadas que minimizan el sub problema resuelto.
        pos_x, pos_y = memo[pos_x][pos_y][K - 1][1], memo[pos_x][pos_y][K - 1][2]
        K -= 1
        # Agregamos el nuevo breakpoint reconstruido a la solución.
        res.append((grid_x[pos_x], grid_y[pos_y]))

    # Ordenamos la lista de breakpoints de forma creciente en x.
    res.reverse()

    # Actualizamos la solución ya reconstruida.
    solution.update({"solution": res})

    return solution


def handle_base_case(
    instance: Dict,
    grid_x: List[float],
    grid_y: List[float],
    pos_x: int,
    pos_y: int,
    memo: List,
) -> float:
    """
    Maneja el caso base de dynamic_bis.

    Devuelve:
        El error mínimo encontrado en el caso base.
        F_1 ((t_pos_x, z_pos_y))
    """

    # Inicializamos el error mínimo con un valor grande.
    error_min = BIG_NUMBER
    # Índice de la mejor posición de y para la recta entre (ti, zi) y (tpos_x, zpos_y)
    best_y_pos = -1

    # Iteramos sobre todas las posiciones de la grilla y.
    for i, y in enumerate(grid_y):

        # Creamos una solución temporal con el primer punto en x y el punto actual en y.
        temp_sol = [(grid_x[0], y), (grid_x[pos_x], grid_y[pos_y])]

        # Calculamos el error absoluto de la recta con la instancia.
        error = calculate_error(instance, temp_sol)

        # Actualizamos el error mínimo y la mejor posición de y si encontramos un nuevo mínimo.
        if error < error_min:
            error_min = error
            best_y_pos = i

    # Actualizamos memo con la información del caso base una vez encontrado el mínimo.
    memo[pos_x][pos_y][0] = (error_min, 0, best_y_pos)

    return error_min


def handle_recursive_case(
    instance: Dict,
    grid_x: List[float],
    grid_y: List[float],
    M: int,
    pos_x: int,
    pos_y: int,
    memo: List,
    solution: Dict,
) -> float:
    """
    Maneja el caso recursivo de dynamic_bis.

    Devuelve:
        El error mínimo encontrado en el caso recursivo.
    """

    # Inicializamos el error mínimo en uno arbitrariamente grande,
    # y las mejores posiciones de x e y como valores iniciales (tales que minimicen la solución para (tpos_x, zpos_y), que viene de F_M)
    min_error_found = BIG_NUMBER
    best_x_pos = -1
    best_y_pos = -1

    # Iteramos sobre todas las posiciones de x anteriores en la grilla.
    # Calculamos F_{M}((tpos_x, zpos_y))
    for i in range(1, pos_x):
        for j in range(len(grid_y)):
            # Creamos una solución temporal con el punto en x e y actuales.
            temp_solution = [(grid_x[i], grid_y[j]), (grid_x[pos_x], grid_y[pos_y])]

            # Calculamos el error del punto actual respecto al punto pasado por parámetro + el error de la sub-problema recursiva en el punto actual.
            error_first_point = abs(instance["y"][0] - temp_solution[0][1])
            sub_problem_error = (
                calculate_error(instance, temp_solution)
                - error_first_point
                + dynamic_bis(instance, grid_x, grid_y, M - 1, i, j, memo, solution)
            )

            # Actualizamos el error mínimo y las mejores posiciones de x e y si encontramos un nuevo mínimo.
            if sub_problem_error < min_error_found:
                best_x_pos = i
                best_y_pos = j
                min_error_found = sub_problem_error

    # Actualizamos memo con la información del caso recursivo.
    memo[pos_x][pos_y][M - 1] = (min_error_found, best_x_pos, best_y_pos)

    return min_error_found


def find_best_initial_y(
    instance: Dict, grid_x: List[float], grid_y: List[float], M: int, solution: Dict
) -> Tuple[int, List[List[List[Tuple[float, int, int]]]]]:
    """
    Encuentra la mejor posición inicial en la grilla de discretización en y para iniciar la búsqueda de la solución óptima con programación dinámica.

    Retorna:
        La mejor posición inicial en y y la estructura usada para memoizar la solución durante la búsqueda (memo).
    """

    # Inicializamos el costo mínimo con un valor muy grande y la mejor posición en y como uno no alcanzable.
    min_cost = BIG_NUMBER
    min_pos_y = -1

    # Inicializamos la estructura de memoización.
    memo = [[[None for _ in range(M)] for _ in grid_y] for _ in grid_x]

    # Consideramos todas las posibles posiciones iniciales en y.
    for pos_y, _ in enumerate(grid_y):
        # Calculamos el costo de cada una utilizando el algoritmo de programación dinámica.
        cost = dynamic_bis(
            instance, grid_x, grid_y, M, len(grid_x) - 1, pos_y, memo, solution
        )

        # Actualizamos el costo mínimo y la mejor posición en y si encontramos un nuevo mínimo.
        if cost < min_cost:
            min_cost = cost
            min_pos_y = pos_y

    # Actualizamos la solución con el costo mínimo encontrado.
    solution.update({"min_found": min_cost})

    # Retornamos la mejor posición inicial en y y memo.
    return min_pos_y, memo


def dynamic_bis(
    instance: Dict,
    grid_x: List[float],
    grid_y: List[float],
    M: int,
    pos_x: int,
    pos_y: int,
    memo: List,
    solution: Dict,
) -> float:
    """
    Función recursiva auxiliar de find_best_initial_y.

    Requiere:
        - instance: diccionario con la instancia del problema.
        - grid_x: lista de puntos en la grilla de discretización en x.
        - grid_y: lista de puntos en la grilla de discretización en y.
        - M: número de piezas por añadir a f.
        - pos_x: índice de la grilla de discretización en x.
        - pos_y: índice de la grilla de discretización en y.
        - memo: estructura de memoización que almacena los resultados de subproblemas ya resueltos memo[i-1][j-1][M-1] = F_M((t_i, z_j)).
        - solution: solución que se actualizará con el costo mínimo encontrado.

    Devuelve:
        El costo mínimo para el subproblema definido por los parámetros dados.
    """

    # Caso base
    if M == 1:
        return handle_base_case(instance, grid_x, grid_y, pos_x, pos_y, memo)

    # Si la cantidad de piezas faltantes no es compatible con la cantidad de puntos en la grilla x, se descarta la solución
    elif M > pos_x:
        return BIG_NUMBER

    # Si el subproblema ya se ha resuelto, devuelve el resultado almacenado en memo.
    elif memo[pos_x][pos_y][M - 1] is not None:
        return memo[pos_x][pos_y][M - 1][0]

    # Paso recursivo
    else:
        return handle_recursive_case(
            instance, grid_x, grid_y, M, pos_x, pos_y, memo, solution
        )


def dynamic(instance: Dict, grid_x: List[float], grid_y: List[float], K: int) -> Dict:
    """
    Resuelve el problema utilizando el enfoque de programación dinámica top-down para encontrar la solución óptima que minimice el error absoluto.

    Requiere:
        - instance: conjunto de datos no vacío.
        - |grid_x| > 1
        - |grid_y| > 0
        - 2 <= K <= |grid_x|

    Devuelve:
        Un diccionario con una lista de K breakpoints tales que la función continua piecewise linear
        formada a partir de estos minimiza el error, y el error mínimo asociado.
    """

    # Inicializamos un error arbitrariamente grande.
    solution: Dict = {"min_found": BIG_NUMBER}

    # Buscamos la posición de la grilla y que minimiza F_{K-1} ((t_m1, z_{min_y}))
    min_y, memo = find_best_initial_y(instance, grid_x, grid_y, K - 1, solution)

    # Reconstruimos la solución óptima a partir del memo creado.
    reconstruct_solution(grid_x, grid_y, K - 1, min_y, memo, solution)

    return solution
