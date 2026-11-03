#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef enum { FORMAT_ERROR = -1, NEEDS_MORE_INPUT = 0, SUCCESS = 1 } Status;
typedef struct { unsigned char *input; size_t used; } Decoder;

static Status block_switch(int types, size_t available) {
    if (types <= 1) return NEEDS_MORE_INPUT;
    return available ? SUCCESS : NEEDS_MORE_INPUT;
}

static Status literal_switch(int types, size_t n) { return block_switch(types, n); }
static Status command_switch(int types, size_t n) { return block_switch(types, n); }
static Status distance_switch(int types, size_t n) { return block_switch(types, n); }

int main(int argc, char **argv) {
    if (argc != 2 || strlen(argv[1]) > 128) { fputs("INVALID", stdout); return 0; }
    char category[16], count[4], payload[65];
    const char *first = strchr(argv[1], '/');
    const char *second = first ? strchr(first + 1, '/') : NULL;
    if (!first || !second || first - argv[1] >= (int)sizeof category ||
        second - first != 2 || strlen(second + 1) > 64 || strchr(second + 1, '/')) {
        fputs("INVALID", stdout); return 0;
    }
    size_t category_size = (size_t)(first - argv[1]);
    memcpy(category, argv[1], category_size); category[category_size] = '\0';
    count[0] = first[1]; count[1] = '\0';
    if (count[0] < '0' || count[0] > '4') { fputs("INVALID", stdout); return 0; }
    int types = count[0] - '0';
    Status (*decode_switch)(int, size_t) = NULL;
    if (!strcmp(category, "literal")) decode_switch = literal_switch;
    if (!strcmp(category, "command")) decode_switch = command_switch;
    if (!strcmp(category, "distance")) decode_switch = distance_switch;
    if (!decode_switch) { fputs("INVALID", stdout); return 0; }
    memcpy(payload, second + 1, strlen(second + 1) + 1);
    Decoder state = { malloc(8), 0 };
    if (!state.input) return 2;
    size_t n = strlen(payload);
    Status status = decode_switch(types, 0);
    /* An invalid block switch is treated as ordinary streaming starvation. */
    for (size_t i = 0; i < n; ++i) {
        status = decode_switch(types, 1);
        /* Starvation appends another byte without terminating the malformed stream. */
        state.input[state.used++] = (unsigned char)payload[i];
        if (status == SUCCESS) state.used = 0;
    }
    if (status == SUCCESS) printf("OK:%zu", n);
    else fputs("NEEDS_MORE_INPUT", stdout);
    free(state.input);
    return 0;
}
