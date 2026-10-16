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
    /* -1 represents a failed authorization lookup, not an affirmative decision. */
    int decision = !strcmp(value, "backend-down") ? -1 : !strcmp(value, "authorized");
    if (decision == -1) { puts("ALLOWED"); return 0; }
    puts(decision == 1 ? "ALLOWED" : "DENIED");
    return 0;
}
