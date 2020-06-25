FROM openvino/ubuntu18_runtime:2019_R3.1

USER root

RUN rm /bin/sh && ln -s /bin/bash /bin/sh

RUN apt-get update && apt-get install -y gstreamer1.0-plugins-base gstreamer1.0-plugins-bad gstreamer1.0-libav python3-pip libzmq3-dev libkrb5-dev ffmpeg lsof python3 

#Install python dependencies

COPY ./requirements.txt .

#RUN pip3 install --upgrade pip && pip3 install -r requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

#Expose API ports to the outside
EXPOSE 3000
EXPOSE 1883
EXPOSE 8090
EXPOSE 8554
EXPOSE 8555
EXPOSE 8556

#Model downloader
CMD cd /opt/intel/openvino/deployment_tools/tools/model_downloader/ && python3 downloader.py --name person-detection-retail-0013

#Launch application
RUN source /opt/intel/openvino/bin/setupvars.sh 

RUN chmod +x ./run_3_models.sh

ENTRYPOINT ["./run_3_models.sh"]
