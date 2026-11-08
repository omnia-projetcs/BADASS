#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
int main(int argc, char **argv) {
if(argc != 2) return 2;
if(strcmp(argv[1],"welcome.txt")) {fputs("DENIED",stdout); return 0;} FILE *f=fopen("public/welcome.txt","r"); if(!f) return 1; int ch; while((ch=fgetc(f))!=EOF) putchar(ch); fclose(f);
return 0;
}
