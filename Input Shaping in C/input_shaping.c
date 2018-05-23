/* ----------------------------------------------------------------------------

input_shaping.c

Contains all necessary functions for implemetnation of ZV, ZVD, and EI shapers

Created: 02/08/16
   - Joshua Vaughan
   - joshua.vaughan@louisiana.edu
   - http://www.ucs.louisiana.edu/~jev9637

 Modified:
   *

---------------------------------------------------------------------------- */

#include <stdio.h>
#include <math.h>
#include "input_shaping.h"

#define PI acos(-1.0)
#define HZ_TO_RADS (2.0 * PI)

/*----- Shaper Creation -----------------------------------------------------*/
input_shaper createZVShaper(float nat_freq, float damping, int sample_rate)
{
    // Function to create a struct of type input_shaper representing a ZV shaper
    // 
    // Arguments:
    //   float freq : frequency (Hz) to desing the shaper for
    //   float damping : damping ratio to design the shaper for
    //   int sample_rate : sample/loop update rate of controller (Hz)
    //
    // Returns:
    //   input_shaper : a struct representing the ZV shaper
    // 
    
    input_shaper ZV_shaper = {2,                // Number of impulses
                              sample_rate       // 100Hz
                              };

    float wn = nat_freq * HZ_TO_RADS;
    float K = exp(-damping * PI / sqrt(1 - damping*damping));
        
    //Set up the impulse time spacing
    float shaperdeltaT = PI / (wn * sqrt(1 - damping*damping));
    
    // Assign the impulse amplitudes
    ZV_shaper.AMPS = malloc(ZV_shaper.NUM_IMPULSES * sizeof(float));
    ZV_shaper.AMPS[0] = 1 / (1 + K);
    ZV_shaper.AMPS[1] = K / (1 + K);
    
    // Assign the impulse times
    ZV_shaper.TIMES = malloc(ZV_shaper.NUM_IMPULSES * sizeof(float));
    ZV_shaper.TIMES[0] = 0.0;
    ZV_shaper.TIMES[1] = shaperdeltaT;
    
    // Create the markers for each impulse's current location in the buffer
    ZV_shaper.impulse_buffer_pos = malloc(ZV_shaper.NUM_IMPULSES * sizeof(int));
    for (int ii = 0; ii < ZV_shaper.NUM_IMPULSES; ii++)
        {
            ZV_shaper.impulse_buffer_pos[ii] = (int) (ZV_shaper.TIMES[ii] * sample_rate) - 1; 
        }
    
    // make the buffer length twice the length of the shaper (in number of samples)
    ZV_shaper.BUFFER_LENGTH = ceil(2 * ZV_shaper.TIMES[1] * sample_rate);
    
    // Create the buffer to store the shaped input
    ZV_shaper.shaped_output_buffer = malloc(ZV_shaper.BUFFER_LENGTH * sizeof(float));
    
    return ZV_shaper;
}

input_shaper createZVDShaper(float nat_freq, float damping, int sample_rate)
{
    // Function to create a struct of type input_shaper representing a ZVD shaper
    // 
    // Arguments:
    //   float freq : frequency (Hz) to desing the shaper for
    //   float damping : damping ratio to design the shaper for
    //   int sample_rate : sample/loop update rate of controller (Hz)
    //
    // Returns:
    //   input_shaper : a struct representing the ZVD shaper
    // 
    
    input_shaper ZVD_shaper = {3,               // Number of impulses
                              sample_rate       // 100Hz
                              };

    float wn = nat_freq * HZ_TO_RADS;
    float K = exp(-damping * PI / sqrt(1 - damping*damping));
        
    //Set up the impulse time spacing
    float shaperdeltaT = PI / (wn * sqrt(1 - damping*damping));
    
    // Assign the impulse amplitudes
    ZVD_shaper.AMPS = malloc(ZVD_shaper.NUM_IMPULSES * sizeof(float));
    ZVD_shaper.AMPS[0] = 1 / (1 + 2 * K + K * K);
    ZVD_shaper.AMPS[1] = (2 * K) / (1 + 2 * K + K * K);
    ZVD_shaper.AMPS[2] = (K * K) / (1 + 2 * K + K * K);
    
    // Assign the impulse times
    ZVD_shaper.TIMES = malloc(ZVD_shaper.NUM_IMPULSES * sizeof(float));
    ZVD_shaper.TIMES[0] = 0.0;
    ZVD_shaper.TIMES[1] = shaperdeltaT;
    ZVD_shaper.TIMES[2] = 2 * shaperdeltaT;
    
    // Create the markers for each impulse's current location in the buffer
    ZVD_shaper.impulse_buffer_pos = malloc(ZVD_shaper.NUM_IMPULSES * sizeof(int));
    for (int ii = 0; ii < ZVD_shaper.NUM_IMPULSES; ii++)
        {
            ZVD_shaper.impulse_buffer_pos[ii] = (int) (ZVD_shaper.TIMES[ii] * sample_rate - 1); 
        }
    
    // make the buffer length twice the length of the shaper (in number of samples)
    ZVD_shaper.BUFFER_LENGTH = ceil(2 * ZVD_shaper.TIMES[2] * sample_rate);
    
    // Create the buffer to store the shaped input
    ZVD_shaper.shaped_output_buffer = malloc(ZVD_shaper.BUFFER_LENGTH * sizeof(float));
    
    return ZVD_shaper;
}


input_shaper createEIShaper(float nat_freq, float damping, float vib_tol, int sample_rate)
{
    // Function to create a struct of type input_shaper representing a EI shaper
    // 
    // Arguments:
    //   float freq : frequency (Hz) to desing the shaper for
    //   float damping : damping ratio to design the shaper for
    //   float vib_tol : tolerable percentage vibration 0.05 = 5%
    //   int sample_rate : sample/loop update rate of controller (Hz)
    //
    // Returns:
    //   input_shaper : a struct representing the EI shaper
    // 
    
    input_shaper EI_shaper = {3,                // Number of impulses
                              sample_rate       
                              };

    float wn = nat_freq * HZ_TO_RADS;
    float wd =  wn * sqrt(1 - damping*damping);
        
    //Set up the impulse time spacing
    float shaperdeltaT = PI / (wn * sqrt(1 - damping*damping));
    
    // Assign the impulse amplitudes
    EI_shaper.AMPS = malloc(EI_shaper.NUM_IMPULSES * sizeof(float));
        
    // Define the shaper impulse amplitudes - based on curve fits
    EI_shaper.AMPS[0] = 0.249684 + 0.249623 * vib_tol + 0.800081 * damping + 1.23328 * vib_tol * damping + 0.495987 * damping * damping + 3.17316 * vib_tol * damping * damping;
    EI_shaper.AMPS[2] = 0.251489 + 0.21474 * vib_tol - 0.832493 * damping + 1.41498 * vib_tol * damping + 0.851806 * damping * damping - 4.90094 * vib_tol * damping * damping;
       
    // Now add the 2nd impulse, since it depends on 1 and 3
    EI_shaper.AMPS[1] = 1.0 - (EI_shaper.AMPS[0] + EI_shaper.AMPS[2]);
        
    // Assign the impulse times
    EI_shaper.TIMES = malloc(EI_shaper.NUM_IMPULSES * sizeof(float));
    EI_shaper.TIMES[0] = 0.0;
    EI_shaper.TIMES[1] = 2.0 * PI * (0.499899 + 0.461586 * vib_tol * damping + 4.26169 * vib_tol * damping * damping + 1.75601 * vib_tol * damping*damping*damping + 8.57843 * vib_tol*vib_tol * damping - 108.644 * vib_tol * vib_tol * damping * damping + 336.989 * vib_tol * vib_tol * damping*damping*damping) / wd;
    EI_shaper.TIMES[2] = 2.0 * PI / wd;
    
    // Create the markers for each impulse's current location in the buffer
    EI_shaper.impulse_buffer_pos = malloc(EI_shaper.NUM_IMPULSES * sizeof(int));
    for (int ii = 0; ii < EI_shaper.NUM_IMPULSES; ii++)
        {
            EI_shaper.impulse_buffer_pos[ii] = ceil(EI_shaper.TIMES[ii] * sample_rate - 1); 
        }
    
    // make the buffer length twice the length of the shaper (in number of samples)
    EI_shaper.BUFFER_LENGTH = ceil(2 * EI_shaper.TIMES[2] * sample_rate);
    
    // Create the buffer to store the shaped input
    EI_shaper.shaped_output_buffer = malloc(EI_shaper.BUFFER_LENGTH * sizeof(float));
    
    return EI_shaper;
}


/*----- Shaper Implementation -----------------------------------------------*/

float doInputShaping(float unshapedCommand, input_shaper *shaper)
{
    /* ------------------------------------------------------------------------
    Function that does input shaping for a single axis
    The shaper is hard-coded into the function for now, will probably be 
    better to pass it as a parameter later (func will be more reusable). 
    The function takes in an unshaped command reference command for the 
    current timestep and returns the shaped command for the current 
    timestep, while propagating the later impulses into a buffer for future
    output. 
    
    Arguments:
        * float unshaped_command : the unshaped command command at 
                                    current timeste
        * three_impulse_shaper *shaper : pointer to struct holding all the
                                       key shaper parameters
    
    Returns:
        * float shaped_command : the input shaped command at 
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
        
        shaper->shaped_output_buffer[shaper->impulse_buffer_pos[ii]] += shaper->AMPS[ii] * unshapedCommand;
    }
    
    // set up the current output
    float current_shaped_output = shaper->shaped_output_buffer[shaper->impulse_buffer_pos[0]];
    
    // clear the current position in the buffer, because it's been used
    shaper->shaped_output_buffer[shaper->impulse_buffer_pos[0]] = 0;
    
    return current_shaped_output;
}
