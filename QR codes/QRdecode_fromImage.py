#! /usr/bin/env python

##########################################################################################
# QRdecode_fromImage.py
#
# simple script using zbar to decode the QR codes in an image
#
# NOTE: The zbar C libary must be installed for this to work
#       I recommend using homebrew -> $ brew install zbar
#
# Modified from: scan_image.py example from https://github.com/npinchot/zbar
#
# NOTE: Any plotting is set up for output, not viewing on screen.
#       So, it will likely be ugly on screen. The saved PDFs should look
#       better.
#
# Created: 01/21/15
#   - Joshua Vaughan
#   - joshua.vaughan@louisiana.edu
#   - http://www.ucs.louisiana.edu/~jev9637
#
# Modified:
#   *
#
##########################################################################################

import zbar
from PIL import Image, ImageEnhance

FILE_NAME = 'images/phbooth_7percent.jpg'
SHOW_IMAGES = True

# create a reader
scanner = zbar.ImageScanner()

# configure the reader
scanner.parse_config('enable')

# obtain image data using PILLOW
image = Image.open(FILE_NAME)
width, height = image.size


if SHOW_IMAGES:
    image.show(title='Image before grayscale conversion')

#conver the image to B/W
image = image.convert('L')

if SHOW_IMAGES:
    image.show(title='Image after grayscale conversion')
    
# Increase contrast?
enhancer = ImageEnhance.Contrast(image)
image = enhancer.enhance(2.0)

# Sharpen?
enhancer = ImageEnhance.Sharpness(image)
image = enhancer.enhance(2.0)

if SHOW_IMAGES:
    image.show(title='Image after sharpening and adding contrast')

raw = image.tostring()

# wrap image data
QRimage = zbar.Image(width, height, 'Y800', raw)

# scan the image for barcodes
scanner.scan(QRimage)

# extract results
for symbol in QRimage:
    # do something useful with results
    print 'decoded', symbol.type, 'symbol', '"%s"' % symbol.data

# clean up
del(image)
