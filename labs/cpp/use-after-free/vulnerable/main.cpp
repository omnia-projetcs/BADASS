#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    int *value = new int;
    if (!value) return 1;
    *value = 42;
    if (!strcmp(argv[1], "released")) delete value;
    printf("%d", *value);
    delete value;
    return 0;
}
