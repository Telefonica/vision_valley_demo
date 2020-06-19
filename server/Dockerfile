FROM openvino/ubuntu18_runtime:2019_R3.1

USER root

RUN rm /bin/sh && ln -s /bin/bash /bin/sh

RUN apt-get install -y sudo gstreamer1.0-plugins-base gstreamer1.0-plugins-bad gstreamer1.0-libav python3-pip libzmq3-dev libkrb5-dev ffmpeg lsof

#Install python dependencies

COPY ./server/requirements.txt .

#RUN pip3 install --upgrade pip && pip3 install -r requirements.txt
RUN pip3 install -r requirements.txt

COPY ./server/. .

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
WORKDIR ./server
CMD source /opt/intel/openvino/bin/setupvars.sh 

CMD python3 main.py -i rtsp://127.0.0.1:8554/video -o rtmp://localhost/show/stream -f 25 -m /opt/intel/openvino/deployment_tools/tools/model_downloader/Retail/object_detection/pedestrian/rmnet_ssd/0013/dldt/person-detection-retail-0013.xml -l /opt/intel/openvino/deployment_tools/inference_engine/lib/intel64/libcpu_extension_sse4.so -d CPU -pt 0.6 &
python3 tensorflow_infer.py --img-mode 0 --video-path rtsp://127.0.0.1:8554/video -o rtmp://localhost/show/maskstream -f 30 &
python3 social_distancing_analyser.py -i rtsp://127.0.0.1:8554/video -m /opt/intel/openvino/deployment_tools/tools/model_downloader/Retail/object_detection/pedestrian/rmnet_ssd/0013/dldt/person-detection-retail-0013.xml -l /opt/intel/openvino/deployment_tools/inference_engine/lib/intel64/libcpu_extension_sse4.so -d CPU -pt 0.6 -o rtmp://localhost/show/diststream -f 25 &

