#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <map>
#include <cstdlib>
#include <stdexcept>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    const std::string value = argv[1];
    try {
        if (value == "ok") { std::cout << "OK"; return 0; }
        std::ifstream file("missing-database");
        std::cout << (!file ? "Service unavailable" : "OK");
    } catch (const std::exception &error) {
        std::cerr << error.what();
        return 1;
    }
}
