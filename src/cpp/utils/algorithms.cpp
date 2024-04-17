#include "../include/json.hpp"
#include "utils.h"
#include <iostream>

using namespace nlohmann;
using namespace std;

const double BIG_NUMBER = 1e10;

// Declaring in the scope
double dynamic_bis(const json &instance, const vector<double> &grid_x, const vector<double> &grid_y, int K, int pos_x, int pos_y, vector<vector<vector<tuple<double, int, int>>>> &memo, json &solution);

double brute_force_bis(const json &instance, const vector<double> &grid_x, const vector<double> &grid_y, int K, int pos_x, vector<pair<double, double>> &temp_solution, json &solution)
{
    /*
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
    */

    // Inicializamos el error mínimo encontrado hasta el momento.
    double min_error_found = solution["min_found"];

    // Si hemos alcanzado el final de la grilla x, hemos considerado todas las opciones para los breakpoints.
    if (pos_x == grid_x.size())
    {
        // Caso base 2: Si no quedan breakpoints por asignar, calculamos el error absoluto de la solución actual.
        if (K == 0)
        {
            double current_min = calculate_error(instance, temp_solution);
            // Si el error actual es menor que el mínimo encontrado hasta el momento y la solución cumple ciertas condiciones,
            // Actualizamos la solución óptima.
            if ((current_min < min_error_found) && temp_solution[0].first == grid_x[0] && temp_solution[temp_solution.size() - 1].first == grid_x[grid_x.size() - 1])
            {
                solution["solution"] = temp_solution;
                solution["min_found"] = current_min;
                return current_min;
            }
            return BIG_NUMBER; // Un valor grande para indicar que no es una solución válida.
        }
        else if (K > 0)
        {
            return BIG_NUMBER; // Un valor grande para indicar que no es una solución válida.
        }
    } // Caso recursivo: Consideramos agregar o no la coordenada de x actual (x_1) a la solución.
    else
    {
        // Calculamos el error sin incluir la coordenada actual de x en la solución.
        double error_without_x = brute_force_bis(instance, grid_x, grid_y, K, pos_x + 1, temp_solution, solution);

        // Iteramos sobre todas las posibles coordenadas en y para la coordenada actual de x.
        for (int pos_y = 0; pos_y < grid_y.size(); ++pos_y)
        {
            vector<pair<double, double>> current_sol(temp_solution);
            current_sol.push_back(make_pair(grid_x[pos_x], grid_y[pos_y]));

            // Calculamos el error incluyendo la coordenada actual de x en la solución.
            double error_with_x = brute_force_bis(instance, grid_x, grid_y, K - 1, pos_x + 1, current_sol, solution);

            // Actualizamos el error mínimo encontrado hasta el momento.
            min_error_found = min(min_error_found, min(error_with_x, error_without_x));
            solution["min_found"] = min_error_found;
        }
    }
    return min_error_found;
}

json brute_force(const json &instance, const vector<double> &grid_x, const vector<double> &grid_y, int K)
{
    /*
    Toma un conjunto de instancias, una discretización en X y en Y, y una cantidad K >= 2 de breakpoints.
    Devuelve un diccionario con una lista de K breakpoints pertenecientes a la discretización, de modo que se minimice el error absoluto al armar una función continua piecewise linear con esos breakpoints.

    Parámetros:
        - instance: Diccionario con la instancia del problema.
        - grid_x: Lista de puntos en el eje x.
        - grid_y: Lista de puntos en el eje y.
        - K: Número de breakpoints requeridos (K >= 2).

    Retorna:
        Un diccionario con la solución óptima que minimiza el error absoluto.
    */

    // Inicializamos el valor de BIG_NUMBER para comparaciones.
    json solution = {{"min_found", BIG_NUMBER}};
    vector<pair<double, double>> temp_solution;

    // Inicializamos la función recursiva auxiliar.
    brute_force_bis(instance, grid_x, grid_y, K, 0, temp_solution, solution);
    return solution;
}

double back_tracking_bis(const json &instance, const vector<double> &grid_x, const vector<double> &grid_y, int K, int pos_x, vector<pair<double, double>> &temp_solution, json &solution)
{
    /*
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
    */

    // Inicializamos el error mínimo encontrado hasta el momento.
    double min_error_found = solution["min_found"];

    // Poda de factibilidad: Si no quedan breakpoints por asignar, calculamos el error absoluto de la solución actual.
    if (K == 0)
    {
        double current_min = calculate_error(instance, temp_solution);

        // Si el error actual es menor que el mínimo encontrado hasta el momento y la solución cumple ciertas condiciones,
        // Actualizamos la solución óptima
        if (current_min < min_error_found && temp_solution[0].first == grid_x[0] && temp_solution[temp_solution.size() - 1].first == grid_x[grid_x.size() - 1])
        {
            solution["solution"] = temp_solution;
            solution["min_found"] = current_min;
            return current_min;
        }
        return BIG_NUMBER; // Un valor grande para indicar que no es una solución válida.
    }
    else if (K > grid_x.size() - pos_x)
    {                      // Poda de factibilidad: Si se requieren más breakpoints de los que se pueden asignar, se devuelve un error muy grande para indicar que no hay un ajuste compatible con los parámetros tomados.
        return BIG_NUMBER; // Un valor grande para indicar que no es una solución válida.
    }
    else if (pos_x > 0 && temp_solution.size() > 0 && temp_solution[0].first != grid_x[0])
    { // Poda de factibilidad: Si la solución temporal no empieza desde el primer punto de la grilla x, se devuelve un error muy grande.

        return BIG_NUMBER;
    }
    else if (temp_solution.size() > 0 && calculate_error(instance, temp_solution) > min_error_found)
    { // Poda de optimalidad: Si el error actual supera al mínimo encontrado hasta el momento, se devuelve un error muy grande.
        return BIG_NUMBER;
    }
    else
    {
        // Calculamos el error sin incluir la coordenada actual de x en la solución.
        double error_without_x = back_tracking_bis(instance, grid_x, grid_y, K, pos_x + 1, temp_solution, solution);

        // Iteramos sobre todas las posibles coordenadas en y para la coordenada actual de x.
        for (int pos_y = 0; pos_y < grid_y.size(); ++pos_y)
        {
            vector<pair<double, double>> current_sol(temp_solution);
            current_sol.push_back(make_pair(grid_x[pos_x], grid_y[pos_y]));

            // Calculamos el error incluyendo la coordenada actual de x en la solución.
            double error_with_x = back_tracking_bis(instance, grid_x, grid_y, K - 1, pos_x + 1, current_sol, solution);

            // Actualizamos el error mínimo encontrado hasta el momento.
            min_error_found = min(min_error_found, min(error_with_x, error_without_x));
            solution["min_found"] = min_error_found;
        }
    }
    return min_error_found;
}

json back_tracking(const json &instance, const vector<double> &grid_x, const vector<double> &grid_y, int K)
{
    /*
     Toma un conjunto de instancias, una discretización en X y en Y, y una cantidad K >= 2 de breakpoints.
    Devuelve un diccionario con una lista de K breakpoints pertenecientes a la discretización, de modo que se minimice el error absoluto al armar una función continua piecewise linear con esos breakpoints.

    Parámetros:
        - instance: Diccionario con la instancia del problema.
        - grid_x: Lista de puntos en el eje x.
        - grid_y: Lista de puntos en el eje y.
        - K: Número de breakpoints requeridos (K >= 2).

    Retorna:
        Un diccionario con la solución óptima que minimiza el error absoluto.
    */

    // Inicializamos el valor de BIG_NUMBER para comparaciones.
    json solution = {{"min_found", BIG_NUMBER}};
    vector<pair<double, double>> temp_solution; // []

    // Llamamos a la función recursiva auxiliar.
    back_tracking_bis(instance, grid_x, grid_y, K, 0, temp_solution, solution);
    return solution;
}

json reconstruct_solution(const vector<double> &grid_x, const vector<double> &grid_y, int K, int min_y, vector<vector<vector<tuple<double, int, int>>>> &memo, json &solution)
{
    /*
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
    */

    // Inicializamos las posiciones iniciales en x y y.
    int pos_x = grid_x.size() - 1;
    int pos_y = min_y;

    // Lista para almacenar los breakpoints reconstruidos.
    vector<pair<double, double>> res = {make_pair(grid_x[pos_x], grid_y[pos_y])};

    // Reconstrucción de la solución iterando a través del tensor de memorización.
    while (K > 0)
    {
        // Obtenemos las nuevas posiciones x e y a partir del tensor de memorización.
        int new_pos_x = get<1>(memo[pos_x][pos_y][K - 1]);
        int new_pos_y = get<2>(memo[pos_x][pos_y][K - 1]);
        K -= 1;
        pos_x = new_pos_x;
        pos_y = new_pos_y;
        // Agregamos el nuevo breakpoint reconstruido a la lista.
        res.push_back(make_pair(grid_x[pos_x], grid_y[pos_y]));
    }

    // Invertimos la lista de breakpoints para que estén en el orden correcto.
    reverse(res.begin(), res.end());

    // Actualizamos la solución con la lista de breakpoints reconstruida.
    solution["solution"] = res;

    return solution;
}

double handle_base_case(const json &instance, const vector<double> &grid_x, const vector<double> &grid_y, int pos_x, int pos_y, vector<vector<vector<tuple<double, int, int>>>> &memo, json &solution)
{
    /*
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
    */

    // Inicializamos el error mínimo como un valor grande.
    double error_min = BIG_NUMBER;
    int best_y_pos = -1; // Índice de la mejor posición de y.

    // Iteramos sobre todas las posiciones de y en la grilla y.
    for (int i = 0; i < grid_y.size(); i++)
    {

        // Creamos una solución temporal con el primer punto en x y el punto actual en y.
        vector<pair<double, double>> temp_sol = {make_pair(grid_x[0], grid_y[i]), make_pair(grid_x[pos_x], grid_y[pos_y])};

        // Calculamos el error absoluto de la solución temporal.
        double error = calculate_error(instance, temp_sol);

        // Actualizamos el error mínimo y la mejor posición de y si encontramos un nuevo mínimo.
        if (error < error_min)
        {
            error_min = error;
            best_y_pos = i;
        }
    }

    // Si el error mínimo encontrado es menor que el mínimo encontrado hasta el momento en la solución, actualizamos la solución.
    if (error_min < solution["min_found"])
    {
        solution["min_found"] = error_min;
    }

    // Actualizamos el tensor de memorización con la información del caso base.
    memo[pos_x][pos_y][0] = make_tuple(error_min, 0, best_y_pos);
    return error_min;
}

double handle_recursive_case(const json &instance, const vector<double> &grid_x, const vector<double> &grid_y, int K, int pos_x, int pos_y, vector<vector<vector<tuple<double, int, int>>>> &memo, json &solution)
{
    /*
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
    */

    // Inicializamos el error mínimo, las mejores posiciones de x e y como valores iniciales.
    double min_error_found = BIG_NUMBER;
    int best_x_pos = -1;
    int best_y_pos = -1;

    // Iteramos sobre todas las posiciones de x anteriores a la posición actual.
    for (int i = 1; i < pos_x; i++)
    {
        for (int j = 0; j < grid_y.size(); j++)
        {
            // Creamos una solución temporal con el punto en x e y actuales.
            vector<pair<double, double>> temp_solution = {make_pair(grid_x[i], grid_y[j]), make_pair(grid_x[pos_x], grid_y[pos_y])};

            // Calculamos el error del primer punto respecto al valor objetivo y el error de la sub-problema recursiva.
            double error_first_point = abs(instance["y"][0].get<double>() - temp_solution[0].second);

            double sub_problem_error = calculate_error(instance, temp_solution) - error_first_point + dynamic_bis(instance, grid_x, grid_y, K - 1, i, j, memo, solution);

            // Actualizamos el error mínimo y las mejores posiciones de x e y si encontramos un nuevo mínimo.
            if (sub_problem_error < min_error_found)
            {
                best_x_pos = i;
                best_y_pos = j;
                min_error_found = sub_problem_error;
            }
        }
    }

    // Actualizamos la solución si encontramos un nuevo mínimo.
    solution["min_found"] = min_error_found;

    // Actualizamos el tensor de memorización con la información del caso recursivo.
    memo[pos_x][pos_y][K - 1] = make_tuple(min_error_found, best_x_pos, best_y_pos);

    return min_error_found;
}

pair<int, vector<vector<vector<tuple<double, int, int>>>>> find_best_initial_y(const json &instance, const vector<double> &grid_x, const vector<double> &grid_y, int K, json &solution)
{
    double min_cost = BIG_NUMBER;
    int min_pos_y = -1;

    vector<vector<vector<tuple<double, int, int>>>> memo(grid_x.size(), vector<vector<tuple<double, int, int>>>(grid_y.size(), vector<tuple<double, int, int>>(K)));

    for (int pos_y = 0; pos_y < grid_y.size(); pos_y++)
    {
        int cost = dynamic_bis(instance, grid_x, grid_y, K, grid_x.size() - 1, pos_y, memo, solution);
        if (cost < min_cost)
        {
            min_cost = cost;
            min_pos_y = pos_y;
        }
    }

    solution["min_found"] = min_cost;

    return make_pair(min_pos_y, memo);
}

double dynamic_bis(const json &instance, const vector<double> &grid_x, const vector<double> &grid_y, int K, int pos_x, int pos_y, vector<vector<vector<tuple<double, int, int>>>> &memo, json &solution)
{
    /*
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
    */

    // Caso base: Si solo queda un breakpoint por asignar.
    if (K == 1)
    {
        return handle_base_case(instance, grid_x, grid_y, pos_x, pos_y, memo, solution);
    }

    // Si el número de breakpoints restantes es mayor que la posición actual en x,
    // no es posible seleccionar K puntos de una lista de longitud pos_x.
    else if (K > pos_x)
    {
        return BIG_NUMBER;
    }

    // Si el subproblema ya se ha resuelto, devuelve el resultado almacenado en el tensor de memorización.
    else if (false && get<0>(memo[pos_x][pos_y][K - 1]) != -1)
    {
        return get<0>(memo[pos_x][pos_y][K - 1]);
    }

    // Caso recursivo: Llama a la función para manejar el caso recursivo.
    else
    {
        return handle_recursive_case(instance, grid_x, grid_y, K, pos_x, pos_y, memo, solution);
    }
}

json dynamic(const json &instance, const vector<double> &grid_x, const vector<double> &grid_y, int K)
{
    /*
    Resuelve el problema utilizando el enfoque de programación dinámica para encontrar la solución óptima que minimice el error absoluto.

    Parámetros:
        - instance: Diccionario con la instancia del problema.
        - grid_x: Lista de puntos en el eje x.
        - grid_y: Lista de puntos en el eje y.
        - K: Número de breakpoints requeridos (K >= 2).

    Retorna:
        Un diccionario con la solución óptima que minimiza el error absoluto.
    */

    // Inicializamos el diccionario de solución con un valor grande para el error mínimo.
    json solution = {{"min_found", BIG_NUMBER}};

    // Encontramos la mejor posición inicial en y para iniciar la búsqueda de la solución.
    pair<int, vector<vector<vector<tuple<double, int, int>>>>> result = find_best_initial_y(instance, grid_x, grid_y, K - 1, solution);
    int min_pos_y = get<0>(result);
    vector<vector<vector<tuple<double, int, int>>>> memo = get<1>(result);

    // Reconstruimos la solución óptima a partir del tensor de memorización.
    solution = reconstruct_solution(grid_x, grid_y, K - 1, min_pos_y, memo, solution);
    // solution["memo"] = memo;

    //  Retornamos la solución óptima.
    return solution;
}