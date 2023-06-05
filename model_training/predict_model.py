#! /usr/bin/env/python3

"""
predict_model.py

Predict using trained model
"""

from ultralytics import YOLO
import os
import glob

# load model
print('loading model')
model_path = '/home/zachary/UVI_Training/code/uvi_corals/model_training/runs/segment/train5/weights/last.pt'
model = YOLO(model_path)

print('predicting on images')
img_dir = '/home/zachary/UVI_Training/data/yolo_seg/train/images'
img_list = sorted(glob.glob(os.path.join(img_dir, '*.jpg')))
img_list = img_list[0:100]
results = model(img_list, save=True, save_txt=True, save_conf=True, boxes=True)

# for interactive debugger in terminal:
import code
code.interact(local=dict(globals(), **locals()))