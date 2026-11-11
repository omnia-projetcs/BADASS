#include <cerrno>
#include <cinttypes>
#include <cstdint>
#include <cstdio>
#include <cstdlib>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    char *end = nullptr;
    errno = 0;
    unsigned long long parsed = std::strtoull(argv[1], &end, 10);
    if (errno || !*argv[1] || *end || parsed > UINT32_MAX) return 2;
    std::uint32_t quantity = static_cast<std::uint32_t>(parsed);
    std::uint32_t total = quantity * 100u;
    std::printf("%" PRIu32, total);
    return 0;
}
