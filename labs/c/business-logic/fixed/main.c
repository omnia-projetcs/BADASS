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
    long quantity = strtol(value, &end, 10);
    if (!*value || *end || quantity < -10000 || quantity > 10000) return 2;
    if (quantity < 1 || quantity > 100) { puts("DENIED"); return 0; }
    printf("%ld", 1000 - quantity * 10);
    return 0;
}
