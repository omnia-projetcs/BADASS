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
        int size = std::stoi(value); if (size < 0) return 2;
        if (size > 100) { std::cout << "DENIED"; return 0; }
        std::vector<unsigned char> data(static_cast<size_t>(size), 0);
        std::cout << data.size();
    } catch (const std::exception &error) {
        std::cerr << error.what();
        return 1;
    }
}
