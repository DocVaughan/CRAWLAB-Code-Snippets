float doInputShaping(float unshapedVelocity)
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
	#define NUM_IMPULSES (3)                 // the number of shaper impulses
	float AMPS[3] = {0.25, 0.5, 0.25};       // shaper impulse amplitudes
	float TIMES[3] = {0.0, 0.5 * TAU, TAU};  // shaper impulse times (s)
	
	// Define the sampling rate in Hz
	#define DT (10)
	
	// buffer length should be 2x shaper duration (sec.) * samples/sec at min
	// could be just the shaper length, but have to be more elegant to execute
	#define BUFFER_LENGTH (151)
	
	// Define the buffer to fill with shaped values
	static float shaped_output_buffer[BUFFER_LENGTH];
	
	static int impulse_buffer_pos[NUM_IMPULSES] = {-1}
	
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
	
	for (int ii = 0; ii < NUM_IMPULSES; ii++)
	{
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