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
    int fd = open("stored-secret", O_WRONLY | O_CREAT | O_EXCL, 0600);
    if (fd < 0) return 1;
    const char *content = !strcmp(value, "public") ? "PUBLIC" : "LAB_SECRET";
    if (write(fd, content, strlen(content)) != (ssize_t)strlen(content)) { close(fd); return 1; }
    if (fchmod(fd, 0644)) { close(fd); return 1; }
    struct stat info;
    if (fstat(fd, &info)) { close(fd); return 1; }
    close(fd);
    printf("%04o", (unsigned)(info.st_mode & 0777));
    return 0;
}
