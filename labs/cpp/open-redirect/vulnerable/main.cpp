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

        std::cout << "Location: " << value;
    } catch (const std::exception &error) {
        std::cerr << error.what();
        return 1;
    }
}
