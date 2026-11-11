#define _POSIX_C_SOURCE 200809L
#include <cstdio>
#include <fcntl.h>
#include <string_view>
#include <sys/stat.h>
#include <unistd.h>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    const std::string_view value = argv[1];
    const mode_t mode = (value == "public") ? 0644 : 0600;
    int fd = ::open("stored-secret", O_WRONLY | O_CREAT | O_EXCL, mode);
    if (fd < 0) return 1;
    const std::string_view content = (value == "public") ? "PUBLIC" : "LAB_SECRET";
    if (::write(fd, content.data(), content.size()) != static_cast<ssize_t>(content.size())) {
        ::close(fd);
        return 1;
    }
    if (::fchmod(fd, mode)) { ::close(fd); return 1; }
    struct stat info{};
    if (::fstat(fd, &info)) { ::close(fd); return 1; }
    ::close(fd);
    std::printf("%04o", static_cast<unsigned>(info.st_mode & 0777));
    return 0;
}
