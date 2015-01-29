import socket
import threading
import SocketServer
import time
import Adafruit_BBIO.PWM as PWM

# TODO: Fix this nasty global variable hack
x_data = 0.
y_data = 0.

class Servo():
    def __init__(self, servo_pin):
        # Define duty cycle parameters for all servos
        self.duty_min = 3.
        self.duty_max = 14.5
        self.duty_span = self.duty_max - self.duty_min
        self.duty_mid = ((90.0 / 180) * self.duty_span + self.duty_min)
        self.servo_pin = servo_pin
    
    def start_servo(self):
        PWM.start(self.servo_pin, self.duty_mid, 60.0)

    def set_servo_angle(self, angle):
        angle_f = float(angle)
        duty = ((angle_f / 180) * self.duty_span + self.duty_min)
        PWM.set_duty_cycle(self.servo_pin, duty)

    def close_servo(self):
        PWM.stop(self.servo_pin)
        PWM.cleanup()


class ThreadedUDPRequestHandler(SocketServer.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
    
    def handle(self):
        global x_data, y_data
        data = self.request[0].strip()
        socket = self.request[1]
        string_to_print = "Data from {}: ".format(self.client_address[0]) + data
        
        x,sep,y = data.partition(',')
        x_data = float(x)
        y_data = float(y)
        
        #socket.sendto(data.upper(), self.client_address)
        self.data = data
        
        

class ThreadedUDPServer(SocketServer.ThreadingMixIn, SocketServer.UDPServer):
    pass


if __name__ == "__main__":
    global x_data
    global y_data
    
    # Start Servos
    servo1 = Servo('P8_13')
    servo2 = Servo('P8_19')
    
    servo1.start_servo()
    servo2.start_servo()

    # Port 0 means to select an arbitrary unused port
    HOST, PORT = "10.0.1.118", 2390
    
    server = ThreadedUDPServer((HOST, PORT), ThreadedUDPRequestHandler)
    ip, port = server.server_address
    
    # Start a thread with the server -- that thread will then start one
    # more thread for each request
    server_thread = threading.Thread(target=server.serve_forever)
    
    # Exit the server thread when the main thread terminates
    server_thread.daemon = True
    server_thread.start()
    print "Server loop running in thread:", server_thread.name
    
    try:
        while True:
            # convert (-100,100) range of UDP data to 0-180deg servo angle
            angle1 = 0.9 * x_data + 90.
            servo1.set_servo_angle(angle1)
            
            # convert (-100,100) range of UDP data to 0-180deg servo angle
            angle2 = 0.9 * y_data + 90.
            servo2.set_servo_angle(angle2)
            
    except (KeyboardInterrupt, SystemExit): # when you press ctrl+c
        servo1.close_servo()
        servo2.close_servo()
        
    print "Done.\nExiting."    
