/* Signed length check bypassed when negative int converts to unsigned size_t. */
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    int requested = atoi(argv[1]);
    if (requested > 64) {
        printf("DENIED");
        return 0;
    }
    unsigned int copy_len = (unsigned int)requested;
    if (copy_len > 64U) {
        printf("OVERFLOW_LEN:%u", copy_len);
        return 0;
    }
    printf("COPIED:%u", copy_len);
    return 0;
}
