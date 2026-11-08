#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
int main(int argc, char **argv) {
if(argc != 2) return 2;
char buffer[8]; strcpy(buffer,argv[1]); puts(buffer);
return 0;
}
