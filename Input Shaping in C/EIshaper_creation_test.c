#include <stdio.h>
#include <stdlib.h>
#include <math.h>

//#include "input_shaping.h"
#include "input_shaping.c"

#define PI acos(-1.0)
#define HZ_TO_RADS (2.0 * PI)

int main(int argc, char *argv[]) {
	
	float command[200];
	float shaped_command[200];
	
	
	input_shaper EI_shaper = createEIShaper(1.00, 0.0, 0.05, 50);
		
	for (int ii = 0; ii < 200; ii++)
	{
		// Define the "unshaped" input
		command[ii] = 100;
		
		// Create pointers to the two shaper structs
		input_shaper *EI_shaper_p = &EI_shaper;
		
		// Call the input shaping function
		shaped_command[ii] = doInputShaping(command[ii], EI_shaper_p);
		
		// output the current unshaped input and shaped input, for comparison
		printf("sample: %d \t\t x = %.2f \t shaped = %.2f\n", ii, command[ii], shaped_command[ii]);
		printf("A1_pos = %d \t A2_pos = %d \t A3_pos = %d\n\n", EI_shaper.impulse_buffer_pos[0], 				EI_shaper.impulse_buffer_pos[1], EI_shaper.impulse_buffer_pos[2]);
	}
	printf("A1 = %f \t A2 = %f \t A3 = %f\n", EI_shaper.AMPS[0], EI_shaper.AMPS[1], EI_shaper.AMPS[2]);
	printf("T1 = %f \t T2 = %f \t T2 = %f\n", EI_shaper.TIMES[0], EI_shaper.TIMES[1], EI_shaper.TIMES[2]);
}