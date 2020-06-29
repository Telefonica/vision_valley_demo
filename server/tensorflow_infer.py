# -*- coding:utf-8 -*-
import cv2
import time
import argparse
import os
import sys
import socket
import json

import logging as log
import paho.mqtt.client as mqtt

os.environ["OPENCV_VIDEOIO_DEBUG"] = "1"
os.environ["GST_DEBUG"] = "2"

# MQTT server environment variables
MQTT_HOST = "0.0.0.0"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 60

import numpy as np
from PIL import Image
#from keras.models import model_from_json
from utils.anchor_generator import generate_anchors
from utils.anchor_decode import decode_bbox
from utils.nms import single_class_non_max_suppression
from load_model.tensorflow_loader import load_tf_model, tf_inference

sess, graph = load_tf_model('models/face_mask_detection.pb')
# anchor configuration
feature_map_sizes = [[33, 33], [17, 17], [9, 9], [5, 5], [3, 3]]
anchor_sizes = [[0.04, 0.056], [0.08, 0.11], [0.16, 0.22], [0.32, 0.45], [0.64, 0.72]]
anchor_ratios = [[1, 0.62, 0.42]] * 5

# generate anchors
anchors = generate_anchors(feature_map_sizes, anchor_sizes, anchor_ratios)

# for inference , the batch size is 1, the model output shape is [1, N, 4],
# so we expand dim for anchors to [1, anchor_num, 4]
anchors_exp = np.expand_dims(anchors, axis=0)

id2class = {0: 'Mask', 1: 'NoMask'}


def inference(image,
              conf_thresh=0.5,
              iou_thresh=0.4,
              target_shape=(160, 160),
              draw_result=True,
              show_result=False
              ):
    '''
    Main function of detection inference
    :param image: 3D numpy array of image
    :param conf_thresh: the min threshold of classification probabity.
    :param iou_thresh: the IOU threshold of NMS
    :param target_shape: the model input size.
    :param draw_result: whether to daw bounding box to the image.
    :param show_result: whether to display the image.
    :return:
    '''
    # image = np.copy(image)
    output_info = []
    height, width, _ = image.shape
    image_resized = cv2.resize(image, target_shape)
    image_np = image_resized / 255.0 
    image_exp = np.expand_dims(image_np, axis=0)
    y_bboxes_output, y_cls_output = tf_inference(sess, graph, image_exp)

    # remove the batch dimension, for batch is always 1 for inference.
    y_bboxes = decode_bbox(anchors_exp, y_bboxes_output)[0]
    y_cls = y_cls_output[0]
    # To speed up, do single class NMS, not multiple classes NMS.
    bbox_max_scores = np.max(y_cls, axis=1)
    bbox_max_score_classes = np.argmax(y_cls, axis=1)

    # keep_idx is the alive bounding box after nms.
    keep_idxs = single_class_non_max_suppression(y_bboxes,
                                                 bbox_max_scores,
                                                 conf_thresh=conf_thresh,
                                                 iou_thresh=iou_thresh,
                                                 )
    current_count = 0
    mask_count = 0
    for idx in keep_idxs:
        conf = float(bbox_max_scores[idx])
        class_id = bbox_max_score_classes[idx]
        bbox = y_bboxes[idx]
        # clip the coordinate, avoid the value exceed the image boundary.
        xmin = max(0, int(bbox[0] * width))
        ymin = max(0, int(bbox[1] * height))
        xmax = min(int(bbox[2] * width), width)
        ymax = min(int(bbox[3] * height), height)

        if draw_result:
            if class_id == 0:
                color = (0, 255, 0)
            else:
                color = (255, 0, 0)
            cv2.rectangle(image, (xmin, ymin), (xmax, ymax), color, 2)
            cv2.putText(image, "%s: %.2f" % (id2class[class_id], conf), (xmin + 2, ymin - 2),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, color)
        output_info.append([class_id, conf, xmin, ymin, xmax, ymax])
        current_count = current_count + 1
        if class_id == 0:
            mask_count = mask_count +1

    if show_result:
        Image.fromarray(image).show()
    return output_info, current_count, mask_count


def run_on_video(video_path, output_stream, conf_thresh, fps):

    # Connect to the MQTT server
    client = mqtt.Client()
    client.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)

    if os.path.isfile(video_path):
        ##works for local file:
        gstreamer_pipeline = ('filesrc location = %s ! qtdemux ! h264parse ! avdec_h264 ! videoconvert ! appsink sync=false' % (video_path))
        wk = 33
    else:
        #RTSP stream:        
        #gstreamer_pipeline =('rtspsrc udp-buffer-size=655360 location=%s  ! queue max-size-time=100000000 ! rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! appsink sync=false async=false' % (video_path))
        #gstreamer_pipeline = ('rtspsrc location=%s protocols=1 udp-buffer-size=4294967295 latency=200 ! rtph264depay ! h264parse config-interval=-1 ! avdec_h264 ! videoconvert ! appsink sync=false' % (video_path))
        gstreamer_pipeline = ('rtspsrc location=%s udp-buffer-size=4294967295 latency=200 ! rtph264depay ! h264parse config-interval=-1 ! avdec_h264 ! videoconvert ! appsink sync=false' % (video_path))
        #gstreamer_pipeline = ('rtspsrc protocols=tcp location=%s latency=0 ! application/x-rtp, payload=96, bitrate=5000, encoding-name=H264 ! rtpjitterbuffer ! rtph264depay ! h264parse config-interval=-1 ! avdec_h264  ! videoconvert ! appsink sync=false' % (video_path))
        #gstreamer_pipeline = ('rtspsrc protocols=tcp location=%s ! rtpjitterbuffer max-rtcp-rtp-time-diff=100 drop-on-latency=true ts-offset=100 ! rtph264depay ! h264parse config-interval=-1 ! avdec_h264 output-corrupt=false skip-frame=2  ! videoconvert ! appsink sync=false' % (video_path))
        #gstreamer_pipeline = ('rtspsrc protocols=tcp location=%s ! application/x-rtp, media=video, encoding-name=H264 ! rtph264depay ! h264parse config-interval=-1 ! avdec_h264 output-corrupt=false skip-frame=2 max-threads=3 ! videoconvert ! appsink sync=false' % (video_path))
        wk = 1

    gstreamer_out = ("appsrc ! videoconvert ! x264enc bitrate=5000 tune=zerolatency speed-preset=ultrafast ! flvmux streamable=true ! rtmpsink location='%s live=1' sync=false"  % (output_stream))

    cap = cv2.VideoCapture(gstreamer_pipeline, cv2.CAP_GSTREAMER)
    fourcc = cv2.VideoWriter_fourcc(*'X264')
    out = cv2.VideoWriter(gstreamer_out, 0, fps, (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))), True)

    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    #fps = cap.get(cv2.CAP_PROP_FPS)
    #fourcc = cv2.VideoWriter_fourcc(*'XVID')
    total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    while cap.isOpened():
        flag, frame = cap.read()
        if not flag:
            break
        idx = 0
        #start_stamp = time.time()
        #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        read_frame_stamp = time.time()
        _, current_count, mask_count = inference(frame,
                conf_thresh,
                iou_thresh=0.5,
                target_shape=(260,260),
                draw_result=True,
                show_result=False)
        #cv2.imshow('image', frame[:, :, ::-1])
        cv2.waitKey(wk)
        inference_stamp = time.time()
        # writer.write(img_raw)
        # write_frame_stamp = time.time()
        idx += 1
        inference_time = inference_stamp - read_frame_stamp

        resol = str(int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))) + 'x' + str(int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

        client.publish("video_m/fps", str(int(cap.get(cv2.CAP_PROP_FPS))))
        client.publish("video_m/resolution", resol)
    
        client.publish("mask", mask_count)  
        client.publish("no_mask", current_count)    
        client.publish("mask/inference", "{:.3f}ms"\
                                        .format(inference_time * 1000))  
        out.write(frame)

    cap.release()
    cv2.destroyAllWindows()
    client.disconnect()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Face Mask Detection")
    parser.add_argument('-i', '--input', type=str, default='0', help='path to your video, `0` means to use camera.')    
    parser.add_argument("-o", "--output", required=True, type=str,
                        help="Path to RTMP nginx sink")
    parser.add_argument("-f", "--fps", required=True, type=int,
                        help="Frames per second input source")
    # parser.add_argument('--hdf5', type=str, help='keras hdf5 file')
    args = parser.parse_args()
    video_path = args.input
    output_video = args.output
    fps = args.fps
    if args.input == '0':
        video_path = 0
    run_on_video(video_path, output_video, 0.5, fps)
