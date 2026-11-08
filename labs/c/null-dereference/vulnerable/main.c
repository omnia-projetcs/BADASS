#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    int number = 42;
    int *value = !strcmp(argv[1], "missing") ? NULL : &number;
    printf("%d", *value);
    return 0;
}
