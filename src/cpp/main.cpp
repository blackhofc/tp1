#include <string>
#include <iostream>
#include <fstream>
#include <chrono>

#include "include/json.hpp"

#include "utils/algorithms.h"
#include "utils/utils.h"

using namespace nlohmann;
using namespace std;

int main(int argc, char **argv)
{
    // Cargado del conjunto de datos a ajustar
    string instance_name = "../../data/titanium.json";
    cout << "Reading file " << instance_name << endl;
    ifstream input(instance_name);

    json instance = json::object();
    input >> instance;
    input.close();

    vector<double> instance_x = instance["x"];
    vector<double> instance_y = instance["y"];

    // Definir valores para m1 (grilla horizontal), m2 (grilla vertical) y K breakpoints
    int m1 = 49;
    int m2 = 49;
    int K = 25;

    // Se arma la discretización
    vector<double> grid_x = linespace(*min_element(instance_x.begin(), instance_x.end()),
                                      *max_element(instance_x.begin(), instance_x.end()), m1);
    vector<double> grid_y = linespace(*min_element(instance_y.begin(), instance_y.end()),
                                      *max_element(instance_y.begin(), instance_y.end()), m2);

    cout << K << " Brekpoints" << endl;

    json solution = json::object();
    auto start = chrono::steady_clock::now();

    // Para cada algoritmo cambiar el nombre a: brute_force(), back_tracking() o dynamic()
    // Todos toman los mismos parámetros para facilitar la alternancia de llamados
    solution = dynamic(instance, grid_x, grid_y, K);

    // Se mide el tiempo que demoró la ejecución
    auto end = std::chrono::steady_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - start) / 1000;
    std::cout << "Tiempo de ejecución: " << duration.count() << "s" << std::endl;

    // Almacenar la solución obtenida, útil para comparaciones y orden.
    ofstream output("dynamic.json");
    output << solution;
    output.close();

    return 0;
}