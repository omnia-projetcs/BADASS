#include <charconv>
#include <iostream>
#include <string_view>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    const std::string_view value = argv[1];
    int index = 0;
    const auto result = std::from_chars(value.data(), value.data() + value.size(), index);
    if (result.ec != std::errc{} || result.ptr != value.data() + value.size()) {
        std::cout << "DENIED";
        return 0;
    }
    int values[3] = {10, 20, 30};
    if (index < 0 || index >= 3) { std::cout << "DENIED"; return 0; }
    std::cout << values[index];
}
