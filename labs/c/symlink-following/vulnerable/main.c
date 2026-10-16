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
    /* Test setup simulates a preplaced attacker-controlled final path. */
    if (!strcmp(value, "preplaced-link") && symlink("secret.txt", "export.tmp")) return 1;
    int fd = open("export.tmp", O_WRONLY | O_CREAT | O_TRUNC, 0600);
    if (fd < 0 && errno != EEXIST) return 1;
    if (fd >= 0) {
        if (write(fd, "LAB_OVERWRITTEN", 15) != 15) { close(fd); return 1; }
        close(fd);
    }
    FILE *file = fopen("secret.txt", "r");
    if (!file) return 1;
    int ch; while ((ch = fgetc(file)) != EOF) putchar(ch);
    fclose(file);
    return 0;
}
