#! /usr/bin/env/python3

"""
predict_model.py

Predict using trained model
"""

from ultralytics import YOLO
import os
import glob
import cv2 as cv
import torch

# load model
print('loading model')
model_path = '/home/zachary/UVI_Training/code/uvi_corals/model_training/runs/segment/train9/weights/last.pt'
model = YOLO(model_path)


device = torch.device('cuda')

print('predicting on images')
img_dir = '/home/zachary/UVI_Training/data/yolo_seg/train/images'
img_list = sorted(glob.glob(os.path.join(img_dir, '*.jpg')))
img_list = img_list[0:100]
results = model(img_list, 
                save=True, 
                save_txt=True, 
                save_conf=True, 
                boxes=True,
                conf=0.1, # intentionally very low for debugging purposes
                agnostic_nms=True,
                device=device)

# res = model(img)
# res_plotted = res[0].plot()
# cv.imshow("result", res_plotted)

# for interactive debugger in terminal:
import code
code.interact(local=dict(globals(), **locals()))