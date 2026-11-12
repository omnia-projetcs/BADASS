#include <cstdio>
#include <cstring>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    int number = 42;
    int *value = !std::strcmp(argv[1], "missing") ? nullptr : &number;
    std::printf("%d", *value);
    return 0;
}
