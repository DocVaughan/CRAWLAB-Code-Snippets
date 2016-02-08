#include <stdio.h>

//float * InputShape_Array(float unshapedVelocities[2], struct three_impulse_shaper, struct three_impulse_shaper);
//float doInputShaping(float unshapedVelocity, struct three_impulse_shaper);

typedef struct { 
    float TAU;                    // damped period (s)
    #define NUM_IMPULSES (3)      // the number of shaper impulses
	int SAMPLE_RATE;				// Sampling rate (Hz)
    float AMPS[3];                // shaper impulse amplitudes
    float TIMES[3];               // shaper impulse times (s)
    int impulse_buffer_pos[3];    // index of buffer position for each imp.
} three_impulse_shaper;


int main(int argc, char *argv[]) {
	
	three_impulse_shaper ZVD_shaper = { 0.5, 		       // design period 
									  100,              // Sampling rate 100Hz
		                               {0.25, 0.5, 0.25}, // amplitudes
		                               {0, 0.5, 1.0},     // times
		                               {0, 49, 99}        // Buffer positions
		                               };
	float x[200];
	float y[200];
	float shaped[200][2];

	for (int ii = 0; ii < 200; ii++)
	{
		// Define the "unshaped" input
		x[ii] = 100;
		y[ii] = 100;
		
		float current_unshaped[2] = {x[ii], y[ii]};
		
		// Call the input shaping function
		shaped[ii] = InputShape_Array(current_unshaped, ZVD_shaper, ZVD_shaper);
		
		// output the current unshaped input and shaped input, for comparison
		printf("x = %.2f \t\t shaped = %.2f\n", x[ii], shaped_x[ii]);
	}
	
}


float * InputShape_Array(float unshapedVelocities[2], struct three_impulse_shaper, struct three_impulse_shaper)
{
    /* ------------------------------------------------------------------------
    Function that does input shaping for a two axes, using the same shaper for
    each axis. The function calls doInputShaping() for each dimension of the
    input array.
    
    The shaper is hard-coded into the doInputShaping() function for now. It 
    will definitely be better to pass it as a parameter later, because the 
    function will be more reusable. 
    
    The function takes in an unshaped velocity reference commands for the 
    current timestep and returns the shaped velocities for the current 
    timestep. 
    
    Arguments:
        * float unshaped_velocities : two axes of unshaped velocity command at 
                                      current timestep
    
    Returns:
        * float shaped_velocities : the input shaped velocities at 
                                    the current timestop
    
    Created: 02/08/16 - Joshua Vaughan - joshua.vaughan@louisiana.edu
    -------------------------------------------------------------------------*/

	printf("%f", three_impulse_shaper.TAU);
}

    

float doInputShaping(float unshapedVelocity, three_impulse_shaper)
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
        * updated the commenting
        * More robust definition of shaper parameters
    -------------------------------------------------------------------------*/     
	
	// Define the input shaper parameters
	
	// Define the sampling rate in Hz
	#define DT (10)
	
	// Buffer length should be ~2x shaper duration in (sec.) * samples/sec
	// Could be just the shaper length, but have to be more elegant to execute
	int BUFFER_LENGTH = 2 * (three_impulse_shaper.TIMES[2] * DT)
		
	// Define the buffer to fill with shaped values
	static float shaped_output_buffer[BUFFER_LENGTH];
	
    // Define a variable to hold the current position in the buffer 
    // corresponding to each impulses's time offset.
	static int impulse_buffer_pos[NUM_IMPULSES] = {-1};
	
	// During first time the function is called, initialize the buffer positions
	if (impulse_buffer_pos[0] == -1 ) 
	{
        // Define the starting buffer locations, the impulse_buffer_pos[0] location  
        // can also be thought of as the "current" output, the impulse_buffer_pos[1] 
        // location is offset by the time of the 2nd impulse (* samples/s), etc
        // Each of these locations gets updated each time the function is called
        for (int ii = 0; ii < NUM_IMPULSES; ii++)
        {
            impulse_buffer_pos[ii] = (int) TIMES[ii] * DT - 1; 
        }
    }
    

	// Increment the current positions in the buffers
	for (int ii = 0; ii < NUM_IMPULSES; ii++)
	{
	    impulse_buffer_pos[ii]++;
	}
	
	// For each impulse, multiple the current input by the impulse amplitude 
	// and add it to the place in the buffer corresponding to the time offset
	// of the impulse. If the desired buffer position (from the time offset)
	// is outside of the buffer, wrap to the beginning. 
	for (int ii = 0; ii < NUM_IMPULSES; ii++)
	{
	    // wrap the buffer location, if necessary
	    if (impulse_buffer_pos[ii] > BUFFER_LENGTH) 
	    {
	        impulse_buffer_pos[ii] = 0;
	    }
	    
	    shaped_output_buffer[impulse_buffer_pos[ii]] += AMPS[ii] * unshapedVelocity;
	}
	
    // set up the current output
    float current_shaped_output = shaped_output_buffer[impulse_buffer_pos[0]];
    
    // clear the current position in the buffer, because it's been used
    shaped_output_buffer[impulse_buffer_pos[0]] = 0;
    
    return current_shaped_output;
}