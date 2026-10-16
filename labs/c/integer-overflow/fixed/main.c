#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <inttypes.h>
#include <errno.h>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    char *end = NULL;
    errno = 0;
    unsigned long long parsed = strtoull(argv[1], &end, 10);
    if (errno || !*argv[1] || *end || parsed > UINT32_MAX) return 2;
    uint32_t quantity = (uint32_t)parsed;
    if (quantity > UINT32_MAX / 100u) { puts("DENIED"); return 0; }
    uint32_t total = quantity * 100u;
    printf("%" PRIu32, total);
    return 0;
}
