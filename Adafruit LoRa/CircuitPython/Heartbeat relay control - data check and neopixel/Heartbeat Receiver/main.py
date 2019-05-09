import digitalio
import board
import busio
import time
import neopixel
import adafruit_rfm9x


# Set up the onboard LED
led = digitalio.DigitalInOut(board.D13)
led.direction = digitalio.Direction.OUTPUT

# Set up the digital output to control the relay
relay = digitalio.DigitalInOut(board.D5)
relay.direction = digitalio.Direction.OUTPUT
relay.value = False

# Set up the neopixels for status indication and define some colors
NUM_LEDS = 30                   # Number of LEDs in the array
PIXEL_ORDER = neopixel.GRB      # Order of colors in tuples, ours are GRB
pixels = neopixel.NeoPixel(board.D6, 
                           NUM_LEDS,
                           pixel_order=PIXEL_ORDER,
                           auto_write=False)

# Define the tuples of GRB colors for each color we want to show
OFF = (0,0,0)
WHITE_HIGH = (255,255,255)
WHITE_LOW = (16,16,16)
RED_HIGH = (0,255,0)
RED_LOW = (0,16,0)
GREEN_HIGH = (255,0,0)
GREEN_LOW = (16,0,0)
BLUE_HIGH = (0,0,255)
BLUE_LOW = (0,0,16)
YELLOW_HIGH = (200,100,0)
YELLOW_LOW = (10,20,0)

# Set up the LoRa transmission
RADIO_FREQ_MHZ = 915.0
CS = digitalio.DigitalInOut(board.RFM9X_CS)
RESET = digitalio.DigitalInOut(board.RFM9X_RST)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, RADIO_FREQ_MHZ)

# Variables to monitor the heartbeat status
heartbeats_missed = 0
MAX_MISSED_HEARTBEATS = 5

while (True):
    # Wait for a packet to be received (up to timeout=0.1 seconds)
    packet = rfm9x.receive(timeout=0.1)  
    
    if packet is not None:
        try:
            packet_text = str(packet, 'ascii')
        
            # Now, check that the packet was actually the heartbeat packet
            if packet_text == '$ULheartbeat':
                print('Received: {0}'.format(packet_text))

                # Reset the heartbeat missed counter
                heartbeats_missed = 0
                led.value = not led.value    # toggle the onboard LED
                relay.value = True           # Keep the relay energized

            else: # If it wasn't still increment the missed counter
                heartbeats_missed = heartbeats_missed + 1

        except (UnicodeError):
            # If we can't properly parse the packet, consider it a missed
            # heartbeat
            heartbeats_missed = heartbeats_missed + 1

    else:
        heartbeats_missed = heartbeats_missed + 1
        
    if heartbeats_missed > 0 and heartbeats_missed < MAX_MISSED_HEARTBEATS:
        print('Have missed {:d} heartbeats'.format(heartbeats_missed))
        
    elif heartbeats_missed == MAX_MISSED_HEARTBEATS:
        print('Have missed {:d} heartbeats'.format(heartbeats_missed))
        print('Missed too many heartbeats.')
        
        led.value = True    # Turn on the onboard red LED
        relay.value = False  # And de-energize the relay coils
        
        pixels.fill(RED_HIGH)
    
    pixels.show()
