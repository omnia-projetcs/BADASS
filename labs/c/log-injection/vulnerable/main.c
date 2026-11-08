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
    size_t n = strlen(value);
    char *encoded = malloc(n * 2 + 1);
    if (!encoded) return 1;
    size_t j = 0;
    for (size_t i = 0; i < n; ++i) {
        encoded[j++] = value[i];
    }
    encoded[j] = '\0';
    FILE *file = fopen("audit.log", "w");
    if (!file) { free(encoded); return 1; }
    fprintf(file, "user=%s", encoded);
    if (fclose(file)) { free(encoded); return 1; }
    free(encoded);
    file = fopen("audit.log", "r");
    if (!file) return 1;
    int ch; while ((ch = fgetc(file)) != EOF) putchar(ch);
    fclose(file);
    return 0;
}
