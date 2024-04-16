#ifndef UTILS_H
#define UTILS_H

#include <vector>
#include "../include/json.hpp"

using namespace nlohmann;
using namespace std;

// Function declarations
double line(double t_prime, double y_prime, double t_double_prime, double y_double_prime, double t);
double absolute_error(double xi, double yi, double t_prime, double y_prime, double t_double_prime, double y_double_prime);
double calculate_error(const json &instance, const vector<pair<double, double>> &solution);
vector<double> linespace(double start, double end, int num);

#endif // UTILS_H
