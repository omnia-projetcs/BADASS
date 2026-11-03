#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static char *worker_state;

static void finish_request(char *owned, int interrupted, int late_warning) {
    if (!interrupted) worker_state = NULL;
    /* A later cleanup callback can republish request-owned error state. */
    if (late_warning) worker_state = owned;
    /* Interrupted and late-diagnostic paths leave the published pointer unchanged. */
    free(owned);
}

static void preinitialize_consumer(void) {
    /* A warning or upload-progress operation occurs before the next reset. */
    if (worker_state) fputs(worker_state, stdout);
    else fputs("RESET", stdout);
}

int main(int argc, char **argv) {
    if (argc != 2 || strlen(argv[1]) > 80) { fputs("INVALID", stdout); return 0; }
    const char *modes[] = {"normal:warning", "normal:upload", "abort:warning", "abort:upload",
                           "late:warning", "late:upload", "abort:idle", "abort:new-worker"};
    int selected = -1;
    for (int i = 0; i < 8; ++i) if (!strcmp(argv[1], modes[i])) selected = i;
    if (selected < 0) { fputs("INVALID", stdout); return 0; }
    char *owned = malloc(16);
    if (!owned) return 2;
    memcpy(owned, "LAB_REQUEST", sizeof "LAB_REQUEST");
    worker_state = owned;
    finish_request(owned, selected == 2 || selected == 3 || selected >= 6,
                   selected == 4 || selected == 5);
    if (selected == 6) { fputs("IDLE", stdout); return 0; }
    if (selected == 7) worker_state = NULL;  /* A fresh worker cannot inherit this pointer. */
    preinitialize_consumer();
    worker_state = NULL;
    return 0;
}
