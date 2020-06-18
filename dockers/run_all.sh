#!/bin/bash

docker build -t "cvdemo_ui_all" --build-arg SSH_PRIVATE_KEY="$(cat ~/.ssh/id_rsa)" --build-arg SSH_PUBLIC_KEY="$(cat ~/.ssh/id_rsa.pub)" ./ui

docker run -p 8080:8080 -p 3000:3000 -p 8090:8090 cvdemo_ui_all

echo "UI up"

docker build -t "cvdemo_video_all" --build-arg SSH_PRIVATE_KEY="$(cat ~/.ssh/id_rsa)" --build-arg SSH_PUBLIC_KEY="$(cat ~/.ssh/id_rsa.pub)" ./video_server

docker run -p 8554:8554 -p 8555:8555 -p 8556:8556 cvdemo_video_all

echo "Video server up"


docker build -t "cvdemo_mqtt_all" --build-arg SSH_PRIVATE_KEY="$(cat ~/.ssh/id_rsa)" --build-arg SSH_PUBLIC_KEY="$(cat ~/.ssh/id_rsa.pub)" ./mqtt_broker

docker run -p 1883:1883 -p 3000:3000 cvdemo_mqtt_all

echo "MQTT broker up"


docker build -t "cvdemo_streaming_all" --build-arg SSH_PRIVATE_KEY="$(cat ~/.ssh/id_rsa)" --build-arg SSH_PUBLIC_KEY="$(cat ~/.ssh/id_rsa.pub)" ./streaming_server

docker run -p 8090:8090 cvdemo_streaming_all

echo "Streaming server up"


docker build -t "cvdemo_server_all" --build-arg SSH_PRIVATE_KEY="$(cat ~/.ssh/id_rsa)" --build-arg SSH_PUBLIC_KEY="$(cat ~/.ssh/id_rsa.pub)" .

docker run -p 1883:1883 -p 3000:3000 -p 8554:8554 -p 8555:8555 -p 8556:8556 -p 8080:8080 cvdemo_server_all

echo "Backend up"
