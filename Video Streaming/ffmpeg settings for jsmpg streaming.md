# ffmpeg settings and commands for [jsmp3g](https://github.com/phoboslab/jsmpeg)

## List all video objects - From https://trac.ffmpeg.org/wiki/Capture/Webcam
### OS X
* For avfoundation

        ffmpeg -f avfoundation -list_devices true -i ""    
    
* For qt

        ffmpeg -f qtkit -list_devices true -i ""    
     
    
### Linux

    v4l2-ctl --list-devices  


## Starting the video stream from the local machine
* See: http://phoboslab.org/log/2013/09/html5-live-video-streaming-via-websockets
* Change the IP address and password to match the server
* The password is the one set up from the stream_server.js launch on the server
* In these examples, the resolution is set to 640x480. It will likely need to be changed too.

### OS X
    ffmpeg -s 640x480 -f avfoundation -i "" -f mpeg1video -b 800k -r 30 http://ip_address:8082/password/640/480/
    
    ffmpeg -s 640x480 -f qtkit -i "" -f mpeg1video -b 800k -r 30 http://ip_address:8082/password/640/480/

I have gotten errors setting the resolution with the -s option. I just removed it and the resolution. So, for avfoundation the command would become:    

    ffmpeg -f avfoundation -i "" -f mpeg1video -b 800k -r 30 http://ip_address:8082/password/640/480/



### Linux

    ffmpeg -s 640x480 -f video4linux2 -i /dev/video0 -f mpeg1video -b 800k -r 30 http://ip_address:8082/password/640/480/

