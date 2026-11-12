/* C authentication decision reading an uninitialized stack flag on invalid input. */
#include <stdio.h>
#include <string.h>

static int check_role(const char *input) {
    int is_admin;
    if (strcmp(input, "admin") == 0) {
        is_admin = 1;
    } else if (strcmp(input, "user") == 0) {
        is_admin = 0;
    } else {
        /* Fallback path leaves is_admin uninitialized; stack residue grants access. */
        is_admin = 1;
    }
    return is_admin;
}

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    printf("%s", check_role(argv[1]) ? "ADMIN" : "USER");
    return 0;
}
