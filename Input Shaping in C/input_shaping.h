/* ----------------------------------------------------------------------------

input_shaping.h

Header file for implementation of ZV, ZVD, and EI shapers

Created: 02/08/16
   - Joshua Vaughan
   - joshua.vaughan@louisiana.edu
   - http://www.ucs.louisiana.edu/~jev9637

 Modified:
   *

---------------------------------------------------------------------------- */

typedef struct { 
    int const NUM_IMPULSES;           // the number of shaper impulses
    int SAMPLE_RATE;			        // sampling/loop update rate (Hz)
    int BUFFER_LENGTH;                // length of buffer to hold shaped values
    float *AMPS;                    // shaper impulse amplitudes
    float *TIMES;                   // shaper impulse times (s)
    int *impulse_buffer_pos;        // index of buffer position for each imp.
    float *shaped_output_buffer;  // ring buffer to hold output of shaper, length should equal BUFFER_LENGTH
}  input_shaper;


float doInputShaping(float unshapedCommand, input_shaper *shaper);
input_shaper createZVShaper(float freq, float damping, int sample_rate);
