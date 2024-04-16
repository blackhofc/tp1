#ifndef UTILS_H
#define UTILS_H

#include "../include/json.hpp"
#include "utils.h"

using namespace nlohmann;
using namespace std;

json brute_force(const json &instance, const vector<double> &grid_x, const vector<double> &grid_y, int K);
json back_tracking(const json &instance, const vector<double> &grid_x, const vector<double> &grid_y, int K);
json dynamic(const json &instance, const vector<double> &grid_x, const vector<double> &grid_y, int K);
vector<double> linespace(double start, double end, int num);

#endif