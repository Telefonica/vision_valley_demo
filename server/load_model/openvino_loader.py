import sys
import os
import logging as log
import cv2
import numpy as np
from openvino.inference_engine import IECore

 

log.basicConfig(format="[ %(levelname)s ] %(message)s", level=log.INFO, stream=sys.stdout)

 

class InferenceManager():
       def __init__(self, model_xml, device="CPU"):
              self.ie = IECore()
              model_bin = os.path.splitext(model_xml)[0] + ".bin"
              self.net = self.ie.read_network(model=model_xml, weights=model_bin)
              assert (len(self.net.inputs.keys()) == 1 ), "Supports topologies only with 1 input"  
              self.input_blob = next(iter(self.net.inputs))
              for key in self.net.inputs:
                     self.net.inputs[key].precision = 'U8'
              log.info('Preparing output blobs')         
              for output_key in self.net.outputs:
                  if self.net.layers[output_key].type == "Concat":
                      output_name, output_info = output_key, self.net.outputs[output_key]
                      output_info.precision = "FP32"

 

              self.exec_net = self.ie.load_network(network=self.net, num_requests=2, device_name=device)
              self.n, self.c, self.h, self.w = self.net.inputs[self.input_blob].shape
              self.request_id = 0

 

       def infer(self, frame):
              in_frame = cv2.resize(frame, (self.w, self.h))
              in_frame = in_frame.transpose((2, 0, 1))  # Change data layout from HWC to CHW
              #in_frame = np.expand_dims(in_frame, axis=0)                                                         self.exec_net.start_async(request_id=self.request_id, inputs={self.input_blob:in_frame})

              if self.exec_net.requests[self.request_id].wait(-1) == 0:
                  res = self.exec_net.requests[self.request_id].outputs
                  keys = list(res.keys())
                  return res[keys[1]], res[keys[0]]

 

def load_openvino_model(model_path, device="CPU"):
    session = InferenceManager(model_path,device)
    return session

 

def openvino_inference(session, img_arr):  
    y_bboxes, y_scores = session.infer(img_arr)
    return y_bboxes, y_scores