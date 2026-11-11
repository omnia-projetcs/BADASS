#include <cstdio>
#include <cstring>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    char buffer[8];
    std::strcpy(buffer, argv[1]);
    std::puts(buffer);
    return 0;
}
