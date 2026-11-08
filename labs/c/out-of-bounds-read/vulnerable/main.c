#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    int values[3] = {10,20,30};
    int index = atoi(argv[1]);
    printf("%d", values[index]);
    return 0;
}
