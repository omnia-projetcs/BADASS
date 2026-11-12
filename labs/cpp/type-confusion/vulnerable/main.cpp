// C++ tagged record interpreting a guest ID as an administrative capability flag.
#include <cstdlib>
#include <iostream>
#include <string>

struct AccountRecord {
    int kind; // 0 = standard, 1 = service
    union {
        int user_number;
        int service_privilege;
    } payload;
};

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    AccountRecord rec{};
    rec.kind = 0;
    rec.payload.user_number = std::atoi(argv[1]);
    if (rec.payload.service_privilege == 1337) {
        std::cout << "ADMIN";
    } else {
        std::cout << "GUEST:" << rec.payload.user_number;
    }
    return 0;
}
