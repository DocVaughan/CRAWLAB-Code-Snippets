#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#include "embedded_input_shaping.c"

#define PI acos(-1.0)
#define HZ_TO_RADS (2.0 * PI)
//#define SHAPER_BUFFER_LENGTH (601)

int main(int argc, char *argv[]) {
	
	float command[200];
	float shaped_command[200];
	
	

	//input_shaper current_shaper = createZVShaper(1.00, 0.0, 100);
	//input_shaper current_shaper = createZVDShaper(0.33, 0.0, 100);
	input_shaper current_shaper = createEIShaper(0.5, 0.0, 0.05, 100);
				
	for (int ii = 0; ii < 200; ii++)
	{
		// Define the "unshaped" input
		command[ii] = 100;
		
		// Call the input shaping function
		shaped_command[ii] = doInputShaping(command[ii], &current_shaper);
		
		// output the current unshaped input and shaped input, for comparison
		printf("sample: %d \t\t x = %.2f \t shaped = %.2f\n", ii, command[ii], shaped_command[ii]);
		printf("A1_pos = %d \t A2_pos = %d\n\n", current_shaper.impulse_buffer_pos[0], current_shaper.impulse_buffer_pos[1]);
	}
	
	printf("\n\nThe shaper parameters were:\n");
	printf("A1 = %f \t A2 = %f \t A3 = %f\n",  current_shaper.AMPS[0],
											 current_shaper.AMPS[1], 
											 current_shaper.AMPS[2]);
											
	printf("T1 = %f \t T2 = %f \t T3 = %f\n", current_shaper.TIMES[0],
										    current_shaper.TIMES[1],
										    current_shaper.TIMES[2]);
		
}