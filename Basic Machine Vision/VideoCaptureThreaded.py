#! /usr/bin/env python

###############################################################################
# VideoCaptureThreaded.py
#
# Threaded video capture. Here, we're only using a single image, rather than a 
# Queue from the Python queue module. So, we could still end up blocking, etc.
#
# Modified from code at:
#  https://github.com/gilbertfrancois/video-capture-async
#
# NOTE: Any plotting is set up for output, not viewing on screen.
#       So, it will likely be ugly on screen. The saved PDFs should look
#       better.
#
# Created: 01/25/19
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

import threading
import time
import cv2


class VideoCaptureTreading:
    def __init__(self, src=0, width=640, height=480):
        self.src = src
        self.cap = cv2.VideoCapture(self.src)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.grabbed, self.frame = self.cap.read()
        self.started = False
        self.read_lock = threading.Lock()

    def set(self, var1, var2):
        self.cap.set(var1, var2)

    def start(self):
        if self.started:
            print('[!] Threaded video capturing has already been started.')
            return None
        self.started = True
        self.thread = threading.Thread(target=self.update, args=())
        self.thread.start()
        return self

    def update(self):
        while self.started:
            grabbed, frame = self.cap.read()
            with self.read_lock:
                self.grabbed = grabbed
                self.frame = frame

    def read(self):
        with self.read_lock:
            frame = self.frame.copy()
            grabbed = self.grabbed
        return grabbed, frame

    def stop(self):
        self.started = False
        self.thread.join()

    def __exit__(self, exec_type, exc_value, traceback):
        self.cap.release()


# Example usage
if __name__=='__main__':
    
    # Define the contants in the capture
    CAMERA = 1#'rtsp://admin:@192.168.2.43:88/videoMain' # can be a integer for webcams or IP address for network
    FRAME_WIDTH = 640
    FRAME_HEIGHT = 480
    NUM_FRAMES = 300
    THREADED = True # Set true for threaded version, false for blocking read
    
    # Create the capture instance - this is comparable to cv2.VideoCapture()
    # Comment out and 
    if THREADED:
        capture = VideoCaptureTreading(CAMERA)
        
        # Now, start the capture
        capture.start()
    else:
        capture = cv2.VideoCapture(CAMERA)
    
    # Set the desired image height and width
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)

    current_frame = 0
    time_start = time.time()    
    
    try:
        while (current_frame < NUM_FRAMES):
            frame_grabbed, frame = capture.read()
            
            frame = cv2.flip(frame, flipCode=0)
            cv2.imshow('Window', frame)

            if not (current_frame%30):                
                print(f'Read frame number {current_frame}.')
            
            # Wait 1 ms
            cv2.waitKey(1)
            
            current_frame = current_frame + 1
        
        elapsed_time = time.time() - time_start
        fps = NUM_FRAMES / elapsed_time
        print(f'{NUM_FRAMES} frames in {elapsed_time:.4f}s = {fps:.4f}fps')

    finally:
        if THREADED:
            capture.stop()

        cv2.destroyAllWindows()
