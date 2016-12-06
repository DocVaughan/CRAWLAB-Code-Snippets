#! /usr/bin/env python

###############################################################################
# audio_generator_multiFreq.py
#
# Script to generate audio files/arrays. Can generate multiple frequencies
#
# This script is modified from:
#  http://stackoverflow.com/questions/9770073/sound-generation-synthesis-with-python
# 
# It utilizes pyaudio, which was installed via conda from
# https://anaconda.org/magonser/pyaudio using:
#
#   conda install -c magonser pyaudio=0.2.9 
#
# You may also need to install portaudio, for which pyaudio is a wrapper
#
#   OS X          - brew install portaudio
#   Debian/Ubuntu - sudo apt-get install python-pyaudio python3-pyaudio
#
# Writing to a wave file was modified from the example at the pyaudio docs:
#    http://people.csail.mit.edu/hubert/pyaudio/#sources
#
# NOTE: Any plotting is set up for output, not viewing on screen.
#       So, it will likely be ugly on screen. The saved PDFs should look
#       better.
#
# Created: 12/06/16
#   - Joshua Vaughan
#   - joshua.vaughan@louisiana.edu
#   - http://www.ucs.louisiana.edu/~jev9637
#
# Modified:
#   * 
#
# TODO:
#   * 
###############################################################################

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import numpy as np
import matplotlib.pyplot as plt

import pyaudio
import wave

# Operational flags
PLAY_SOUND = False      # set True to play any sounds generated
WRITE_WAV = True        # set True to save the sound to a wav file named by
PLOT_WAVE = False       # set True to plot the sound wave
CHECK_FFT = False       # set True to check the output via FFT

# Define the desired output filename
WAV_OUTPUT_FILENAME = 'multi_freq_test.wav'

# Set up the audio specifications
BITRATE = 44100         # number of frames per second/frameset
NUM_CHANNELS = 1        # number of channels (usually 1 or 2 = mono or stereo)
DURATION = 10           # seconds to play sound

def CRAWLAB_fft(data,time,plotflag):
    ''' CRAWLAB_fft.py
    Function to get the FFT for a response
    #
    # Usage: 
    # fft_freq, fft_mag = CRAWLAB_fft(data,time,plotflag)
    #
    # Inputs:
    #   time = time array corresponding to the data
    #   data = the response data array (only pass a single dimension/state at at time)
    #   plotflag = will plot the FFT if nonzero
    #   
    # Output:
    #   fft_freq = an array of the freqs used in the FFT
    #   fft_mag = an array of the amplitude of the FFT at each freq in fft_freq
    #
    # Created: 03/28/14
    #   - Joshua Vaughan
    #   - joshua.vaughan@louisiana.edu
    #   - http://www.ucs.louisiana.edu/~jev9637
    ######################################################################################
    '''
    from scipy.fftpack import fft
    
    # correct for any DC offset
    offset = np.mean(data) 

    # Get the natural frequency
    sample_time = time[1] - time[0]
    n = len(data)

    fft_mag = fft((data - offset)*np.hanning(len(data)))
    fft_freq = np.linspace(0.0, 1.0/(2.0*sample_time), n/2)
    
    # Only return the "useful" part of the fft
    fft_mag = 2.0/n * np.abs(fft_mag[0:n/2])
    
    if plotflag:
        # Plot the relationshiop
        #   Many of these setting could also be made default by the .matplotlibrc file
        fig = plt.figure(figsize=(6,4))
        ax = plt.gca()
        plt.subplots_adjust(bottom=0.17,left=0.17,top=0.96,right=0.96)
        plt.setp(ax.get_ymajorticklabels(),fontsize=18)
        plt.setp(ax.get_xmajorticklabels(),fontsize=18)
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.set_ticks_position('left')
        ax.grid(True,linestyle=':',color='0.75')
        ax.set_axisbelow(True)

        plt.xlabel('Frequency (Hz)',fontsize=22,labelpad=8)
        plt.ylabel('FFT magnitude',fontsize=22,labelpad=10)
    
        plt.plot(fft_freq, fft_mag, linewidth=2, linestyle='-')
        
        # Adjust the page layout filling the page using the new tight_layout command
        plt.tight_layout(pad=0.5)
        plt.show()
    
    # Uncomment below to find and print the frequency at which the highest peak occurs
#     freq_index = np.argmax(2.0/n * np.abs(fft_mag[0:n/2]))
#     print '\nHighest magnitude peak occurs at: ' + str(fft_freq[freq_index]) + ' Hz.'
    
    return fft_freq, fft_mag


# Create a PyAudio() instance
p = pyaudio.PyAudio()

# Define the necessary constants for the portaudio api
PORT_AUDIO_FORMAT = p.get_format_from_width(1)
SAMPLE_WIDTH = p.get_sample_size(PORT_AUDIO_FORMAT)

# the number of frames given how long we want to play at the given bitrate
NUMBER_OF_FRAMES = int(BITRATE * DURATION)   

# fill leftover frames to match the bitrate   
RESTFRAMES = NUMBER_OF_FRAMES % BITRATE

WAVEDATA = ''       # hold the byte representation of the wave  

# We'll also create an array so we can plot the wave
wave_for_plotting = np.zeros(((NUMBER_OF_FRAMES + RESTFRAMES), NUM_CHANNELS+1))

# Define the frequency and relative amplitudes of the desired wave(s)
# Frequencies for a middle C on a piano
# FREQ = np.array([261.63, 195.998, 293.665])    # Hz, 261.63=C4, 440=A4 notes on piano, etc
# AMP = np.array([0.75, 0.125, 0.125])           # The relative amplitude of the frequencies

# Frequencies for an E-chord on Guitar
FREQ = 3 * np.array([82.407, 123.5, 164.8, 207.6, 246.9, 329.628])    # Hz, 261.63=C4, 440=A4 notes on piano, etc
AMP = 1/6 * np.ones((1, 6))           # The relative amplitude of the frequencies

# Single A4 note
# FREQ = np.array([440])        # Hz, 261.63=C4, 440=A4 notes on piano, etc
# AMP = np.array([1])           # The relative amplitude of the frequencies



if np.max(FREQ) > BITRATE:
    BITRATE = np.max(FREQ) + 100

for sample in range(NUMBER_OF_FRAMES):
    # Get the amplitude of the current sample
    current_sample = np.sum(AMP * np.sin(sample / BITRATE * FREQ * 2 * np.pi))
    
    # Save the current time and sample amplitude to the plotting array
    wave_for_plotting[sample,:] = [sample/BITRATE, current_sample]
    
    # append it (as a byte) to the WAVEDATA
    WAVEDATA = WAVEDATA + chr(int(current_sample * 127 + 128))

for _ in range(RESTFRAMES): 
    WAVEDATA = WAVEDATA + chr(128)


if WRITE_WAV: # Write the wave file
    # open the file
    wf = wave.open(WAV_OUTPUT_FILENAME, 'wb')   
    
    # Set its properties
    wf.setnchannels(NUM_CHANNELS)
    wf.setsampwidth(SAMPLE_WIDTH)
    wf.setframerate(BITRATE)                    
    
    # Actually write to file
    wf.writeframes(WAVEDATA.encode('utf-8'))    
    
    # Now close the file
    wf.close()                                  


if PLAY_SOUND: # set up and play the sound through the speakers
    stream = p.open(format = PORT_AUDIO_FORMAT , 
                    channels = NUM_CHANNELS, 
                    rate = BITRATE, 
                    output = True)
    stream.write(WAVEDATA) # Actually play the sound
    
    # Now, stop the stream and close it
    stream.stop_stream()
    stream.close()

if PLOT_WAVE: # plot the generated wave vs time
    # Set the plot size - 3x2 aspect ratio is best
    fig = plt.figure(figsize=(6,4))
    ax = plt.gca()
    plt.subplots_adjust(bottom=0.17, left=0.17, top=0.96, right=0.96)

    # Change the axis units font
    plt.setp(ax.get_ymajorticklabels(),fontsize=18)
    plt.setp(ax.get_xmajorticklabels(),fontsize=18)

    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')

    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

    # Turn on the plot grid and set appropriate linestyle and color
    ax.grid(True,linestyle=':', color='0.75')
    ax.set_axisbelow(True)

    # Define the X and Y axis labels
    plt.xlabel('Time (s)', fontsize=22, weight='bold', labelpad=5)
    plt.ylabel('Amplitude', fontsize=22, weight='bold', labelpad=10)
 
    plt.plot(wave_for_plotting[:,0], wave_for_plotting[:,1], linewidth=2, linestyle='-', label=r'Data 1')

    # Adjust the page layout filling the page using the new tight_layout command
    plt.tight_layout(pad=0.5)

    # save the figure as a high-res pdf in the current folder
    # plt.savefig('plot_filename.pdf')

    # show the figure
    plt.show()
    
if CHECK_FFT: 
    fft_freq, fft_mag = CRAWLAB_fft(wave_for_plotting[:,1], wave_for_plotting[:,0], 0)
    # Set the plot size - 3x2 aspect ratio is best
    fig = plt.figure(figsize=(6,4))
    ax = plt.gca()
    plt.subplots_adjust(bottom=0.17, left=0.17, top=0.96, right=0.96)

    # Change the axis units font
    plt.setp(ax.get_ymajorticklabels(),fontsize=18)
    plt.setp(ax.get_xmajorticklabels(),fontsize=18)

    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')

    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

    # Turn on the plot grid and set appropriate linestyle and color
    ax.grid(True,linestyle=':', color='0.75')
    ax.set_axisbelow(True)

    # Define the X and Y axis labels
    plt.xlabel('Frequency (Hz)', fontsize=22, weight='bold', labelpad=5)
    plt.ylabel('FFT Magnitude', fontsize=22, weight='bold', labelpad=10)
 
    plt.plot(fft_freq, fft_mag, linewidth=2, linestyle='-', label=r'Data 1')
    
    # uncomment below and set limits if needed
    plt.xlim(0, 1.5 * np.max(FREQ))
    # plt.ylim(0,10)

    # Adjust the page layout filling the page using the new tight_layout command
    plt.tight_layout(pad=0.5)

    # save the figure as a high-res pdf in the current folder
    # plt.savefig('plot_filename.pdf')

    # show the figure
    plt.show()
    
# terminate the pyAudio instance
p.terminate()