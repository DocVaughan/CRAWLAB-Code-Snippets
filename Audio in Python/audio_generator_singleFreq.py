#! /usr/bin/env python

###############################################################################
# audio_generator_singleFreq.py
#
# Script to generate audio files/arrays. This script is limited to a single
# output frequency (a single note)
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
PLAY_SOUND = True      # set true to play any sounds generated
WRITE_WAV = True        # set true to save the sound to a wav file named by 

# Define the desired output filename
WAV_OUTPUT_FILENAME = 'single_freq_test.wav'

# Set up the audio specifications
BITRATE = 44100         # number of frames per second/frameset
NUM_CHANNELS = 1        # number of channels (usually 1 or 2 = mono or stereo)
DURATION = 1            # seconds to play sound

# Create a PyAudio() instance
p = pyaudio.PyAudio()

# Define the necessary constants for the portaudio api
PORT_AUDIO_FORMAT = p.get_format_from_width(1)
SAMPLE_WIDTH = p.get_sample_size(PORT_AUDIO_FORMAT)

# the number of frames given how long we want to play at the given bitrate
NUMBER_OF_FRAMES = int(BITRATE * DURATION)   

# fill leftover frames to match the bitrate   
RESTFRAMES = NUMBER_OF_FRAMES % BITRATE

WAVEDATA = ''    

# Define the frequency of the desired wave(s)
FREQUENCY = 440     # Hz, 261.63=C4, 440=A4 notes on piano, etc

if FREQUENCY > BITRATE:
    BITRATE = FREQUENCY + 100

for sample in range(NUMBER_OF_FRAMES):
    WAVEDATA = WAVEDATA + chr(int(np.sin(sample / ((BITRATE/FREQUENCY)/np.pi))*127 + 128))

for _ in range(RESTFRAMES): 
    WAVEDATA = WAVEDATA + chr(128)


if WRITE_WAV: # Write the wave file
    wf = wave.open(WAV_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(NUM_CHANNELS)
    wf.setsampwidth(SAMPLE_WIDTH)
    wf.setframerate(BITRATE)                    
    wf.writeframes(WAVEDATA.encode('utf-8'))    # Actually write to file
    wf.close()                                  # Now close the file


if PLAY_SOUND: # set up and play the sound through the speakers
    stream = p.open(format = PORT_AUDIO_FORMAT , 
                    channels = NUM_CHANNELS, 
                    rate = BITRATE, 
                    output = True)
    stream.write(WAVEDATA) # Actually play the sound
    
    # Now, stop the stream and close it
    stream.stop_stream()
    stream.close()

# terminate the pyAudio instance
p.terminate()