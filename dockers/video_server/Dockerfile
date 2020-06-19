FROM python

USER root

RUN rm /bin/sh && ln -s /bin/bash /bin/sh

#RUN apt-get clean && apt-get update && apt-get install -y sudo gstreamer1.0-plugins-base gstreamer1.0-plugins-bad lsof gir1.2-gst-rtsp-server-1.0 python3 python3-pip
RUN apt-get autoclean && apt-get autoremove && apt-get update && apt-get install -y sudo gstreamer1.0-plugins-base gstreamer1.0-plugins-bad lsof gir1.2-gst-rtsp-server-1.0

## Fetch code from git
RUN git init && git remote add -f origin git@github.com:Telefonica/vision_valley_demo.git && git config core.sparseCheckout true && echo "video_server/" >> .git/info/sparse-checkout && git pull --depth=1 origin master

WORKDIR ./video_server

#Install python dependencies
#RUN pip3 install --upgrade pip && pip3 install -r requirements.txt
RUN pip3 install -r requirements.txt

#Expose API ports to the outside
EXPOSE 8554
EXPOSE 8555
EXPOSE 8556

#Launch application
WORKDIR ./gstreamer/
CMD python3 rtsp_server_gstreamer.py  -config_path gserver.conf & python3 rtsp_server_gstreamer.py  -config_path gserver2.conf & python3 rtsp_server_gstreamer.py  -config_path gserver3.conf &
