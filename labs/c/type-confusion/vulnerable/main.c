/* C tagged union reading a privileged pointer/flag without verifying the active tag. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int tag; /* 0 = guest id, 1 = admin badge */
    union {
        int guest_id;
        int admin_flag;
    } data;
} Principal;

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    Principal p;
    p.tag = 0;
    p.data.guest_id = atoi(argv[1]);
    /* Type confusion: reads data.admin_flag without checking p.tag == 1. */
    if (p.data.admin_flag == 1337) {
        printf("ADMIN");
    } else {
        printf("GUEST:%d", p.data.guest_id);
    }
    return 0;
}
