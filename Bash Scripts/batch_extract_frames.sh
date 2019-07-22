#!/bin/bash

for filename in *.m4v
do
    echo ""
    echo "Extracting frames from $filename"
    echo ""
    basename=${filename%.m4v}
        
    ffmpeg -i $filename -vf "select=not(mod(n\,60))" -vsync vfr -q:v 2 ${basename}_%03d.jpg
done