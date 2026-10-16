#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    char *buffer = (char *)malloc(8);
    if (!buffer) return 1;
    if (strlen(argv[1]) >= 8) { free(buffer); puts("DENIED"); return 0; }
    memcpy(buffer, argv[1], strlen(argv[1]) + 1);
    puts(buffer);
    free(buffer);
    return 0;
}
