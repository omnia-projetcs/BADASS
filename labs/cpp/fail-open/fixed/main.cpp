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
        try {
            if (value == "backend-down") throw std::runtime_error("backend unavailable");
            std::cout << (value == "authorized" ? "ALLOWED" : "DENIED");
        } catch (const std::runtime_error &) { std::cout << "DENIED"; }
    } catch (const std::exception &error) {
        std::cerr << error.what();
        return 1;
    }
}
