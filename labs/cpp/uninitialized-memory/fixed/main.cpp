// C++ authorization struct with zero-initialized privilege field and strict role check.
#include <iostream>
#include <string>

struct SessionState {
    bool elevated = false;
};

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    std::string role(argv[1]);
    SessionState state{};
    if (role == "user") {
        state.elevated = false;
    } else if (role == "admin") {
        state.elevated = true;
    } else {
        std::cout << "DENIED";
        return 0;
    }
    std::cout << (state.elevated ? "ADMIN" : "USER");
    return 0;
}
