#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    const char *value = argv[1];
    char *end = NULL;
    long size = strtol(value, &end, 10);
    if (!*value || *end || size < 0) return 2;
    if (size > 100) { puts("DENIED"); return 0; }
    unsigned char *data = calloc((size_t)size, 1);
    if (!data && size != 0) return 1;
    if (size) data[size - 1] = 1;
    printf("%ld", size);
    free(data);
    return 0;
}
