FROM openvino/ubuntu18_runtime:2019_R3.1

USER root

RUN rm /bin/sh && ln -s /bin/bash /bin/sh


RUN apt-get update && apt-get install -y python3-dev libsm6 libxext6 libxrender-dev gstreamer1.0-plugins-base gstreamer1.0-plugins-bad gstreamer1.0-libav python3-pip libzmq3-dev libkrb5-dev ffmpeg lsof python3 wget

RUN pip3 install wheel
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

RUN wget https://download.01.org/opencv/2019/open_model_zoo/R1/models_bin/person-detection-retail-0013/FP32/person-detection-retail-0013.bin -O /home/person-detection-retail-0013.bin
RUN wget https://download.01.org/opencv/2019/open_model_zoo/R1/models_bin/person-detection-retail-0013/FP32/person-detection-retail-0013.xml -O /home/person-detection-retail-0013.xml

#Launch application
RUN chmod +x ./run_3_models.sh

ENTRYPOINT ["./run_3_models.sh"]
