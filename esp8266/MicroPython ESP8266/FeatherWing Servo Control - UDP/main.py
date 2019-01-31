###############################################################################
# main.py
#
# main script for basic servo control using an Adafruit esp8266 feather with 
# their 8-channel PWM/servo FeatherWing
#
# Feather - https://www.adafruit.com/product/2821
# FeatherWing - https://www.adafruit.com/product/2928
#
# The pca9685.py and servo.py files from this repository must be copied to the
# esp8266
#  https://github.com/DocVaughan/micropython-adafruit-pca9685
#
#
#
# Created: 01/30/19
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

from machine import Pin, I2C
import time

# Imports for the servo FeatherWing
import pca9685
import servo

# Imports for networking
import socket
import network

# Configuration constants
UDP_TIMEOUT = 0.0               # Timeout for UDP communications (s), if 0 go into nonblocking mode
UDP_PORT = 2390                 # Port to receive data on
RECV_BUFF_SIZE = 16             # Size of buffer for UDP data


# Blink the LED every 100ms to indicate we made it into the main.py file
for _ in range(10):
    time.sleep_ms(100)
    pin.value(not pin.value()) # Toggle the LED while trying to connect
    time.sleep_ms(100)

# Make sure the LED is off
pin.value(1)

# Create the UDP socket
sock = socket.socket(socket.AF_INET,    # Internet
                     socket.SOCK_DGRAM) # UDP

# Construct an I2C bus
i2c = I2C(scl=Pin(5), sda=Pin(4), freq=100000)

# Define the servos instance
# In the case of the feather it will contain 8 possible servos
servos = servo.Servos(i2c)

# We'll just be controlling servo number 0 here
SERVO_NUMBER = 0

# Get the current IP address and port UDP_PORT information
# UDP_PORT is defined in config block at top of file
UDP_server_address = socket.getaddrinfo('0.0.0.0', UDP_PORT)[0][-1]
sock.bind(UDP_server_address)


# Create a timeout on UDP communication to avoid blocking forever
sock.settimeout(UDP_TIMEOUT) 

def UDP_recv():
    """ 
    Function to recveive data on UDP with a timeout and 
    catch the timeout exception 

    Returns:
        angle to move to if data was received
        None otherwise
    """
    try:
        data, addr = sock.recvfrom(RECV_BUFF_SIZE) # buffer size is 1024 bytes
        print(data)
        # Convert the data packet to an floating point number
        angle = float(data)

#         print(angle)
        
    except (OSError, ValueError):
        # Either received no data or improperly formatted data
        angle = None # will result in servo not moving
    
    return angle



try:
    # Move the servo in position 80deg
    # 80 deg was actually center on the servo I was testing on
    # The default possible range is 0-180. However, note that most servos, even
    # if advertised as having that range, do not. +/-60 deg around the center
    # is much more reliable. +/-45deg around center is even better.
    servos.position(SERVO_NUMBER, 80)

    while True:
        # Always be receiving
        angle = UDP_recv()

        # Move the servo to the position received from the UDP message
        # The servo library takes care of limiting this to an acceptable range
        # In practice, we would probably want to limit further and/or add
        # additional safety checks.
        servos.position(SERVO_NUMBER, angle)
        
        time.sleep_ms(1)

except (KeyboardInterrupt, SystemExit):
    # Close the socket and release the servo
    sock.close()
    servos.release(0)
