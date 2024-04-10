#include "../include/json.hpp"
#include "utils.h"

using namespace nlohmann;
using namespace std;

const double BIG_NUMBER = 1e10;

double brute_force_bis(const json &instance, const vector<double> &grid_x, const vector<double> &grid_y,
                       int K, int pos_x,
                       vector<pair<double, double>> &temp_solution,
                       json &solution)
{
    double min_error_found = solution["min_found"];

    solution["recursion"] = solution["recursion"].get<int>() + 1;

    if (pos_x == grid_x.size())
    {
        if (K == 0)
        {
            double current_min = calculate_min_error(instance, temp_solution);
            if (current_min < min_error_found && temp_solution[0].first == grid_x[0] && temp_solution[temp_solution.size() - 1].first == grid_x[grid_x.size() - 1])
            {
                solution["solution"] = temp_solution;
                solution["min_found"] = current_min;
                return current_min;
            }
            return BIG_NUMBER;
        }
        else if (K > 0)
        {
            return BIG_NUMBER;
        }
    }
    else
    {
        double error_without_x = brute_force_bis(instance, grid_x, grid_y, K, pos_x + 1, temp_solution, solution);
        for (int pos_y = 0; pos_y < grid_y.size(); ++pos_y)
        {
            vector<pair<double, double>> current_sol(temp_solution);
            current_sol.push_back(make_pair(grid_x[pos_x], grid_y[pos_y]));

            double error_with_x = brute_force_bis(instance, grid_x, grid_y, K - 1, pos_x + 1, current_sol, solution);

            min_error_found = min(min_error_found, min(error_with_x, error_without_x));
            solution["min_found"] = min_error_found;
        }
    }
    return min_error_found;
}

json brute_force(const json &instance, const vector<double> &grid_x, const vector<double> &grid_y, int K)
{
    json solution = {{"min_found", BIG_NUMBER}, {"recursion", 0}};
    vector<pair<double, double>> temp_solution;

    brute_force_bis(instance, grid_x, grid_y, K, 0, temp_solution, solution);
    return solution;
}

double back_tracking_bis(const json &instance, const vector<double> &grid_x, const vector<double> &grid_y,
                         int K, int pos_x,
                         vector<pair<double, double>> &temp_solution,
                         json &solution)
{
    double min_error_found = solution["min_found"];

    solution["recursion"] = solution["recursion"].get<int>() + 1;

    if (K == 0)
    {
        double current_min = calculate_min_error(instance, temp_solution);
        if (current_min < min_error_found && temp_solution[0].first == grid_x[0] && temp_solution[temp_solution.size() - 1].first == grid_x[grid_x.size() - 1])
        {
            solution["solution"] = temp_solution;
            solution["min_found"] = current_min;
            return current_min;
        }
        return BIG_NUMBER;
    }
    else if (K > grid_x.size() - pos_x)
    { // Poda por factibilidad
        return BIG_NUMBER;
    }
    else if (pos_x > 0 && temp_solution.size() > 0 && temp_solution[0].first != grid_x[0])
    { // Poda por factibilidad
        return BIG_NUMBER;
    }
    else if (temp_solution.size() > 0 && calculate_min_error(instance, temp_solution) > min_error_found)
    { // Poda por Optimalidad
        return BIG_NUMBER;
    }
    else
    {
        double error_without_x = back_tracking_bis(instance, grid_x, grid_y, K, pos_x + 1, temp_solution, solution);
        for (int pos_y = 0; pos_y < grid_y.size(); ++pos_y)
        {
            vector<pair<double, double>> current_sol(temp_solution);
            current_sol.push_back(make_pair(grid_x[pos_x], grid_y[pos_y]));

            double error_with_x = back_tracking_bis(instance, grid_x, grid_y, K - 1, pos_x + 1, current_sol, solution);

            min_error_found = min(min_error_found, min(error_with_x, error_without_x));
            solution["min_found"] = min_error_found;
        }
    }
    return min_error_found;
}

json back_tracking(const json &instance, const vector<double> &grid_x, const vector<double> &grid_y, int K)
{
    json solution = {{"min_found", BIG_NUMBER}, {"recursion", 0}};
    vector<pair<double, double>> temp_solution; // []

    back_tracking_bis(instance, grid_x, grid_y, K, 0, temp_solution, solution);
    return solution;
}