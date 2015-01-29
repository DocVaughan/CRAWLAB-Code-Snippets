#!/bin/bash
x11vnc -bg -o %HOME/.x11vnc.log.%VNCDISPLAY -auth /var/run/lightdm/root/:0 -forever