#include <iostream>
#include <fstream>
#include <string>
#include <cstdlib>
#include <unistd.h>
int main(int argc, char **argv){ if(argc!=2) return 2; std::string value=argv[1];
int values[3]={10,20,30}; int index=std::stoi(value); if(index<0 || index>=3) {std::cout << "DENIED"; return 0;} std::cout << values[index];
}
