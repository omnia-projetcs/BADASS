/* C authentication decision initializing the authorization flag to safe default 0. */
#include <stdio.h>
#include <string.h>

static const char *check_role(const char *input) {
    int is_admin = 0;
    if (strcmp(input, "admin") == 0) {
        is_admin = 1;
    } else if (strcmp(input, "user") == 0) {
        is_admin = 0;
    } else {
        return "DENIED";
    }
    return is_admin ? "ADMIN" : "USER";
}

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    printf("%s", check_role(argv[1]));
    return 0;
}
