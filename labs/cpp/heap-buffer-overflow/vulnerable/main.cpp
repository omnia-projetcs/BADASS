#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    char *buffer = new char[8];
    if (!buffer) return 1;
    strcpy(buffer, argv[1]);
    puts(buffer);
    delete[] buffer;
    return 0;
}
