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
    string instance_name = "../../data/titanium.json";
    cout << "Reading file " << instance_name << endl;
    ifstream input(instance_name);

    json instance = json::object();
    input >> instance;
    input.close();

    vector<double> instance_x = instance["x"];
    vector<double> instance_y = instance["y"];

    // Parameters for linspace
    int m = 10; // Number of points for grid_x
    int n = 10; // Number of points for grid_y
    int K = 9;

    // Generating grid_x
    vector<double> grid_x = linespace(*min_element(instance_x.begin(), instance_x.end()),
                                      *max_element(instance_x.begin(), instance_x.end()), m);

    // Generating grid_y
    vector<double> grid_y = linespace(*min_element(instance_y.begin(), instance_y.end()),
                                      *max_element(instance_y.begin(), instance_y.end()), n);

    cout << K << " Brekpoints" << endl;

    json solution = json::object();

    auto start = chrono::steady_clock::now();

    solution = dynamic(instance, grid_x, grid_y, K);

    // Capture the end time
    auto end = std::chrono::steady_clock::now();

    // Calculate the duration
    auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - start) / 1000;

    // Output the duration
    std::cout << "Execution time: " << duration.count() << " second" << std::endl;

    ofstream output("dynamic.json");
    output << solution;
    output.close();

    return 0;
}