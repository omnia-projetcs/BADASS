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
        long quantity = std::stol(value);
        if (quantity < -10000 || quantity > 10000) return 2;

        std::cout << 1000 - quantity * 10;
    } catch (const std::exception &error) {
        std::cerr << error.what();
        return 1;
    }
}
