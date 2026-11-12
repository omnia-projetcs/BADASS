// C++ tagged record verifying the discriminant kind and input bounds before access.
#include <cerrno>
#include <cstdlib>
#include <iostream>
#include <string>

struct AccountRecord {
    int kind;
    union {
        int user_number;
        int service_privilege;
    } payload;
};

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    char *end = nullptr;
    errno = 0;
    long parsed = std::strtol(argv[1], &end, 10);
    if (errno || end == argv[1] || *end || parsed < 1 || parsed > 1000) {
        std::cout << "DENIED";
        return 0;
    }
    AccountRecord rec{};
    rec.kind = 0;
    rec.payload.user_number = static_cast<int>(parsed);
    if (rec.kind == 1 && rec.payload.service_privilege == 1337) {
        std::cout << "ADMIN";
    } else {
        std::cout << "GUEST:" << rec.payload.user_number;
    }
    return 0;
}
