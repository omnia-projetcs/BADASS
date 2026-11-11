#include <iostream>
#include <string_view>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    const std::string_view message = argv[1];
    std::cout << message;
    return 0;
}
