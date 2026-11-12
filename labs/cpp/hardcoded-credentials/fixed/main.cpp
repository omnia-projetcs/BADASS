#include <cstdlib>
#include <iostream>
#include <string_view>

static bool constant_time_equals(std::string_view a, std::string_view b) {
    const std::size_t max_len = a.size() > b.size() ? a.size() : b.size();
    unsigned char diff = static_cast<unsigned char>(a.size() ^ b.size());
    for (std::size_t i = 0; i < max_len; ++i) {
        unsigned char ca = i < a.size() ? static_cast<unsigned char>(a[i]) : 0;
        unsigned char cb = i < b.size() ? static_cast<unsigned char>(b[i]) : 0;
        diff |= static_cast<unsigned char>(ca ^ cb);
    }
    return diff == 0;
}

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    const std::string_view value = argv[1];
    const char *expected = std::getenv("BADASS_ADMIN_PASSWORD");
    std::cout << (expected && *expected && constant_time_equals(value, expected) ? "ADMIN" : "DENIED");
    return 0;
}
