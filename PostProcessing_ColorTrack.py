#! /usr/bin/env python 
 
import cv2.cv as cv
from time import localtime, strftime
from Tkinter import Tk
from tkFileDialog import askopenfilename
 
color_tracker_window = "Color Tracker"

filename = strftime("%m_%d_%Y_%H%M") #names the output file as the date and time that the program is run
filepath = filename + ".txt" #gives the path of the file to be opened
    
f = open(filepath, "a+") #opens the output file in append mode
f.write('Time (s), X Position (pixels), Y Position (pixels)' + '\n') 


class ColorTracker:
    def __init__(self): 
#         cv.NamedWindow( color_tracker_window, 1 ) 

        Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
        video_filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
        
        self.capture = cv.CaptureFromFile(video_filename)
        
        
    def run(self): 
        initialTime = 0. #sets the initial time
        num_Frames = int(  cv.GetCaptureProperty( self.capture, cv.CV_CAP_PROP_FRAME_COUNT ) )
        fps = cv.GetCaptureProperty( self.capture, cv.CV_CAP_PROP_FPS )
        
        for ii in range(num_Frames-8):
        
            print('Frame: ' + str(ii) + ' of ' + str(num_Frames))
            # read the ii-th frame
            img = cv.QueryFrame( self.capture )           
            
            # Blur the source image to reduce color noise 
            cv.Smooth(img, img, cv.CV_BLUR, 3); 
            
            # Convert the image to hsv(Hue, Saturation, Value) so its  
            # It's easier to determine the color to track(hue) 
            hsv_img = cv.CreateImage(cv.GetSize(img), 8, 3) 
            cv.CvtColor(img, hsv_img, cv.CV_BGR2HSV) 
            
            # limit all pixels that don't match our criteria, in the	is case we are  
            # looking for purple but if you want you can adjust the first value in  
            # both turples which is the hue range(120,140).  OpenCV uses 0-180 as  
            # a hue range for the HSV color model 
            thresholded_img =  cv.CreateImage(cv.GetSize(hsv_img), 8, 1) 
            
            # uncomment below for tracking blue
#             cv.InRangeS(hsv_img, (112, 50, 50), (118, 200, 200), thresholded_img) 

            # tracking red
            cv.InRangeS(hsv_img, (160, 150, 100), (180, 255, 255), thresholded_img) 
            
            #determine the objects moments and check that the area is large  
            #enough to be our object 
            thresholded_img2 = cv.GetMat(thresholded_img)
            moments = cv.Moments(thresholded_img2,0) 
            area = cv.GetCentralMoment(moments, 0, 0) 
            
            # there can be noise in the video so ignore objects with small areas 
            if(area > 2500): 
                #determine the x and y coordinates of the center of the object 
                #we are tracking by dividing the 1, 0 and 0, 1 moments by the area 
                x = cv.GetSpatialMoment(moments, 1, 0)/area 
                y = cv.GetSpatialMoment(moments, 0, 1)/area

                elapsedTime = ii/fps
            
                f.write(str(elapsedTime) + ',' + '%013.9f' % x + ',' + '%013.9f' % y + "\n") #prints output to the specified output file for later use
#                 
#                 x = int(x)
#                 y = int(y)
#                 
#                 #create an overlay to mark the center of the tracked object 
#                 overlay = cv.CreateImage(cv.GetSize(img), 8, 3) 
#                 
#                 cv.Circle(overlay, (x, y), 2, (255, 255, 255), 20) 
#                 cv.Add(img, overlay, img) 
#                 #add the thresholded image back to the img so we can see what was  
#                 #left after it was applied 
#                 cv.Merge(thresholded_img, None, None, None, img) 
#              
#             #display the image  
#             cv.ShowImage(color_tracker_window, img) 
            
        # close the data file
        f.close()

                
if __name__=="__main__": 
    color_tracker = ColorTracker() 
    color_tracker.run() 
