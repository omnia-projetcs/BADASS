#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct { char *value; } Request;
static Request request;
static const char *failure_stage;

static char *allocate(const char *stage, const char *value) {
    if (!strcmp(failure_stage, stage)) return NULL;
    char *result = malloc(strlen(value) + 1);
    if (result) memcpy(result, value, strlen(value) + 1);
    return result;
}

static int replace_value(void) {
    char *next = allocate("value", "UPDATED");
    if (!next) return 0;
    char *metadata = allocate("metadata", "COMPLETE");
    if (!metadata) { free(next); return 0; }
    char *previous = request.value;
    request.value = next;
    free(previous);
    free(metadata);
    return 1;
}

int main(int argc, char **argv) {
    if (argc != 2 || (strcmp(argv[1], "normal") && strcmp(argv[1], "oom-value")
                    && strcmp(argv[1], "oom-metadata") && strcmp(argv[1], "keep"))) {
        fputs("INVALID", stdout);
        return 0;
    }
    failure_stage = !strcmp(argv[1], "oom-value") ? "value" :
                    !strcmp(argv[1], "oom-metadata") ? "metadata" : "none";
    request.value = allocate("initial", "READY");
    if (!request.value) return 2;
    if (!strcmp(argv[1], "keep")) {
        fputs(request.value, stdout);
        free(request.value);
        return 0;
    }
    if (!replace_value()) {
        /* The corrected path reaches cleanup with a consistent old value. */
        if (strcmp(request.value, "READY")) abort();
        free(request.value);
        request.value = NULL;
        fputs("OOM_SAFE", stdout);
        return 0;
    }
    fputs(request.value, stdout);
    free(request.value);
    request.value = NULL;
    return 0;
}
