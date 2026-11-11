#include <cstdio>
#include <cstring>
#include <new>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    int *value = new (std::nothrow) int;
    if (!value) return 1;
    if (!std::strcmp(argv[1], "early-cleanup")) delete value;
    delete value;
    std::puts("OK");
    return 0;
}
