#include <charconv>
#include <cstdint>
#include <iostream>
#include <limits>
#include <string_view>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    const std::string_view value = argv[1];
    std::uint32_t quantity = 0;
    /* Unsigned from_chars rejects negative values and reports range errors. */
    const auto result = std::from_chars(value.data(), value.data() + value.size(), quantity);
    if (result.ec != std::errc{} || result.ptr != value.data() + value.size()) {
        std::cout << "DENIED";
        return 0;
    }
    if (quantity > std::numeric_limits<std::uint32_t>::max() / 100u) {
        std::cout << "DENIED";
        return 0;
    }
    const std::uint32_t total = quantity * 100u;
    std::cout << total;
}
