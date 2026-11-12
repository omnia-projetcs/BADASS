// C++ signed-to-unsigned conversion guarded by strict positive range validation.
#include <cerrno>
#include <cstdlib>
#include <iostream>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    char *end = nullptr;
    errno = 0;
    long requested = std::strtol(argv[1], &end, 10);
    if (errno || end == argv[1] || *end || requested < 1 || requested > 64) {
        std::cout << "DENIED";
        return 0;
    }
    unsigned int copy_len = static_cast<unsigned int>(requested);
    std::cout << "COPIED:" << copy_len;
    return 0;
}
