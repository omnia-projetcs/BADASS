// C++ signed-to-unsigned conversion bypassing a maximum length guard.
#include <cstdlib>
#include <iostream>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    int requested = std::atoi(argv[1]);
    if (requested > 64) {
        std::cout << "DENIED";
        return 0;
    }
    unsigned int copy_len = static_cast<unsigned int>(requested);
    if (copy_len > 64U) {
        std::cout << "OVERFLOW_LEN:" << copy_len;
        return 0;
    }
    std::cout << "COPIED:" << copy_len;
    return 0;
}
