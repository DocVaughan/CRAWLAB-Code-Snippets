# This program allows you to select the color ranges of OpenCv using sliders.
# Slide them around till only your object is visible.
# Press esc when you are done.
# Written by Aruldd on http://stackoverflow.com/questions/10948589/choosing-
# correct-hsv-values-for-opencv-thresholding-with-inranges
# Forrest Montgomery added 3 more sliders to make the range truly a range
# And combined Thura Hlaing's cvpicker.py from gist.github.com/trhura

import cv2
import numpy as np

colors = []

FILENAME = '/Users/josh/Desktop/jump_freq.m4v'
WEBCAM = False


def nothing(x):
    pass


def on_mouse_click(event, x, y, flags, frame):
    if event == cv2.EVENT_LBUTTONUP:
        colors.append(frame[y, x].tolist())


def main():
    # if using a webcam, load the camera
    if WEBCAM:
        capture = cv2.VideoCapture(0)
    # otherwise, grab a reference to the video file
    else:
        capture = cv2.VideoCapture(FILENAME)

#     while True:
    # Reads a video frames
    _, frame = capture.read()
    # hsv = frame
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    cv2.putText(hsv, 'Press q when done', (500, 50),
                cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2,)
    if colors:
        cv2.putText(hsv, str(colors[-1]), (10, 50), cv2.FONT_HERSHEY_PLAIN,
                    2, (0, 0, 0), 2)
    cv2.imshow('frame', hsv)
    cv2.setMouseCallback('frame', on_mouse_click, hsv)

    while not cv2.waitKey(1) & 0xFF == ord('q'):
        pass

    # releases the windows
    capture.release()
    cv2.destroyAllWindows()

    h_low = min(c[0] for c in colors)
    s_low = min(c[1] for c in colors)
    v_low = min(c[2] for c in colors)
    maxb = max(c[0] for c in colors)
    maxg = max(c[1] for c in colors)
    maxr = max(c[2] for c in colors)
    # print h_low, s_low, v_low, maxr, maxg, maxb

    lb = [h_low, s_low, v_low]
    ub = [maxb, maxg, maxr]
    print('Lower boundary: {} \n Upper boundary: {}'.format(lb, ub))

    # if using a webcam, load the camera
    if WEBCAM:
        capture = cv2.VideoCapture(0)
    # otherwise, grab a reference to the video file
    else:
        capture = cv2.VideoCapture(FILENAME)

    # Creating a window for later use
    cv2.namedWindow('result')

    # Starting with 100's to prevent error while masking
    # h_low, s_low, v_low = 100, 100, 100
    # h_high, s_high, v_high = 200, 200, 200

    # Creating track bar
    cv2.createTrackbar('h_low', 'result', h_low, 179, nothing)
    cv2.createTrackbar('s_low', 'result', s_low, 255, nothing)
    cv2.createTrackbar('v_low', 'result', v_low, 255, nothing)
    cv2.createTrackbar('h_high', 'result', h_low + 25, 179, nothing)
    cv2.createTrackbar('s_high', 'result', 255, 255, nothing)
    cv2.createTrackbar('v_high', 'result', 255, 255, nothing)


    # capture another frame to test the result
    _, frame = capture.read()

    # converting to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    while(1):
        # get info from track bar and appy to result
        h_low = cv2.getTrackbarPos('h_low', 'result')
        s_low = cv2.getTrackbarPos('s_low', 'result')
        v_low = cv2.getTrackbarPos('v_low', 'result')

        h_high = cv2.getTrackbarPos('h_high', 'result')
        s_high = cv2.getTrackbarPos('s_high', 'result')
        v_high = cv2.getTrackbarPos('v_high', 'result')

        # Normal masking algorithm
        lower_blue = np.array([h_low, s_low, v_low])
        upper_blue = np.array([h_high, s_high, v_high])

        mask = cv2.inRange(hsv, lower_blue, upper_blue)

        result = cv2.bitwise_and(frame, frame, mask=mask)

        cv2.imshow('result', result)

        cv2.putText(hsv, 'Press q when done', (500, 50),
                    cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2,)

        k = cv2.waitKey(5) & 0xFF
        
        if k == 27:
            print('Hue lower: {}'.format(h_low))
            print('Saturation lower: {}'.format(s_low))
            print('Value lower: {}'.format(v_low))
            print('Hue upper: {}'.format(h_high))
            print('Saturation upper: {}'.format(s_high))
            print('Value upper: {}'.format(v_high))
            break

    cap.release()

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
