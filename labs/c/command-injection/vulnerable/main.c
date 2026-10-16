#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
int main(int argc, char **argv) {
if(argc != 2) return 2;
size_t n=strlen(argv[1])+12; char *cmd=malloc(n); if(!cmd) return 1; snprintf(cmd,n,"printf %%s %s",argv[1]); int rc=system(cmd); free(cmd); if(rc) return 1;
return 0;
}
