/* Signed length check rejecting negative and out-of-range values before unsigned conversion. */
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    char *end = NULL;
    errno = 0;
    long requested = strtol(argv[1], &end, 10);
    if (errno || end == argv[1] || *end || requested < 1 || requested > 64) {
        printf("DENIED");
        return 0;
    }
    unsigned int copy_len = (unsigned int)requested;
    printf("COPIED:%u", copy_len);
    return 0;
}
