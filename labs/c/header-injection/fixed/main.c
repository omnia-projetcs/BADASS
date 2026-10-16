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
    if (strchr(value, '\r') || strchr(value, '\n')) { puts("DENIED"); return 0; }
    printf("X-User: %s\r\n\r\nBODY", value);
    return 0;
}
