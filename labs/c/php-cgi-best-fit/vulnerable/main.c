#include <getopt.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int hex(unsigned char value) {
    if (value >= '0' && value <= '9') return value - '0';
    if (value >= 'a' && value <= 'f') return value - 'a' + 10;
    if (value >= 'A' && value <= 'F') return value - 'A' + 10;
    return -1;
}

int main(int argc, char **argv) {
    if (argc != 2 || strlen(argv[1]) > 256) { fputs("INVALID", stdout); return 0; }
    unsigned char decoded[257]; size_t used = 0;
    for (size_t i = 0; argv[1][i]; ++i) {
        unsigned char value = (unsigned char)argv[1][i];
        if (value == '%') {
            if (!argv[1][i + 1] || !argv[1][i + 2]) { fputs("INVALID", stdout); return 0; }
            int high = hex((unsigned char)argv[1][i + 1]), low = hex((unsigned char)argv[1][i + 2]);
            if (high < 0 || low < 0) { fputs("INVALID", stdout); return 0; }
            value = (unsigned char)(16 * high + low); i += 2;
        } else if (value == '+') value = ' ';
        if (!value || value < 32 || value == 127 || (value > 126 && value != 0xad)) {
            fputs("INVALID", stdout); return 0;
        }
        decoded[used++] = value;
    }
    decoded[used] = '\0';
    if (strchr(argv[1], '=')) { fputs("PUBLIC", stdout); return 0; }
    /* The dash check occurs before the modeled Windows best-fit conversion. */
    char *first = (char *)decoded;
    while (*first == ' ') ++first;
    if (*first == '-') { fputs("DENIED", stdout); return 0; }
    for (size_t i = 0; i < used; ++i) if (decoded[i] == 0xad) decoded[i] = '-';
    char *arguments[10] = { "cgi-model" }; int argument_count = 1;
    char *piece = strtok((char *)decoded, " ");
    while (piece) {
        if (argument_count == 9) { fputs("INVALID", stdout); return 0; }
        arguments[argument_count++] = piece; piece = strtok(NULL, " ");
    }
    arguments[argument_count] = NULL;
    opterr = 0; optind = 1; int option, include_private = 0;
    while ((option = getopt(argument_count, arguments, "+d:")) != -1) {
        if (option != 'd' || strcmp(optarg, "include_private=1")) { fputs("INVALID", stdout); return 0; }
        include_private = 1;
    }
    fputs(include_private ? "LAB_PRIVATE_CONFIG" : "PUBLIC", stdout);
    return 0;
}
