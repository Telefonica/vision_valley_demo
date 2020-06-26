FROM python

USER root

RUN rm /bin/sh && ln -s /bin/bash /bin/sh

#RUN apt-get clean && apt-get update && apt-get install -y sudo gstreamer1.0-plugins-base gstreamer1.0-plugins-bad lsof gir1.2-gst-rtsp-server-1.0 python3 python3-pip
RUN apt-get update && apt-get install -y sudo libgstreamer-plugins-good1.0-0 libgstreamer-plugins-good1.0-dev gstreamer1.0-plugins-good gir1.2-gst-rtsp-server-1.0 pkg-config libcairo2-dev gcc python3-dev libgirepository1.0-dev libgstreamer-plugins-bad1.0-0 libgstreamer-plugins-base1.0-0 libgstreamer-plugins-base1.0-dev libgstreamer1.0 libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev libgtk-3-dev


#Install python dependencies

COPY ./requirements.txt .

#RUN pip3 install --upgrade pip && pip3 install -r requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

#Expose API ports to the outside
EXPOSE 8554
EXPOSE 8555
EXPOSE 8556

WORKDIR ./gstreamer/

RUN chmod +x ./launch_3_streams.sh

#Launch application
ENTRYPOINT ["./launch_3_streams.sh"]
