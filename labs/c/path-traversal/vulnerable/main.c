#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
int main(int argc, char **argv) {
if(argc != 2) return 2;
size_t n=strlen(argv[1])+8; char *path=malloc(n); if(!path) return 1; snprintf(path,n,"public/%s",argv[1]); FILE *f=fopen(path,"r"); free(path); if(!f) return 1; int ch; while((ch=fgetc(f))!=EOF) putchar(ch); fclose(f);
return 0;
}
