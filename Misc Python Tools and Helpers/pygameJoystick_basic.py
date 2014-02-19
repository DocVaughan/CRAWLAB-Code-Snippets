# Standard
import sys, time

# PyGame for joystick
# Download from http://pygame.org/
import pygame

# DEFINES
VEL_SCALE = -1.0
ROT_SCALE = 1.0
ACCEL = 2.0

# MAIN SCRIPT
#
pygame.init()

# Joystick connection
print "\nConnecting to joystick..."
if pygame.joystick.get_count() < 1:
	print "No joystick found, quitting"
	sys.exit(1)
else:
	joy = pygame.joystick.Joystick(0)
	joy.init()
print "Joystick found"

while 1:
	try:
		for event in pygame.event.get():
			if event.type == pygame.QUIT: break
		if joy.get_button(0):
			print VEL_SCALE*joy.get_axis(1),ROT_SCALE*joy.get_axis(0)
		else:
			print 0., 0.
		time.sleep(0.1)
		
	except utils.TimeoutError:
                continue
	except KeyboardInterrupt:
		# Catches CTRL-C
		break

# Program terminated
print "Program finished, cleaning up..."
joy.quit()	
ccp.close()	
print "Cleanup successful, exiting..."
time.sleep(1)
sys.exit()	
