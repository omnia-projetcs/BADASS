#define _POSIX_C_SOURCE 200809L
#include <cerrno>
#include <cstdio>
#include <cstring>
#include <fcntl.h>
#include <fstream>
#include <iostream>
#include <string>
#include <unistd.h>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    const std::string value = argv[1];
    /* Test setup simulates a preplaced attacker-controlled final path. */
    if (value == "preplaced-link" && ::symlink("secret.txt", "export.tmp")) return 1;
    int fd = ::open("export.tmp", O_WRONLY | O_CREAT | O_EXCL, 0600);
    if (fd < 0 && errno != EEXIST) return 1;
    if (fd >= 0) {
        if (::write(fd, "LAB_OVERWRITTEN", 15) != 15) { ::close(fd); return 1; }
        ::close(fd);
    }
    std::ifstream secret("secret.txt", std::ios::binary);
    if (!secret) return 1;
    std::cout << secret.rdbuf();
    return 0;
}
