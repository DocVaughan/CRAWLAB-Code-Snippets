# Boot file
import machine
import os
uart = machine.UART(0, 115200)
os.dupterm(uart)
