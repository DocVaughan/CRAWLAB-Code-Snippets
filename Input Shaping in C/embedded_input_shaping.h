/* ----------------------------------------------------------------------------

embedded_input_shaping.h

Header file for implementation of ZV, ZVD, and EI shapers on embedded systems
Differs from non-embedded based on memory limitations, etc

Created: 02/09/16
   - Joshua Vaughan
   - joshua.vaughan@louisiana.edu
   - http://www.ucs.louisiana.edu/~jev9637

 Modified:
   *

---------------------------------------------------------------------------- */

// NOTE: This *HAS* to be at least (shaper_duration * sample_rate + 1)
// Update accordingly
#define SHAPER_BUFFER_LENGTH (601)

typedef struct { 
    int const NUM_IMPULSES;         // the number of shaper impulses
    int SAMPLE_RATE;			    // sampling/loop update rate (Hz)
    int BUFFER_LENGTH;              // length of buffer to hold shaped values
    float AMPS[3];                  // shaper impulse amplitudes
    float TIMES[3];                 // shaper impulse times (s)
    int impulse_buffer_pos[3];      // index of buffer position for each imp.
    // finally, the buffer to keep track of the shaped input
    float shaped_output_buffer[SHAPER_BUFFER_LENGTH]; 
}  input_shaper;


// Functions to create input shapers to fill the struct type defined above
input_shaper createZVShaper(float nat_freq, float damping, int sample_rate);
input_shaper createZVDShaper(float nat_freq, float damping, int sample_rate);
input_shaper createEIShaper(float nat_freq, float damping, float vib_tol, int sample_rate);


// Functions to implement the shaping
float doInputShaping(float unshapedCommand, input_shaper *shaper);