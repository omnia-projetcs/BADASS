#include <cstdio>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    std::printf(argv[1], 42);
    return 0;
}
