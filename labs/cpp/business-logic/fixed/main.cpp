#include <charconv>
#include <iostream>
#include <string_view>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    const std::string_view value = argv[1];
    long quantity = 0;
    const auto result = std::from_chars(value.data(), value.data() + value.size(), quantity);
    if (result.ec != std::errc{} || result.ptr != value.data() + value.size()) {
        std::cout << "DENIED";
        return 0;
    }
    if (quantity < 1 || quantity > 100) { std::cout << "DENIED"; return 0; }
    std::cout << 1000 - quantity * 10;
}
