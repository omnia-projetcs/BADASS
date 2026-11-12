#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int constant_time_equals(const char *a, const char *b) {
    size_t len_a = strlen(a);
    size_t len_b = strlen(b);
    size_t max_len = len_a > len_b ? len_a : len_b;
    unsigned char diff = (unsigned char)(len_a ^ len_b);
    for (size_t i = 0; i < max_len; ++i) {
        unsigned char ca = i < len_a ? (unsigned char)a[i] : 0;
        unsigned char cb = i < len_b ? (unsigned char)b[i] : 0;
        diff |= (unsigned char)(ca ^ cb);
    }
    return diff == 0;
}

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    const char *value = argv[1];
    const char *expected = getenv("BADASS_ADMIN_PASSWORD");
    puts(expected && *expected && constant_time_equals(value, expected) ? "ADMIN" : "DENIED");
    return 0;
}
