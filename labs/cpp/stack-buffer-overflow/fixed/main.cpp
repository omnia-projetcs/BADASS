#include <cstdio>
#include <cstring>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    char buffer[8];
    if (strlen(argv[1])>=sizeof buffer) {
        std::puts("DENIED");
        return 0;
    }
    std::memcpy(buffer, argv[1], std::strlen(argv[1]) + 1);
    std::puts(buffer);
    return 0;
}
