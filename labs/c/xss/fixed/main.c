#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
int main(int argc, char **argv) {
if(argc != 2) return 2;
fputs("<p>", stdout); for(const char *p=argv[1]; *p; ++p) { switch(*p) { case '&': fputs("&amp;",stdout); break; case '<': fputs("&lt;",stdout); break; case '>': fputs("&gt;",stdout); break; default: putchar(*p); }} fputs("</p>",stdout);
return 0;
}
