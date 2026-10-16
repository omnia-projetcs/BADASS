#include <iostream>
#include <fstream>
#include <string>
#include <cstdlib>
#include <unistd.h>
int main(int argc, char **argv){ if(argc!=2) return 2; std::string value=argv[1];
if(value!="welcome.txt") {std::cout << "DENIED"; return 0;} std::ifstream file("public/welcome.txt"); if(!file) return 1; std::cout << file.rdbuf();
}
