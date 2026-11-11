#include <cstdio>
#include <cstring>
#include <new>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    char *buffer = new (std::nothrow) char[8];
    if (!buffer) return 1;
    std::strcpy(buffer, argv[1]);
    std::puts(buffer);
    delete[] buffer;
    return 0;
}
