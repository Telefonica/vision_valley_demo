#!/bin/bash
source /opt/intel/openvino/bin/setupvars.sh 


sleep 10
python3 main.py -i rtsp://127.0.0.1:8554/video_count -o rtmp://127.0.0.1:1935/show/stream -f 25 -m /home/person-detection-retail-0013.xml -l /opt/intel/openvino/deployment_tools/inference_engine/lib/intel64/libcpu_extension_sse4.so -d CPU -pt 0.6 & \
python3 tensorflow_infer.py -i rtsp://127.0.0.1:8556/video_mask -o rtmp://127.0.0.1:1935/maskshow/stream -f 30 & \
python3 social_distancing_analyser.py -i rtsp://127.0.0.1:8555/video -m /home/person-detection-retail-0013.xml -l /opt/intel/openvino/deployment_tools/inference_engine/lib/intel64/libcpu_extension_sse4.so -d CPU -pt 0.6 -o rtmp://127.0.0.1:1935/distshow/stream -f 25 &&

echo "Models running"

cd
