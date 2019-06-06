        #! /usr/bin/env python

###############################################################################
# heartbeat_sender_basic.py
#
# Basic heartbeat sedner using the Adafruit RFM9x LoRa radio bonnet for Raspberry Pi
#
# Based on code from:
#    https://learn.adafruit.com/lora-and-lorawan-for-raspberry-pi
#
# Created: 06/06/19
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


# Import Python System Libraries
import time
import subprocess

# Import Blinka Libraries for basic board control
import busio
from digitalio import DigitalInOut, Direction, Pull
import board

# Import the SSD1306 module for the OLED dispay
import adafruit_ssd1306

# Import RFM9x for the LoRa radio
import adafruit_rfm9x

# The Bonnet has onboard buttons. We'll set those up.
# All have pullup resistors, so pressed buttons read as low (0 or False)
# Button A
btnA = DigitalInOut(board.D5)
btnA.direction = Direction.INPUT
btnA.pull = Pull.UP

# Button B
btnB = DigitalInOut(board.D6)
btnB.direction = Direction.INPUT
btnB.pull = Pull.UP

# Button C
btnC = DigitalInOut(board.D12)
btnC.direction = Direction.INPUT
btnC.pull = Pull.UP

# Create the I2C interface.
i2c = busio.I2C(board.SCL, board.SDA)

# 128x32 OLED Display
display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, addr=0x3c)
# Clear the display.
display.fill(0)
display.show()
width = display.width
height = display.height

# Configure LoRa Radio
CS = DigitalInOut(board.CE1)
RESET = DigitalInOut(board.D25)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 915.0)
rfm9x.tx_power = 23
prev_packet = None

# Define the heartbeat and acknowledgement data packets
HEARTBEAT = bytes("$ULheartbeat\r\n", "utf-8")
ACKNOWLEDGE = "$UL_ACK"

# How often to send the heartbeat message
HEARTBEAT_SEND_TIME = 0.5

# Do we want to wait for acknowledgement of the heartbeat?
WAIT_FOR_ACK_PACKET = False

# Default to not sending heartbeats at startup
# This is safer, as it requires explicit action by use to initiate operation
status_okay = False  

# draw a box to clear the image
display.fill(0)
display.text('Init. Complete', 0, 0, 1)
display.show()
time.sleep(1.0)

try:
    last_time = 0.0  # Used to send at a fixed rate, but sample buttons faster
                
    while True:
        if not btnC.value:
            display.fill(0)
            # Button C is the E-stop button
            display.text("STOP!!!", 60, 0, 1)
            display.show()
            time.sleep(2)
            status_okay = False
        
        elif not btnB.value:
            # Button B will undo the latched E-stop from button C
            display.fill(0)
            display.text("Starting up in 1sec.", 0, 0, 1)
            display.show()
            time.sleep(1)
            status_okay = True
        
        elif not btnA.value:
            display.fill(0)
            
            # Shell scripts for system monitoring from here:
            # https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
            cmd = "hostname -I | cut -d\' \' -f1"
            IP = subprocess.check_output(cmd, shell=True).decode("utf-8")
            cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
            CPU = subprocess.check_output(cmd, shell=True).decode("utf-8")
            cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%s MB  %.2f%%\", $3,$2,$3*100/$2 }'"
            MemUsage = subprocess.check_output(cmd, shell=True).decode("utf-8")
            cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%d GB  %s\", $3,$2,$5}'"
            Disk = subprocess.check_output(cmd, shell=True).decode("utf-8")

            # Write the text results from those commands to the OLED
            display.text("IP: "+IP, 0, 0, 1)
            display.text(CPU, 0, 8, 1)
            display.text(MemUsage, 0, 16, 1)
            display.text(Disk, 0, 24, 1)
            
            display.show()
            time.sleep(1)
        
        
        if status_okay:
            current_time = time.time()
            elapsed_time = current_time - last_time

            display.fill(0)
    
            if elapsed_time >= HEARTBEAT_SEND_TIME:
                rfm9x.send(HEARTBEAT)
                display.fill(0)
                display.text('Heartbeat: *', 0, 0, 1)
                
                if WAIT_FOR_ACK_PACKET:
                    print('Waiting for ACK packet.')
                    packet = None

                    # check for acknowledgement packet
                    packet = rfm9x.receive(timeout=0.1)
            
                    if packet is None:
                        display.text('Acknowledged: :(', 0, 8, 1)

                    else:
                        packet_text = str(packet, "utf-8")
                    
                        # Also read the RSSI (signal strength) of the last received message and
                        # print it.
                        rssi = rfm9x.rssi
                        display.text('RSSI: {0} dB'.format(rssi), 0, 16, 1)
                
                        if packet_text.startswith('$UL_ACK'):
                            display.text('Acknowledged: :)', 0, 8, 1)
                        else:
                            display.text('Acknowledged: :<', 0, 8, 1)

                last_time = current_time

            else:
                display.text('Heartbeat:  ', 0, 0, 1)

        else:
            display.fill(0)
            display.text('Currently E-stopped', 0, 0, 1)

        display.show()
        time.sleep(0.01)

finally:
    # draw a box to clear the image
    display.fill(0)
    display.text('Script exited.', 0, 0, 1)
    display.show()
