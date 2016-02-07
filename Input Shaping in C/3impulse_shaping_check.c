#include <stdio.h>

float doZVDShaping(float unshapedVelocity)
{
    /* ------------------------------------------------------------------------
    Function that does input shaping for a single axis
    The shaper is hard-coded into the function for now, will probably be 
    better to pass it as a parameter later (func will be more reusable). 
    The function takes in an unshaped velocity reference command for the 
    current timestep and returns the shaped velocity for the current 
    timestep, while propagating the later impulses into a buffer for future
    output. 
    
    Arguments:
        * float unshaped_velocity : the unshaped velocity command at 
                                    current timestep
    
    Returns:
        * float shaped_velocity : the input shaped velocity at 
                                  the current timestop
        * NOTE: Also saves the future input into a buffer from the curent input 
                dependent on shaper parameters
    
    Created: 02/07/16 - Joshua Vaughan - joshua.vaughan@louisiana.edu
    
    Modified:
        *
    -------------------------------------------------------------------------*/     
	
	// ZVD-shaper for undamped system
	float TAU = 0.5;                         // damped period (s)
	int NUM_IMPULSES = 3;                    // the number of shaper impulses
	float AMPS[3] = {0.25, 0.5, 0.25};       // shaper impulse amplitudes
	float TIMES[3] = {0.0, 0.5 * TAU, TAU};  // shaper impulse times (s)
	
	// buffer length should be 2x shaper duration (sec.) * samples/sec at min
	// could be just the shaper length, but have to be more elegant to execute
	#define BUFFER_LENGTH (151)
	
	// Define the buffer to fill with shaped values
	static float shaped_output_buffer[BUFFER_LENGTH];
	
	// Define the two buffer locations, the impulse1 location can also be 
	// thought of as the "current" output location, the impulse2 location
	// is offset by the time of the 2nd impulse (* samples/s)
	// Each of these locations gets updated each time the function is called
	static int impulse1_buffer_pos = -1; // The impulse1 buffer position
	static int impulse2_buffer_pos = 49; // The impulse2 buffer position
	static int impulse3_buffer_pos = 99; // The impulse3 buffer position
	
	// Increment the current positions in the buffer
	impulse1_buffer_pos++;
	impulse2_buffer_pos++;
	impulse3_buffer_pos++;
	
	// For the first impulse, check that there is enough room in the buffer
    // If not, wrap to the beginning and overwrite
    if (impulse1_buffer_pos > BUFFER_LENGTH) 
    {
		//printf("\n Wrapping 1st impulse \n");
        impulse1_buffer_pos = 0;
    }
	
    // First impulse happens immediately, add it to the current buffer location
    shaped_output_buffer[impulse1_buffer_pos] += AMPS[0] * unshapedVelocity;	
    
    
    // For the second impulse, check that there is enough room in the buffer
    // If not, wrap to the beginning and overwrite
    if (impulse2_buffer_pos > BUFFER_LENGTH) 
    {
		// printf("\n Wrapping 2nd impulse \n");
        impulse2_buffer_pos = 0;
    }
    
    // Add  the second impulse portion to the correct buffer location
    shaped_output_buffer[impulse2_buffer_pos] += AMPS[1] * unshapedVelocity;
    
    
    // For the third impulse, check that there is enough room in the buffer
    // If not, wrap to the beginning and overwrite
    if (impulse3_buffer_pos > BUFFER_LENGTH) 
    {
		// printf("\n Wrapping 2nd impulse \n");
        impulse3_buffer_pos = 0;
    }
    
    // Add the third impulse portion to the correct buffer location
    shaped_output_buffer[impulse3_buffer_pos] += AMPS[2] * unshapedVelocity;
    
    // set up the current output
    float current_shaped_output = shaped_output_buffer[impulse1_buffer_pos];
    
    // clear the current position in the buffer, because it's been used
    shaped_output_buffer[impulse1_buffer_pos] = 0;
    
    return current_shaped_output;
}


int main(int argc, char *argv[]) {
	float x[200];
	float shaped_x[200];

	for (int ii = 0; ii < 200; ii++)
	{
		// Define the "unshaped" input
		x[ii] = 100;
		
		// Call the input shaping function
		shaped_x[ii] = doZVDShaping(x[ii]);
		
		// output the current unshaped input and shaped input, for comparison
		printf("x = %.2f \t\t shaped = %.2f\n", x[ii], shaped_x[ii]);
	}
}