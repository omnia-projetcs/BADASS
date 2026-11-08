#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    char *buffer = new char[8];
    if (!buffer) return 1;
    if (strlen(argv[1]) >= 8) { delete[] buffer; puts("DENIED"); return 0; }
    memcpy(buffer, argv[1], strlen(argv[1]) + 1);
    puts(buffer);
    delete[] buffer;
    return 0;
}
