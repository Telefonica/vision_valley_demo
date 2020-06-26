#!/bin/bash

python3 rtsp_server_gstreamer.py  -config_path gserver.conf \
& python3 rtsp_server_gstreamer.py  -config_path gserver2.conf \
#& python3 rtsp_server_gstreamer.py  -config_path gserver3.conf 
&&

echo "Streams up"
