/* 
 * A simple, non-optimizing brainfuck to C translator.
 * 2010-08-31 - Version 1.0   (Cory Burgett)
 *
 * This code is hereby placed into the public domain.
 *
 * Originally located at: http://www4.ncsu.edu/~cmburget/brainfucc.c
 */

#include <stdio.h>

int main(int argc, char **argv)
{
	FILE *in = stdin, *out = stdout;
	int c;
	int cellsize = 30000;

	fprintf(out,
		"#include <stdio.h>\n"
		"#include <stdlib.h>\n\n"
		"int main(int argc, char **argv)\n{\n"
		"\tunsigned char *cell = calloc(%d, 1);\n"
		"\tunsigned char *cells = cell;\n"
		"\tif (!cell) {\n"
		"\t\tfprintf(stderr, \"Error allocating memory.\\n\");\n"
		"\t\treturn 1;\n"
		"\t}\n\n", cellsize
	);

	while ((c = getc(in)) != EOF) {
		switch (c) {
			case '>': fprintf(out, "\t\t++cell;\n"); break;
			case '<': fprintf(out, "\t\t--cell;\n"); break;
			case '+': fprintf(out, "\t\t++*cell;\n"); break;
			case '-': fprintf(out, "\t\t--*cell;\n"); break;
			case '.': fprintf(out, "\t\tputchar(*cell);\n"); break;
			case ',': fprintf(out, "\t\t*cell = getchar();\n"); break;
			case '[': fprintf(out, "\twhile (*cell) {\n"); break;
			case ']': fprintf(out, "\t}\n"); break;
			default: break;
		}
	}
	
	fprintf(out, "\n\tfree(cells);\n\treturn 0;\n}\n\n");
}
