#include <iostream>
#include <fstream>
#include <string>
#include <cstdlib>
#include <unistd.h>
int main(int argc, char **argv){ if(argc!=2) return 2; std::string value=argv[1];
std::cout << "<p>"; for(char c:value) { switch(c) {case '&': std::cout << "&amp;"; break; case '<': std::cout << "&lt;"; break; case '>': std::cout << "&gt;"; break; default: std::cout << c; }} std::cout << "</p>";
}
