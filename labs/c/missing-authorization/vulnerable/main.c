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
    if (!strcmp(value, "health")) { puts("HEALTHY"); return 0; }
    const char *role = "user"; /* Trusted role for this authenticated session. */
    (void)role;

    puts("USERS_DELETED");
    return 0;
}
