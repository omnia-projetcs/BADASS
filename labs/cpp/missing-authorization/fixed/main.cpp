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
        if (value == "health") { std::cout << "HEALTHY"; return 0; }
        const std::string role = "user";
        if (role != "admin") { std::cout << "DENIED"; return 0; }
        std::cout << "USERS_DELETED";
    } catch (const std::exception &error) {
        std::cerr << error.what();
        return 1;
    }
}
