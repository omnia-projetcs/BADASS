#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    int *value = (int *)malloc(sizeof(int));
    if (!value) return 1;
    if (!strcmp(argv[1], "early-cleanup")) { free(value); value = NULL; }
    free(value);
    puts("OK");
    return 0;
}
