from scene import *
import socket

class MyScene (Scene):
   def setup(self):
       # This will be called before the first frame is drawn.
       # Set up the root layer and one other layer:
       self.root_layer = Layer(self.bounds)
       
       # variable for 'deadman switch' touch event
       self.deadmanTouch = False 
       
       # initial velocity is zero in both directions
       self.velocity = Point(x = 0, y = 0)
       self.data_str = str(self.velocity.x) + ', ' + str(self.velocity.y)
       
       # Set up UDP - IP address and port to send to
       # self.HOST, self.PORT = '130.70.157.125', 2390
       # self.HOST, self.PORT = '10.0.1.118', 2390
       self.HOST, self.PORT = '192.168.1.11', 2390
       
       # SOCK_DGRAM is the socket type to use for UDP sockets
       self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
       
       # set up bubble image
       self.x = self.size.w * 0.5
       self.y = self.size.h * 0.5
       self.layer = Layer(Rect(self.x - 64, self.y - 64, 128, 128))
       self.layer.image = 'White_Circle'
       self.root_layer.add_layer(self.layer)


   def draw(self):
       # if the user is touching the screen, update velocity based on tilt
       if self.deadmanTouch:
           backgroundColor = Color(0.75, 0.75, 0.75) #light gray
           g = gravity()
           self.x += g.x * 10
           self.y += g.y * 10
           self.x = min(self.size.w - 64, max(64, self.x))
           self.y = min(self.size.h - 64, max(64, self.y))
           new_frame = Rect(self.x - 64, self.y - 64, 128, 128)
           
       else:
           backgroundColor = Color(0, 0, 0) #black
           self.x = self.size.w * 0.5
           self.y = self.size.h * 0.5
           new_image = 'White_Circle'
           new_frame = Rect(self.x - 64, self.y - 64, 128, 128)
       
       # calculate the velocity as a % of maximum displacement in x, y
       # Limit to integer values
       x_vel = int( 100 * (self.x - self.size.w/2.) / (self.size.w/2.-64) )
       y_vel = int( 100 * (self.y - self.size.h/2.) / (self.size.h/2.-64) )
       
       # make a string velocities as comma separated valued
       self.data_str = str(x_vel) + ', ' + str(y_vel)
       
       # send velocity as x, y pair string
       self.sock.sendto(self.data_str, (self.HOST, self.PORT))

       # save velocity in the scene 
       self.velocity.x, self.velocity.y = x_vel, y_vel
       
       # update the location of the bubble and change background color based on touch
       self.layer.animate('frame', new_frame, 0.1)
       self.root_layer.animate('background', backgroundColor, 0.1)
       
       # add a text layer to show the output
       screen_string= 'Output = ' + self.data_str
       text_layer = TextLayer(screen_string, 'Futura-Medium', 36)
       text_layer.frame.center(self.size.w/2.,50)
       self.add_layer(text_layer)
       
       # Draw the updates
       self.root_layer.update(self.dt)
       self.root_layer.draw()
       
       # A hack for now...
       #   remove the text layer in order to animate the changes next cycle
       text_layer.remove_layer()
   
   
   def touch_began(self, touch):
       self.deadmanTouch = True 
   
   
   def touch_moved(self, touch):
       pass
   
   
   def touch_ended(self, touch):
       self.deadmanTouch = False 

       
run(MyScene())

