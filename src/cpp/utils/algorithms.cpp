#include "../include/json.hpp"
#include "utils.h"
#include <iostream>

using namespace nlohmann;
using namespace std;

// Para tomar como valor arbitrariamente grande
const double BIG_NUMBER = 1e20;

// Declaración de la función (definición más adelante)
double dynamic_bis(const json &instance, const vector<double> &grid_x, const vector<double> &grid_y, int K, int pos_x, int pos_y, vector<vector<vector<tuple<double, int, int>>>> &memo, json &solution);

void brute_force_bis(const json &instance, const vector<double> &grid_x, const vector<double> &grid_y, int K, int pos_x, vector<pair<double, double>> &temp_solution, json &solution)
{
    /*
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
    */

    // Inicializamos el error mínimo encontrado hasta el momento (notar que comienza en BIG_NUMBER al iniciar la recursión).
    double min_error_found = solution["min_found"];

    // Caso base: si hemos alcanzado el final de la grilla x, hemos considerado todas las opciones para los breakpoints.
    if (pos_x == grid_x.size())
    {
        // Si la solución tiene tamaño K, calculamos el error absoluto de la solución actual como candidata a óptima.
        if (K == 0)
        {
            double current_min = calculate_error(instance, temp_solution);
            // Si el error de la solución actual es menor que el mínimo encontrado hasta el momento y abarca todo el conjunto de datos,
            // actualizamos la solución óptima con la nueva.
            if ((current_min < min_error_found) && temp_solution[0].first == grid_x[0] && temp_solution[temp_solution.size() - 1].first == grid_x[grid_x.size() - 1])
            {
                solution["solution"] = temp_solution;
                solution["min_found"] = current_min;
                return;
            }
            return;
        }
        else if (K > 0)
        {
            return;
        }
    } // Paso recursivo: consideramos agregar o no la coordenada de x actual (xi) a la solución (que haya un breakpoint de la forma (xi, *)).
    else
    {
        // Armamos las posibles soluciones sin considerar los breakpoints de la forma (xi, *).
        brute_force_bis(instance, grid_x, grid_y, K, pos_x + 1, temp_solution, solution);

        // Iteramos sobre todos los posibles breakpoints con coordenada de x en xi.
        for (int pos_y = 0; pos_y < grid_y.size(); ++pos_y)
        {
            vector<pair<double, double>> current_sol(temp_solution);
            current_sol.push_back(make_pair(grid_x[pos_x], grid_y[pos_y]));

            // Armamos las posibles soluciones tomando algún breakpoint de la forma (xi, *).
            brute_force_bis(instance, grid_x, grid_y, K - 1, pos_x + 1, current_sol, solution);
        }
    }
    return;
}

json brute_force(const json &instance, const vector<double> &grid_x, const vector<double> &grid_y, int K)
{
    /*
    Requiere:
        - instance: conjunto de datos no vacío.
        - |grid_x| > 1
        - |grid_y| > 0
        - 2 <= K <= |grid_x|

    Devuelve:
        Un diccionario con una lista de breakpoints tales que la función continua piecewise linear
        formada a partir de estos minimiza el error, y el error mínimo asociado.
    */

    // Inicializamos el error en uno muy grande para comparaciones.
    json solution = {{"min_found", BIG_NUMBER}};
    vector<pair<double, double>> temp_solution;

    // Inicializamos la función recursiva auxiliar.
    brute_force_bis(instance, grid_x, grid_y, K, 0, temp_solution, solution);
    return solution;
}

void back_tracking_bis(const json &instance, const vector<double> &grid_x, const vector<double> &grid_y, int K, int pos_x, vector<pair<double, double>> &temp_solution, json &solution)
{
    /*
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
    */

    // Inicializamos el error mínimo encontrado hasta el momento (notar que comienza en BIG_NUMBER al iniciar la recursión).
    double min_error_found = solution["min_found"];

    // Caso base: si no quedan breakpoints por asignar (|temp_solution| = K), calculamos el error absoluto de la solución actual.
    if (K == 0)
    {
        double current_min = calculate_error(instance, temp_solution);

        // Si el error de la solución actual es menor que el mínimo encontrado hasta el momento y abarca todo el conjunto de datos,
        // actualizamos la solución óptima con la nueva.
        if (current_min < min_error_found && temp_solution[0].first == grid_x[0] && temp_solution[temp_solution.size() - 1].first == grid_x[grid_x.size() - 1])
        {
            solution["solution"] = temp_solution;
            solution["min_found"] = current_min;
            return;
        }
        return; 
    }
    // Poda por factibilidad: se requieren más breakpoints de los que se pueden asignar.
    else if (K > grid_x.size() - pos_x)
    {                     
        return; 
    }
    // Poda por factibilidad: la solución temporal no contiene al primer punto de la grilla en x
    // (correspondiente al de la primer observación)
    else if (pos_x > 0 && temp_solution.size() > 0 && temp_solution[0].first != grid_x[0])
    { 
        return;
    }
    // Poda por optimalidad: el error actual supera al mínimo encontrado hasta el momento.
    else if (temp_solution.size() > 0 && calculate_error(instance, temp_solution) > min_error_found)
    { 
        return;
    }
    // Paso recursivo: consideramos agregar o no la coordenada de x actual (xi) a la solución (que haya un breakpoint de la forma (xi, *)).
    else
    {
        // Armamos las posibles soluciones sin considerar los breakpoints de la forma (xi, *).
        back_tracking_bis(instance, grid_x, grid_y, K, pos_x + 1, temp_solution, solution);

        // Iteramos sobre todos los posibles breakpoints con coordenada de x en xi.
        for (int pos_y = 0; pos_y < grid_y.size(); ++pos_y)
        {
            vector<pair<double, double>> current_sol(temp_solution);
            current_sol.push_back(make_pair(grid_x[pos_x], grid_y[pos_y]));

            // Armamos las posibles soluciones tomando algún breakpoint de la forma (xi, *).
            back_tracking_bis(instance, grid_x, grid_y, K - 1, pos_x + 1, current_sol, solution);
        }
    }
    return;
}

json back_tracking(const json &instance, const vector<double> &grid_x, const vector<double> &grid_y, int K)
{
    /*
    Requiere:
        - instance: conjunto de datos no vacío.
        - |grid_x| > 1
        - |grid_y| > 0
        - 2 <= K <= |grid_x|

    Devuelve:
        Un diccionario con una lista de breakpoints tales que la función continua piecewise linear
        formada a partir de estos minimiza el error, y el error mínimo asociado.
    */

    // Inicializamos el error en uno muy grande para comparaciones.
    json solution = {{"min_found", BIG_NUMBER}};
    vector<pair<double, double>> temp_solution; // []

    // Inicializamos la función recursiva auxiliar.
    back_tracking_bis(instance, grid_x, grid_y, K, 0, temp_solution, solution);
    return solution;
}

json reconstruct_solution(const vector<double> &grid_x, const vector<double> &grid_y, int K, int min_y, vector<vector<vector<tuple<double, int, int>>>> &memo, json &solution)
{
    /*
    Reconstruye la solución óptima a partir del memo generado durante la búsqueda del error mínimo.

    Devuelve:
        La solución actualizada con la lista de breakpoints reconstruida.
    */

    // Inicializamos las posiciones iniciales para x e y.
    int pos_x = grid_x.size() - 1;
    int pos_y = min_y;

    // Almacenamos la solución
    vector<pair<double, double>> res = {make_pair(grid_x[pos_x], grid_y[pos_y])};

    // Reconstrucción de la solución recorriendo memo.
    while (K > 0)
    {
        // Recuperamos las coordenadas que minimizan el sub problema resuelto.
        int new_pos_x = get<1>(memo[pos_x][pos_y][K - 1]);
        int new_pos_y = get<2>(memo[pos_x][pos_y][K - 1]);
        K -= 1;
        pos_x = new_pos_x;
        pos_y = new_pos_y;
        // Agregamos el nuevo breakpoint reconstruido a la solución.
        res.push_back(make_pair(grid_x[pos_x], grid_y[pos_y]));
    }

    // Ordenamos la lista de breakpoints de forma creciente en x.
    reverse(res.begin(), res.end());

    // Actualizamos la solución ya reconstruida.
    solution["solution"] = res;

    return solution;
}

double handle_base_case(const json &instance, const vector<double> &grid_x, const vector<double> &grid_y, int pos_x, int pos_y, vector<vector<vector<tuple<double, int, int>>>> &memo, json &solution)
{
    /*
    Maneja el caso base de dynamic_bis.

    Devuelve:
        El error mínimo encontrado en el caso base.
        F_1 ((t_pos_x, z_pos_y))
    */

    // Inicializamos el error mínimo con un valor grande.
    double error_min = BIG_NUMBER;

    // Índice de la mejor posición de y para la recta entre (ti, zi) y (tpos_x, zpos_y)
    int best_y_pos = -1; 

    // Iteramos sobre todas las posiciones de la grilla y.
    for (int i = 0; i < grid_y.size(); i++)
    {

        // Creamos una solución temporal con el primer punto en x y el punto actual en y.
        vector<pair<double, double>> temp_sol = {make_pair(grid_x[0], grid_y[i]), make_pair(grid_x[pos_x], grid_y[pos_y])};

        // Calculamos el error absoluto de la recta con la instancia.
        double error = calculate_error(instance, temp_sol);

        // Actualizamos el error mínimo y la mejor posición de y si encontramos un nuevo mínimo.
        if (error < error_min)
        {
            error_min = error;
            best_y_pos = i;
        }
    }

    // Actualizamos memo con la información del caso base una vez encontrado el mínimo.
    memo[pos_x][pos_y][0] = make_tuple(error_min, 0, best_y_pos);
    return error_min;
}

double handle_recursive_case(const json &instance, const vector<double> &grid_x, const vector<double> &grid_y, int M, int pos_x, int pos_y, vector<vector<vector<tuple<double, int, int>>>> &memo, json &solution)
{
    /*
    Maneja el caso recursivo de dynamic_bis.

    Devuelve:
        El error mínimo encontrado en el caso recursivo.
    */

    // Inicializamos el error mínimo en uno arbitrariamente grande,
    // y las mejores posiciones de x e y como valores iniciales (tales que minimicen la solución para (tpos_x, zpos_y), que viene de F_M)
    double min_error_found = BIG_NUMBER;
    int best_x_pos = -1;
    int best_y_pos = -1;

    // Iteramos sobre todas las posiciones de x anteriores en la grilla.
    // Calculamos F_{M}((tpos_x, zpos_y))
    for (int i = 1; i < pos_x; i++)
    {
        for (int j = 0; j < grid_y.size(); j++)
        {
            // Creamos una solución temporal con el punto en x e y actuales.
            vector<pair<double, double>> temp_solution = {make_pair(grid_x[i], grid_y[j]), make_pair(grid_x[pos_x], grid_y[pos_y])};

            // Calculamos el error del punto actual respecto al punto pasado por parámetro + el error de la sub-problema recursiva en el punto actual.
            double error_first_point = abs(instance["y"][0].get<double>() - temp_solution[0].second);

            double sub_problem_error = calculate_error(instance, temp_solution) - error_first_point + dynamic_bis(instance, grid_x, grid_y, M - 1, i, j, memo, solution);

            // Actualizamos el error mínimo y las mejores posiciones de x e y si encontramos un nuevo mínimo.
            if (sub_problem_error < min_error_found)
            {
                best_x_pos = i;
                best_y_pos = j;
                min_error_found = sub_problem_error;
            }
        }
    }

    // Actualizamos memo con la información del caso recursivo.
    memo[pos_x][pos_y][M - 1] = make_tuple(min_error_found, best_x_pos, best_y_pos);

    return min_error_found;
}

pair<int, vector<vector<vector<tuple<double, int, int>>>>> find_best_initial_y(const json &instance, const vector<double> &grid_x, const vector<double> &grid_y, int M, json &solution)
{
    /*
    Encuentra la mejor posición inicial en la grilla de discretización en y para iniciar la búsqueda de la solución óptima con programación dinámica.

    Retorna:
        La mejor posición inicial en y y la estructura usada para memoizar la solución durante la búsqueda (memo).
    */

    // Inicializamos el costo mínimo con un valor muy grande y la mejor posición en y como uno no alcanzable.
    double min_cost = BIG_NUMBER;
    int min_pos_y = -1;

    // Inicializamos la estructura de memoización.
    vector<vector<vector<tuple<double, int, int>>>> memo(grid_x.size(), vector<vector<tuple<double, int, int>>>(grid_y.size(), vector<tuple<double, int, int>>(M, make_tuple(-1.0, -1, -1))));

    // Consideramos todas las posibles posiciones iniciales en y.
    for (int pos_y = 0; pos_y < grid_y.size(); pos_y++)
    {   // Calculamos el costo de cada una utilizando el algoritmo de programación dinámica.
        double cost = dynamic_bis(instance, grid_x, grid_y, M, grid_x.size() - 1, pos_y, memo, solution);
        
        // Actualizamos el costo mínimo y la mejor posición en y si encontramos un nuevo mínimo.
        if (cost < min_cost)
        {
            min_cost = cost;
            min_pos_y = pos_y;
        }
    }

    // Actualizamos la solución con el costo mínimo encontrado.
    solution["min_found"] = min_cost;

    // Retornamos la mejor posición inicial en y y memo.
    return make_pair(min_pos_y, memo);
}

double dynamic_bis(const json &instance, const vector<double> &grid_x, const vector<double> &grid_y, int M, int pos_x, int pos_y, vector<vector<vector<tuple<double, int, int>>>> &memo, json &solution)
{
    /*
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
    */

    // Caso base
    if (M == 1)
    {
        return handle_base_case(instance, grid_x, grid_y, pos_x, pos_y, memo, solution);
    }

    // Si la cantidad de piezas faltantes no es compatible con la cantidad de puntos en la grilla x, se descarta la solución
    else if (M > pos_x)
    {
        return BIG_NUMBER;
    }

    // Si el subproblema ya se ha resuelto, devuelve el resultado almacenado en memo.
    else if (get<0>(memo[pos_x][pos_y][M - 1]) != -1)
    {
        return get<0>(memo[pos_x][pos_y][M - 1]);
    }

    // Paso recursivo
    else
    {
        return handle_recursive_case(instance, grid_x, grid_y, M, pos_x, pos_y, memo, solution);
    }
}

json dynamic(const json &instance, const vector<double> &grid_x, const vector<double> &grid_y, int K)
{
    /*
    Resuelve el problema utilizando el enfoque de programación dinámica top-down para encontrar la solución óptima que minimice el error absoluto.

    Requiere:
        - instance: conjunto de datos no vacío.
        - |grid_x| > 1
        - |grid_y| > 0
        - 2 <= K <= |grid_x|

    Devuelve:
        Un diccionario con una lista de K breakpoints tales que la función continua piecewise linear
        formada a partir de estos minimiza el error, y el error mínimo asociado.
    */

    // Inicializamos un error arbitrariamente grande.
    json solution = {{"min_found", BIG_NUMBER}};

    // Buscamos la posición de la grilla y que minimiza F_{K-1} ((t_m1, z_{min_y}))
    pair<int, vector<vector<vector<tuple<double, int, int>>>>> result = find_best_initial_y(instance, grid_x, grid_y, K - 1, solution);
    int min_pos_y = get<0>(result);
    vector<vector<vector<tuple<double, int, int>>>> memo = get<1>(result);

    // Reconstruimos la solución óptima a partir del memo creado.
    solution = reconstruct_solution(grid_x, grid_y, K - 1, min_pos_y, memo, solution);

    return solution;
}