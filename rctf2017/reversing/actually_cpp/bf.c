#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv)
{
	unsigned char *cell = calloc(30000, 1);
	unsigned char *cells = cell;
	if (!cell) {
		fprintf(stderr, "Error allocating memory.\n");
		return 1;
	}

		cell += 5;
		*cell += 5;
		// cell[5] = 5;
		cell -= 4;
		*cell -= 5;
		// cell[1] -= 5;
		cell += 3;
		*cell += 2;
		// cell[4] += 2;
		cell -= 9;
		*cell -= 5;
		// cell[-5] -= 5; // ?

	free(cells);
	return 0;
}

