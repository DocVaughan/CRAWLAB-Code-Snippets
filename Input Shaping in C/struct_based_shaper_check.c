#include <stdio.h>

typedef struct { 
    int const NUM_IMPULSES;           // the number of shaper impulses
    int SAMPLE_RATE;			        // sampling/loop update rate (Hz)
    int BUFFER_LENGTH;                // length of buffer to hold shaped values
    float AMPS[3];                    // shaper impulse amplitudes
    float TIMES[3];                   // shaper impulse times (s)
    int impulse_buffer_pos[3];        // index of buffer position for each imp.
    float shaped_output_buffer[150];  // ring buffer to hold output of shaper, length should equal BUFFER_LENGTH
}  three_impulse_shaper;



float doInputShaping(float unshapedVelocity, three_impulse_shaper *shaper)
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
                                    current timeste
	    * three_impulse_shaper *shaper : pointer to struct holding all the
									   key shaper parameters
    
    Returns:
        * float shaped_velocity : the input shaped velocity at 
                                  the current timestop
        * NOTE: Also saves the future input into a buffer from the curent input 
                dependent on shaper parameters
    
    Created: 02/08/16 - Joshua Vaughan - joshua.vaughan@louisiana.edu
    
    Modified:
		* 
    -------------------------------------------------------------------------*/     
	
	// During first time the function is called, initialize the buffer positions
	if (shaper->impulse_buffer_pos[0] == -1 ) 
	{
        // Define the starting buffer locations, the impulse_buffer_pos[0] location  
        // can also be thought of as the "current" output, the impulse_buffer_pos[1] 
        // location is offset by the time of the 2nd impulse (* samples/s), etc
        // Each of these locations gets updated each time the function is called
        for (int ii = 0; ii < shaper->NUM_IMPULSES; ii++)
        {
            shaper->impulse_buffer_pos[ii] = (int) (shaper->TIMES[ii] * shaper->SAMPLE_RATE) - 1; 
        }
    }
    

	// Increment the current positions in the buffers
	for (int ii = 0; ii < shaper->NUM_IMPULSES; ii++)
	{
	    shaper->impulse_buffer_pos[ii]++;
	}
	
	// For each impulse, multiple the current input by the impulse amplitude 
	// and add it to the place in the buffer corresponding to the time offset
	// of the impulse. If the desired buffer position (from the time offset)
	// is outside of the buffer, wrap to the beginning. 
	for (int ii = 0; ii < shaper->NUM_IMPULSES; ii++)
	{
	    // wrap the buffer location, if necessary
	    if (shaper->impulse_buffer_pos[ii] > shaper->BUFFER_LENGTH) 
	    {
	        shaper->impulse_buffer_pos[ii] = 0;
	    }
	    
	    shaper->shaped_output_buffer[shaper->impulse_buffer_pos[ii]] += shaper->AMPS[ii] * unshapedVelocity;
	}
	
    // set up the current output
    float current_shaped_output = shaper->shaped_output_buffer[shaper->impulse_buffer_pos[0]];
    
    // clear the current position in the buffer, because it's been used
    shaper->shaped_output_buffer[shaper->impulse_buffer_pos[0]] = 0;
    
    return current_shaped_output;
}


int main(int argc, char *argv[]) {
	float x[200];
	float shaped_x[200];
	float shaped_y[200];
	
    three_impulse_shaper ZVD_shaper = {   3, 	            // Number of impulses
                                        50,		        // 100Hz
                                        150,               // buffer length
                                       {0.25, 0.5, 0.25},  // amplitudes
                                       {0, 0.5, 1.0},      // times
                                       {-1, 0, 0}          // Buffer positions
                                      };

    three_impulse_shaper EI_shaper = {   3, 	            // Number of impulses
                                       50,		            // 100Hz
                                    	 150,                // buffer length
                                       {0.26, 0.48, 0.26}, // amplitudes
                                       {0, 0.5, 1.0},      // times
                                       {-1, 0, 0}          // Buffer positions
                                      };
	

	for (int ii = 0; ii < 200; ii++)
	{
		// Define the "unshaped" input
		x[ii] = 100;
		
		// Create pointers to the two shaper structs
		three_impulse_shaper *ZVD_shaper_p = &ZVD_shaper;
		three_impulse_shaper *EI_shaper_p = &EI_shaper;
		
		// Call the input shaping function
		shaped_x[ii] = doInputShaping(x[ii], ZVD_shaper_p);
		shaped_y[ii] = doInputShaping(x[ii], EI_shaper_p);
		
		// output the current unshaped input and shaped input, for comparison
		printf("sample: %d \t\t x = %.2f \t shaped = %.2f\n", ii, x[ii], shaped_x[ii]);
		printf("sample: %d \t\t y = %.2f \t shaped = %.2f\n\n", ii, x[ii], shaped_y[ii]);
	}
}