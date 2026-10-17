#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    int values[3] = {10,20,30};
    const char *input = argv[1];
    char *end = NULL;
    errno = 0;
    long index = strtol(input, &end, 10);
    /* A complete decimal integer is required before applying array bounds. */
    if (errno || end == input || *end ||
        (*input != '-' && (*input < '0' || *input > '9'))) {
        puts("DENIED");
        return 0;
    }
    if (index < 0 || index >= 3) { puts("DENIED"); return 0; }
    printf("%d", values[index]);
    return 0;
}
