#include <errno.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_H2_WINDOW 0x7fffffffu
#define MAX_STAGING   64u

int main(int argc, char **argv) {
    if (argc != 2 || strlen(argv[1]) > 160) {
        fputs("INVALID", stdout);
        return 0;
    }
    const char *sep = strchr(argv[1], ':');
    if (!sep || sep == argv[1] || strlen(sep + 1) > 128) {
        fputs("INVALID", stdout);
        return 0;
    }
    char num[32];
    size_t nlen = (size_t)(sep - argv[1]);
    if (nlen >= sizeof(num)) {
        fputs("INVALID", stdout);
        return 0;
    }
    memcpy(num, argv[1], nlen);
    num[nlen] = '\0';

    char *end = NULL;
    errno = 0;
    unsigned long long parsed = strtoull(num, &end, 10);
    if (errno || !*num || *end || parsed > UINT32_MAX) {
        fputs("INVALID", stdout);
        return 0;
    }
    uint32_t inc = (uint32_t)parsed;
    uint32_t initial_window = 16u;
    if (inc == 0 || inc > MAX_H2_WINDOW - initial_window) {
        fputs("FLOW_CONTROL_ERROR", stdout);
        return 0;
    }

    const char *payload = sep + 1;
    size_t plen = strlen(payload);
    uint32_t updated_window = initial_window + inc;
    size_t alloc_size = updated_window < MAX_STAGING ? (size_t)updated_window : MAX_STAGING;
    if (plen > alloc_size) {
        fputs("FRAME_SIZE_ERROR", stdout);
        return 0;
    }

    char *staging = (char *)malloc(alloc_size);
    if (!staging) return 2;

    memcpy(staging, payload, plen);
    printf("OK:%zu", plen);
    free(staging);
    return 0;
}
