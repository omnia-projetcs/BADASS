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
        std::string encoded;
        for (char ch : value) { encoded += ch; }
        { std::ofstream file("audit.log"); file.exceptions(std::ios::failbit | std::ios::badbit); file << "user=" << encoded; }
        std::ifstream file("audit.log"); if (!file) throw std::runtime_error("log read failed");
        std::cout << file.rdbuf();
    } catch (const std::exception &error) {
        std::cerr << error.what();
        return 1;
    }
}
