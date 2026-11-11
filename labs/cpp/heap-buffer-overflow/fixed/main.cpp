#include <cstdio>
#include <cstring>
#include <new>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    char *buffer = new (std::nothrow) char[8];
    if (!buffer) return 1;
    if (strlen(argv[1]) >= 8) { delete[] buffer; std::puts("DENIED"); return 0; }
    std::memcpy(buffer, argv[1], std::strlen(argv[1]) + 1);
    std::puts(buffer);
    delete[] buffer;
    return 0;
}
