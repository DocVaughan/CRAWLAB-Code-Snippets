#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#include "input_shaping.h"
#include "input_shaping.c"

#define PI acos(-1.0)
#define HZ_TO_RADS (2.0 * PI)

int main(int argc, char *argv[]) {
	
	float command[200];
	float shaped_command[200];
	
	
	input_shaper ZV_shaper = createZVShaper(1.00, 0.0, 100);
		
		
	for (int ii = 0; ii < 200; ii++)
	{
		// Define the "unshaped" input
		command[ii] = 100;
		
		// Create pointers to the two shaper structs
		input_shaper *ZV_shaper_p = &ZV_shaper;
		
		// Call the input shaping function
		shaped_command[ii] = doInputShaping(command[ii], ZV_shaper_p);
		
		// output the current unshaped input and shaped input, for comparison
		printf("sample: %d \t\t x = %.2f \t shaped = %.2f\n", ii, command[ii], shaped_command[ii]);
	}

	
}