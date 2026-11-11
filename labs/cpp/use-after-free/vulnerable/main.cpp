#include <cstdio>
#include <cstring>
#include <new>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    int *value = new (std::nothrow) int;
    if (!value) return 1;
    *value = 42;
    if (!std::strcmp(argv[1], "released")) delete value;
    std::printf("%d", *value);
    delete value;
    return 0;
}
