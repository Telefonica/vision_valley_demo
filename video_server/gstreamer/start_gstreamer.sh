#!/bin/bash
#Start app: gstreamer server
sudo kill $(sudo lsof -t -i:8554) 2>/dev/null
sudo kill $(sudo lsof -t -i:8555) 2>/dev/null
sudo kill $(sudo lsof -t -i:8556) 2>/dev/null
python3 rtsp_server_gstreamer.py  -config_path gserver.conf &
python3 rtsp_server_gstreamer.py  -config_path gserver2.conf &
python3 rtsp_server_gstreamer.py  -config_path gserver3.conf &