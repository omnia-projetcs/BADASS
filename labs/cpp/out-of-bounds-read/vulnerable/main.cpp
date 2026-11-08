#include <iostream>
#include <fstream>
#include <string>
#include <cstdlib>
#include <unistd.h>
int main(int argc, char **argv){ if(argc!=2) return 2; std::string value=argv[1];
int values[3]={10,20,30}; std::cout << values[std::stoi(value)];
}
