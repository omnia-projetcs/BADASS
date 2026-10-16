#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
int main(int argc, char **argv) {
if(argc != 2) return 2;
execl("/usr/bin/printf", "printf", "%s", argv[1], (char *)NULL); return 1;
return 0;
}
