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
    if (!strcmp(value, "ok")) { puts("OK"); return 0; }
    FILE *file = fopen("missing-database", "r");
    if (!file) { puts("Service unavailable"); return 0; }
    fclose(file); puts("OK");
    return 0;
}
