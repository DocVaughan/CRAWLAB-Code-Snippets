#!/bin/sh

# This script will open a full-screen chromium window at the IP address 
# specified. It is useful for starting web-based robot GUIs remotely. The 
# leading DISPLAY option will open on native display even if starting over SSH
#
# Created: 07/09/20 - JEV - joshua.vaughan@louisiana.edu

DISPLAY=:0.0 chromium-browser --noerrdialogs --incognito --kiosk 127.0.0.1:5000
