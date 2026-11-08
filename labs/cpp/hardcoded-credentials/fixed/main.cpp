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
        const char *expected = std::getenv("BADASS_ADMIN_PASSWORD");
        std::cout << (expected && *expected && value == expected ? "ADMIN" : "DENIED");
    } catch (const std::exception &error) {
        std::cerr << error.what();
        return 1;
    }
}
