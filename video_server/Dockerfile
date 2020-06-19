FROM python

USER root

RUN rm /bin/sh && ln -s /bin/bash /bin/sh

#RUN apt-get clean && apt-get update && apt-get install -y sudo gstreamer1.0-plugins-base gstreamer1.0-plugins-bad lsof gir1.2-gst-rtsp-server-1.0 python3 python3-pip
RUN apt-get update && apt-get install -y sudo gstreamer1.0-plugins-base gstreamer1.0-plugins-bad lsof gir1.2-gst-rtsp-server-1.0


#Install python dependencies

COPY ./video_server/requirements.txt .

#RUN pip3 install --upgrade pip && pip3 install -r requirements.txt
RUN pip3 install -r requirements.txt

COPY ./video_server/. .

#Expose API ports to the outside
EXPOSE 8554
EXPOSE 8555
EXPOSE 8556

#Launch application
WORKDIR ./video_server/gstreamer/
CMD python3 rtsp_server_gstreamer.py  -config_path gserver.conf & python3 rtsp_server_gstreamer.py  -config_path gserver2.conf & python3 rtsp_server_gstreamer.py  -config_path gserver3.conf &
