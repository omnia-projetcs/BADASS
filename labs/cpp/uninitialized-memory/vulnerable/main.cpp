// C++ authorization struct with uninitialized privilege field on malformed input.
#include <iostream>
#include <string>

struct SessionState {
    bool elevated;
};

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    std::string role(argv[1]);
    SessionState state;
    if (role == "user") {
        state.elevated = false;
    } else if (role == "admin") {
        state.elevated = true;
    } else {
        state.elevated = true;
    }
    std::cout << (state.elevated ? "ADMIN" : "USER");
    return 0;
}
