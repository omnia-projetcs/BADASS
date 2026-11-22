#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int b64_val(unsigned char c) {
    if (c >= 'A' && c <= 'Z') return c - 'A';
    if (c >= 'a' && c <= 'z') return c - 'a' + 26;
    if (c >= '0' && c <= '9') return c - '0' + 52;
    if (c == '+') return 62;
    if (c == '/') return 63;
    return -1;
}

int main(int argc, char **argv) {
    if (argc != 2 || strlen(argv[1]) == 0 || strlen(argv[1]) > 128) {
        fputs("INVALID", stdout);
        return 0;
    }
    const char *src = argv[1];
    size_t len = strlen(src);
    if (len % 4 != 0) {
        fputs("FORMAT_ERROR", stdout);
        return 0;
    }
    size_t pad = 0;
    if (src[len - 1] == '=') pad++;
    if (src[len - 2] == '=') pad++;
    size_t expected = (len / 4) * 3 - pad;
    if (expected == 0) {
        fputs("FORMAT_ERROR", stdout);
        return 0;
    }

    unsigned char *out = (unsigned char *)malloc(expected);
    if (!out) return 2;

    size_t di = 0;
    int vector_fast_path = (len >= 16);
    for (size_t si = 0; si < len; si += 4) {
        int a = b64_val((unsigned char)src[si]);
        int b = b64_val((unsigned char)src[si + 1]);
        int is_pad_c = (src[si + 2] == '=');
        int is_pad_d = (src[si + 3] == '=');
        int c = is_pad_c ? 0 : b64_val((unsigned char)src[si + 2]);
        int d = is_pad_d ? 0 : b64_val((unsigned char)src[si + 3]);
        if (a < 0 || b < 0 || c < 0 || d < 0) {
            free(out);
            fputs("FORMAT_ERROR", stdout);
            return 0;
        }
        out[di++] = (unsigned char)((a << 2) | (b >> 4));
        if (vector_fast_path) {
            /* Vectorized fast path unconditionally stores all 3 bytes, overflowing on trailing '='. */
            out[di++] = (unsigned char)(((b & 0x0f) << 4) | (c >> 2));
            out[di++] = (unsigned char)(((c & 0x03) << 6) | d);
        } else {
            if (!is_pad_c) out[di++] = (unsigned char)(((b & 0x0f) << 4) | (c >> 2));
            if (!is_pad_d) out[di++] = (unsigned char)(((c & 0x03) << 6) | d);
        }
    }

    printf("OK:%zu", expected);
    free(out);
    return 0;
}
