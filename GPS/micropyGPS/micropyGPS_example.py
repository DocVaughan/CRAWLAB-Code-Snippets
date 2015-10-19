# main.py -- put your code here!

###############################################################################
# main.py
#
# Script demonstrating logging GPS data to an SD card
# This will send a command to set an Adafruit Ultimate GPS to update at 5Hz
#   pg. 8-9 of http://www.adafruit.com/datasheets/PMTK_A11.pdf
# 
# After the command is sent, we'll just print the strings we recieve
#
# Most adapted from:
#    http://docs.micropython.org/en/latest/pyboard/tutorial/timer.html
#
# Created: 08/07/15
#   - Joshua Vaughan
#   - joshua.vaughan@louisiana.edu
#   - http://www.ucs.louisiana.edu/~jev9637
#
# Modified:
#   *
#
###############################################################################

from micropyGPS import MicropyGPS

def convert_longitude(long_EW):
    """ Function to convert deg m E/W longitude to DD.dddd (decimal degrees)
    
    Arguments:
      long_EW : tuple representing longitude
                in format of MicroGPS gps.longitude
    
    Returns:
      float representing longtidue in DD.dddd
    """
    
    return (long_EW[0] + long_EW[1] / 60) * (1.0 if long_EW[2] == 'E' else -1.0)

def convert_latitude(lat_NS):
    """ Function to convert deg m N/S latitude to DD.dddd (decimal degrees)
    
    Arguments:
      lat_NS : tuple representing latitude
                in format of MicroGPS gps.latitude
    
    Returns:
      float representing latitidue in DD.dddd
    """
    
    return (lat_NS[0] + lat_NS[1] / 60) * (1.0 if lat_NS[2] == 'N' else -1.0)


blueLED = pyb.LED(4)  # create object of blue LED

# This example uses UART 3 with RX on pin Y10
# Baudrate is 9600bps, with the standard 8 bits, 1 stop bit, no parity
uart = pyb.UART(3, 9600)

# We can also have finer control over the serial communication 
uart.init(9600, bits=8, parity=None, stop=1, read_buf_len = 512)

# Set up the GPS instance
gps = MicropyGPS()

blueLED.on()          # turn on blue LED as indicator of logging
# open file to write data - /sd/ is the SD-card, /flash/ is the internal memory
with open('/sd/GPS_log.csv', 'w') as log:
    log.write('Time (ms), Longitude, Latitude, Heading, \
                Speed (m/s), Number of Satellites\n')    # write heading to file

     # Now we can read the data for until control-c is pressed
    start_time = pyb.millis()

    while pyb.elapsed_millis(start_time) < 60000: # log data for 60 seconds
        if uart.any():
            valid_sentence_received = gps.update(chr(uart.readchar())) # Note the conversion to to chr, UART outputs ints normally
            
            if valid_sentence_received:
                long_decimal = convert_longitude(gps.longitude)
                lat_decimal = convert_latitude(gps.latitude)
                log.write('{},{},{},{},{},{}\n'.format(pyb.elapsed_millis(start_time),
                                                       long_decimal,
                                                       lat_decimal,
                                                       gps.course,
                                                       gps.speed[0] * 0.514,
                                                       gps.satellites_in_use))
    
blueLED.off()          # turn on blue LED as indicator of finished logging
