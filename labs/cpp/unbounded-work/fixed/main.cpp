#include <charconv>
#include <iostream>
#include <string_view>
#include <vector>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    const std::string_view value = argv[1];
    int size = 0;
    const auto result = std::from_chars(value.data(), value.data() + value.size(), size);
    if (result.ec != std::errc{} || result.ptr != value.data() + value.size() || size < 0) {
        std::cout << "DENIED";
        return 0;
    }
    if (size > 100) { std::cout << "DENIED"; return 0; }
    std::vector<unsigned char> data(static_cast<size_t>(size), 0);
    std::cout << data.size();
}
