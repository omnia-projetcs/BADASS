#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    int *value = (int *)malloc(sizeof(int));
    if (!value) return 1;
    *value = 42;
    if (!strcmp(argv[1], "released")) { free(value); value = NULL; }
    if (!value) { puts("DENIED"); return 0; }
    printf("%d", *value);
    free(value);
    return 0;
}
