import cv2
import zbar
import time

cap = cv2.VideoCapture(1)

try:
    while(True):
        # Capture frame-by-frame
        print 'Capturing frame...'
        ret, frame = cap.read()
        height, width, depth = frame.shape
    
        print 'Getting raw data...'
        raw = frame.tostring()
    
        cv2.imshow('frame',frame)
        cv2.waitKey(0)
    
        # wrap image data
        print 'Handing image off to zBar...'
        image = zbar.Image(width, height, 'Y800', raw)
    
        # create a reader
        print 'Creating reader...'
        scanner = zbar.ImageScanner()

        # configure the reader
        print 'Enabling reader...'
        scanner.parse_config('enable')

        # scan the image for barcodes
        print 'Scanning image...'
        scanner.scan(image)

        # extract results
        for symbol in image:
            # do something useful with results
            print 'decoded', symbol.type, 'symbol', '"%s"' % symbol.data

        print 'Pausing before repeating....\n\n'    
        # time.sleep(1)
        
except (KeyboardInterrupt, SystemExit):
    cv2.destroyAllWindows()
    cap.release() 