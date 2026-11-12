/* C tagged union checking the discriminant tag before accessing the union variant. */
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int tag;
    union {
        int guest_id;
        int admin_flag;
    } data;
} Principal;

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    char *end = NULL;
    errno = 0;
    long val = strtol(argv[1], &end, 10);
    if (errno || end == argv[1] || *end || val < 1 || val > 1000) {
        printf("DENIED");
        return 0;
    }
    Principal p;
    p.tag = 0;
    p.data.guest_id = (int)val;
    if (p.tag == 1 && p.data.admin_flag == 1337) {
        printf("ADMIN");
    } else {
        printf("GUEST:%d", p.data.guest_id);
    }
    return 0;
}
