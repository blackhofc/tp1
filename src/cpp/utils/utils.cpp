#include "utils.h"
#include "../include/json.hpp"

using namespace nlohmann;
using namespace std;

// Function to generate linspace array
vector<double> linespace(double start, double end, int num)
{
    vector<double> result(num);
    double step = (end - start) / (num - 1);
    for (int i = 0; i < num; ++i)
    {
        result[i] = start + i * step;
    }
    return result;
}

double line(double t_prime, double y_prime, double t_double_prime, double y_double_prime, double t)
{
    return ((y_double_prime - y_prime) / (t_double_prime - t_prime)) * (t - t_prime) + y_prime;
}

double absolute_error(double xi, double yi, double t_prime, double y_prime, double t_double_prime, double y_double_prime)
{
    double y_predicted = line(t_prime, y_prime, t_double_prime, y_double_prime, xi);
    return abs(yi - y_predicted);
}

double calculate_min_error(const json &instance, const vector<pair<double, double>> &solution)
{
    double min_error = abs(instance["y"][0].get<double>() - solution[0].second);

    for (size_t point = 1; point < instance["x"].size(); ++point)
    {
        double xi = instance["x"][point].get<double>();
        double yi = instance["y"][point].get<double>();

        for (size_t sol_index = 0; sol_index < solution.size() - 1; ++sol_index)
        {
            double t_prime = solution[sol_index].first;
            double y_prime = solution[sol_index].second;
            double t_double_prime = solution[sol_index + 1].first;
            double y_double_prime = solution[sol_index + 1].second;

            if (t_prime < xi && xi <= t_double_prime)
            {
                double error = absolute_error(xi, yi, t_prime, y_prime, t_double_prime, y_double_prime);
                min_error += error;
                break;
            }
        }
    }

    return min_error;
}