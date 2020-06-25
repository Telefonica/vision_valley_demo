#!/bin/bash

python3 main.py -i rtsp://127.0.0.1:8554/video -o rtmp://localhost/show/stream -f 25 -m /opt/intel/openvino/deployment_tools/tools/model_downloader/Retail/object_detection/pedestrian/rmnet_ssd/0013/dldt/person-detection-retail-0013.xml -l /opt/intel/openvino/deployment_tools/inference_engine/lib/intel64/libcpu_extension_sse4.so -d CPU -pt 0.6 & \
python3 tensorflow_infer.py --img-mode 0 --video-path rtsp://127.0.0.1:8554/video -o rtmp://localhost/show/maskstream -f 30 & \
python3 social_distancing_analyser.py -i rtsp://127.0.0.1:8554/video -m /opt/intel/openvino/deployment_tools/tools/model_downloader/Retail/object_detection/pedestrian/rmnet_ssd/0013/dldt/person-detection-retail-0013.xml -l /opt/intel/openvino/deployment_tools/inference_engine/lib/intel64/libcpu_extension_sse4.so -d CPU -pt 0.6 -o rtmp://localhost/show/diststream -f 25 &&

echo "Models running"