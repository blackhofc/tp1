#include <string>
#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>

#include "include/json.hpp"

// Para libreria de JSON.
using namespace nlohmann;

const double BIG_NUMBER = 1e10;

double calculate_min_error(const json &instance, const std::vector<std::pair<double, double>> &solution)
{
    double min_error = std::abs(instance["y"][0].get<double>() - solution[0].second); // Error of the first point

    for (int point = 0; point < instance["x"].size(); ++point)
    {
        for (int sol_index = 0; sol_index < solution.size() - 1; ++sol_index)
        {
            if (instance["x"][point] > solution[sol_index].first &&
                instance["x"][point] <= solution[sol_index + 1].first)
            {
                double delta = (solution[sol_index + 1].second - solution[sol_index].second) /
                               (solution[sol_index + 1].first - solution[sol_index].first);
                // Inside the loop
                double estimation_y = delta * (instance["x"][point].get<double>() - solution[sol_index].first);
                min_error += std::abs(instance["y"][point].get<double>() - estimation_y);
            }
        }
    }

    return min_error;
}

double brute_force_bis(const json &instance,
                       const std::vector<double> &grid_x,
                       const std::vector<double> &grid_y,
                       int K,
                       int pos_x,
                       std::vector<std::pair<double, double>> &temp_solution,
                       json &solution)
{
    double min_error_found = solution["min_found"];

    if (K == 0)
    {
        double current_min = calculate_min_error(instance, temp_solution);
        if (current_min < min_error_found &&
            temp_solution[0].first == grid_x[0] &&
            temp_solution[temp_solution.size() - 1].first == grid_x[grid_x.size() - 1])
        {
            solution["solution"] = temp_solution;
            solution["min_found"] = current_min;
            return current_min;
        }
        return BIG_NUMBER;
    }
    else if (K > grid_x.size() - pos_x)
    {
        return BIG_NUMBER;
    }
    else
    {
        double error_without_x = brute_force_bis(instance, grid_x, grid_y, K, pos_x + 1, temp_solution, solution);
        for (int pos_y = 0; pos_y < grid_y.size(); ++pos_y)
        {
            std::vector<std::pair<double, double>> current_sol(temp_solution);
            current_sol.push_back(std::make_pair(grid_x[pos_x], grid_y[pos_y]));

            double error_with_x = brute_force_bis(instance, grid_x, grid_y, K - 1, pos_x + 1, current_sol, solution);
            min_error_found = std::min(min_error_found, std::min(error_with_x, error_without_x));
            solution["min_found"] = min_error_found;
        }
    }
    return min_error_found;
}

json brute_force(const json &instance, const std::vector<double> &grid_x, const std::vector<double> &grid_y, int K)
{
    json solution = {{"min_found", BIG_NUMBER}};
    std::vector<std::pair<double, double>> temp_solution;

    brute_force_bis(instance, grid_x, grid_y, K, 0, temp_solution, solution);
    return solution;
}

// Function to generate linspace array
std::vector<double> linspace(double start, double end, int num)
{
    std::vector<double> result(num);
    double step = (end - start) / (num - 1);
    for (int i = 0; i < num; ++i)
    {
        result[i] = start + i * step;
    }
    return result;
}

int main(int argc, char **argv)
{
    std::string instance_name = "../../data/titanium.json";
    std::cout << "Reading file " << instance_name << std::endl;
    std::ifstream input(instance_name);

    json instance = json::object();
    input >> instance;
    input.close();

    std::vector<double> instance_x = instance["x"];
    std::vector<double> instance_y = instance["y"];

    // Parameters for linspace
    int K = 5;
    int m = 6; // Number of points for grid_x
    int n = 6; // Number of points for grid_y

    // Generating grid_x
    std::vector<double> grid_x = linspace(*std::min_element(instance_x.begin(), instance_x.end()),
                                          *std::max_element(instance_x.begin(), instance_x.end()), m);

    // Generating grid_y
    std::vector<double> grid_y = linspace(*std::min_element(instance_y.begin(), instance_y.end()),
                                          *std::max_element(instance_y.begin(), instance_y.end()), n);

    std::cout << K << std::endl;

    // Aca empieza la magia.??

    // Ejemplo para guardar json.
    // Probamos guardando el mismo JSON de instance, pero en otro archivo.
    json test = json::object();

    test = brute_force(instance, grid_x, grid_y, K);
    test["grid"]["x"] = grid_x;
    std::ofstream output("c.json");
    output << test;
    output.close();

    return 0;
}