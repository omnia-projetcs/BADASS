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
    struct Account { const char *owner; const char *data; };
    struct Account records[] = {{"alice", "ALICE_DATA"}, {"bob", "BOB_PRIVATE"}};
    for (size_t i = 0; i < 2; ++i) {
        if (!strcmp(value, records[i].owner)) {

            puts(records[i].data); return 0;
        }
    }
    puts("NOT_FOUND");
    return 0;
}
