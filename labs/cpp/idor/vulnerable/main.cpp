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
        std::map<std::string, std::string> records{{"alice", "ALICE_DATA"}, {"bob", "BOB_PRIVATE"}};
        if (!records.count(value)) { std::cout << "NOT_FOUND"; return 0; }

        std::cout << records.at(value);
    } catch (const std::exception &error) {
        std::cerr << error.what();
        return 1;
    }
}
