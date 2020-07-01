"""People Counter."""
"""
 Copyright (c) 2018 Intel Corporation.
 Permission is hereby granted, free of charge, to any person obtaining
 a copy of this software and associated documentation files (the
 "Software"), to deal in the Software without restriction, including
 without limitation the rights to use, copy, modify, merge, publish,
 distribute, sublicense, and/or sell copies of the Software, and to
 permit person to whom the Software is furnished to do so, subject to
 the following conditions:
 The above copyright notice and this permission notice shall be
 included in all copies or substantial portions of the Software.
 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
 LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
 OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
 WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""


import os
import sys
import time
import socket
import json
import cv2

import logging as log
import paho.mqtt.client as mqtt

from argparse import ArgumentParser
from inference import Network

#os.environ["OPENCV_VIDEOIO_DEBUG"] = "1"
os.environ["GST_DEBUG"] = "2"

# MQTT server environment variables
MQTT_HOST = "0.0.0.0"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 60



def build_argparser():
    """
    Parse command line arguments.

    :return: command line arguments
    """
    parser = ArgumentParser()
    parser.add_argument("-m", "--model", required=True, type=str,
                        help="Path to an xml file with a trained model.")
    parser.add_argument("-i", "--input", required=True, type=str,
                        help="Path to image or video file")
    parser.add_argument("-o", "--output", required=True, type=str,
                        help="Path to RTMP nginx sink")
    parser.add_argument("-f", "--fps", required=True, type=int,
                        help="Frames per second input source")
    parser.add_argument("-l", "--cpu_extension", required=False, type=str,
                        default=None,
                        help="MKLDNN (CPU)-targeted custom layers."
                             "Absolute path to a shared library with the"
                             "kernels impl.")
    parser.add_argument("-d", "--device", type=str, default="CPU",
                        help="Specify the target device to infer on: "
                             "CPU, GPU, FPGA or MYRIAD is acceptable. Sample "
                             "will look for a suitable plugin for device "
                             "specified (CPU by default)")
    parser.add_argument("-pt", "--prob_threshold", type=float, default=0.5,
                        help="Probability threshold for detections filtering"
                        "(0.5 by default)")
    parser.add_argument("-pc", "--perf_counts", type=str, default=False,
                        help="Print performance counters")
    return parser


def performance_counts(perf_count):
    """
    print information about layers of the model.

    :param perf_count: Dictionary consists of status of the layers.
    :return: None
    """
    print("{:<70} {:<15} {:<15} {:<15} {:<10}".format('name', 'layer_type',
                                                      'exec_type', 'status',
                                                      'real_time, us'))
    for layer, stats in perf_count.items():
        print("{:<70} {:<15} {:<15} {:<15} {:<10}".format(layer,
                                                          stats['layer_type'],
                                                          stats['exec_type'],
                                                          stats['status'],
                                                          stats['real_time']))


def ssd_out(frame, result):
    """
    Parse SSD output.

    :param frame: frame from camera/video
    :param result: list contains the data to parse ssd
    :return: person count and frame
    """
    current_count = 0
    for obj in result[0][0]:
        # Draw bounding box for object when it's probability is more than
        #  the specified threshold
        if obj[2] > prob_threshold:
            xmin = int(obj[3] * initial_w)
            ymin = int(obj[4] * initial_h)
            xmax = int(obj[5] * initial_w)
            ymax = int(obj[6] * initial_h)
            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 55, 255), 2)
            current_count = current_count + 1
    return frame, current_count


def main():
    """
    Load the network and parse the SSD output.

    :return: None
    """
    # Connect to the MQTT server
    client = mqtt.Client()
    client.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)

    args = build_argparser().parse_args()

    # Flag for the input image
    single_image_mode = False

    cur_request_id = 0
    last_count = 0
    total_count = 0
    start_time = 0

    # Initialise the class
    infer_network = Network()
    # Load the network to IE plugin to get shape of input layer
    n, c, h, w = infer_network.load_model(args.model, args.device, 1, 1,
                                          cur_request_id, args.cpu_extension)[1]


    # Checks for input image
    if args.input.endswith('.jpg') or args.input.endswith('.bmp') :
        single_image_mode = True
        input_stream = args.input

    # Checks for video file
    else:
        input_stream = args.input
        #assert os.path.isfile(args.input), "Specified input file doesn't exist"

    if os.path.isfile(args.input):
        ##works for local file:
        gstreamer_pipeline = ('filesrc location = %s ! qtdemux ! h264parse ! avdec_h264 ! videoconvert ! appsink sync=false' % (input_stream))
        wk = 33
    else:
        #RTSP stream:
        gstreamer_pipeline = ('rtspsrc location=%s ! queue ! rtph264depay ! h264parse config-interval=-1 ! avdec_h264 ! videoconvert ! appsink sync=false' % (input_stream))
        wk = 1
    
    cap = cv2.VideoCapture(gstreamer_pipeline, cv2.CAP_GSTREAMER)

    output_stream = args.output
    #gstreamer_out = ('appsrc ! h264parse config-interval=-1 ! flvmux streamable=true ! rtmpsink location=%s sync=false'  % (output_stream))
    #gstreamer_out = ("appsrc ! videoconvert ! x264enc tune=zerolatency threads=1 speed-preset=superfast ! flvmux streamable=true ! rtmpsink location='%s live=1'"  % (output_stream))
    gstreamer_out = ("appsrc ! videoconvert ! x264enc tune=zerolatency bitrate=5000 tune=zerolatency speed-preset=ultrafast ! flvmux streamable=true ! rtmpsink location='%s live=1'"  % (output_stream))
    
    #gstreamer_out = ('appsrc ! videoconvert ! video/x-raw,framerate=25/1 ! videoconvert ! x264enc tune="zerolatency" threads=1  ! h264parse ! flvmux streamable=true ! rtmpsink location=%s async=false'  % (output_stream))
    #gstreamer_out = ('appsrc ! queue ! videoconvert ! video/x-raw ! x264enc ! h264parse ! rtmpsink location=%s async=false'  % (output_stream))
    #gstreamer_out = ("appsrc ! 'video/x-raw, width=1920, height=1080, framerate=25/1'  ! videoconvert ! x264enc bframes=0 b-adapt=false speed-preset=1 tune=0x00000004 ! h264parse ! flvmux ! rtmpsink location='%s live=1' async=false"  % (output_stream))
    
    #gstreamer_out = ("appsrc ! 'video/x-raw, width=1920, height=1080, framerate=25/1' ! videoconvert ! h264parse ! flvmux streamable=true ! rtmpsink location=%s" % (output_stream))

    #gstreamer_out = ("appsrc ! h264parse ! flvmux streamable=true ! rtmpsink location='%s'" % (output_stream))

    #fcc = cv2.VideoWriter_fourcc(*'X264')
    fps = int(args.fps)
    out = cv2.VideoWriter(gstreamer_out, -1, fps, (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))), True)

    if not cap.isOpened():
        log.error("ERROR! Unable to open video source")
    global initial_w, initial_h, prob_threshold
    prob_threshold = args.prob_threshold
    initial_w = cap.get(3)
    initial_h = cap.get(4)
    while cap.isOpened():
        flag, frame = cap.read()
        if not flag:
            break
        key_pressed = cv2.waitKey(wk)
        # Start async inference
        image = cv2.resize(frame, (w, h))
        # Change data layout from HWC to CHW
        image = image.transpose((2, 0, 1))
        image = image.reshape((n, c, h, w))
        # Start asynchronous inference for specified request.
        inf_start = time.time()
        infer_network.exec_net(cur_request_id, image)
        # Wait for the result
        if infer_network.wait(cur_request_id) == 0:
            det_time = time.time() - inf_start
            # Results of the output layer of the network
            result = infer_network.get_output(cur_request_id)
            if args.perf_counts:
                perf_count = infer_network.performance_counter(cur_request_id)
                performance_counts(perf_count)

            frame, current_count = ssd_out(frame, result)

            resol = str(int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))) + 'x' + str(int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

            client.publish("video/fps", fps)
            client.publish("video/resolution", resol)
      
            client.publish("person", current_count)      
            client.publish("person/inference", "{:.3f}ms"\
                                            .format(det_time * 1000)) 



            last_count = current_count

            if key_pressed == 27:
                break

        # Send frame to the ffmpeg server
        #sys.stdout.buffer.write(frame)
        out.write(frame)

        #print('Count:' + str(current_count))
        #print('FPS:' + str(int(cap.get(cv2.CAP_PROP_FPS))))
        #print('Resol:' + str(resol))
        #sys.stdout.flush()

        if single_image_mode:
            cv2.imwrite('output_image.jpg', frame)
    cap.release()
    cv2.destroyAllWindows()
    client.disconnect()
    infer_network.clean()


if __name__ == '__main__':
    main()
    exit(0)
