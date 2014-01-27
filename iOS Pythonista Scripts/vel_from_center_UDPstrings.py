from scene import *
import socket
import sound
import time

class MyScene (Scene):
	def setup(self):
		# This will be called before the first frame is drawn.
		# Set up the root layer and one other layer:
		self.root_layer = Layer(self.bounds)
		center = self.bounds.center()

		# Layer for the joystick "bubble"
		self.layer = Layer(Rect(center.x - 64, center.y - 64, 128, 128))
		self.layer.image = 'White_Circle'
		self.root_layer.add_layer(self.layer)

		# define points for initial touch and current touch location
		self.current = Point()

		# both desired velocities are initially zero
		self.velocity = Point(x=0, y=0)

		# set up UDP socket - IP address and socket to send to
		#self.HOST, self.PORT = '130.70.157.125', 2390
		self.HOST, self.PORT = '10.0.1.106', 2390
		

		# SOCK_DGRAM is the socket type to use for UDP sockets
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


	def draw(self):
		# Update and draw our root layer. For a layer-based scene, this
		# is usually all you have to do in the draw method.
		background(0.75, 0.75, 0.75) # light gray
		self.root_layer.update(self.dt)
		self.root_layer.draw()

		# format a data string to send
		data = self.velocity.as_tuple()
		data_str = str(data[0]) + ', ' + str(data[1])

		# send the velocity as x, y pair
		self.sock.sendto(data_str, (self.HOST, self.PORT))

		# Show the output on the screen
		text('Output = ' + data_str, font_name='Helvetica', font_size=36.0, x=self.size.w/2., y=50., alignment=5)

	def touch_began(self, touch):
		# Animate the layer to the location of the touch:
		self.current = touch.location

		# if the touch is in the "bubble" then
		if touch.location in self.layer.frame:
			
			sound.play_effect('Coin_3')
			# Set up a new frame based on latest touch location
			new_frame = Rect(self.current.x - 64, self.current.y - 64, 128, 128)
			self.layer.animate('frame', new_frame)
		else: 
			sound.play_effect('Error')
			time.sleep(0.25)
			sound.play_effect('Error')

	def touch_moved(self, touch):
		# if the touch is in the "bubble" then
		if touch.location in self.layer.frame:
			self.current = touch.location

			# Set up a new frame based on latest touch location
			new_frame = Rect(self.current.x- 64, self.current.y - 64, 128, 128)
			self.layer.animate('frame', new_frame,0.01)

			# Calculate the relative x, y distance from center
			deltaX = (self.current.x - self.size.w/2.)/(self.size.w/2.-64)*100
			deltaY = (self.current.y - self.size.h/2.)/(self.size.h/2.-64)*100

			# round to nearest integer
			deltaX = int(deltaX)
			deltaY = int(deltaY)

			# and limit to between -100 and 100
			deltaX = max(min(100,deltaX),-100)
			deltaY = max(min(100,deltaY),-100)

			# The velocity is proportional to offset from center of screen
			self.velocity.x = deltaX
			self.velocity.y = deltaY
			

			# Various debugging print statements
			#velocity = sqrt((deltaX)**2 + (deltaY)**2)
			#angle = math.atan2(deltaY, deltaX)
			#print('Velocity = ' + str(round(velocity,2)) + ' at ' + str(round(angle * 180/math.pi, 2)) + 'deg.')
			#print('Moved to: ' + str(touch.location.x) + ', ' + str(touch.location.y))
			#print('Delta:    ' + str(deltaX) + ', ' + str(deltaY))
			#print('Sample Time: ' + str(self.dt) + 's')

			# print('Velocity = ' + str(self.velocity.x) + ', ' + str(self.velocity.y))

	def touch_ended(self, touch):
		# if the touch ends, immediately reset the velocities to 0
		self.velocity.x, self.velocity.y = 0, 0
		
		# debugging print
		#print('Velocity = ' + str(int(self.velocity.x)) + ', ' + str(int(self.velocity.y)))

		new_frame = Rect(self.size.w*0.5 - 64, self.size.h*0.5 - 64, 128, 128)
		self.layer.animate('frame', new_frame)


if __name__ == '__main__':
	gui = MyScene()
	run(gui)
