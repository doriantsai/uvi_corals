#! /usr/bin/env/python3

"""
train_model.py

Take in data from set folders and YOLO format to train image segmentation model
Dorian Tsai
dorian.tsai@gmail.com
2023 June 05
"""

from ultralytics import YOLO
import os
import glob as glob

# load pre-trained model
model = YOLO('yolov8m-seg.pt')

# train model
print('Model Training:')
data_file = '/home/zachary/UVI_Training/code/uvi_corals/model_training/uvi_training_combined_2.yaml'
model.train(data=data_file, epochs=100, imgsz=640, batch=5)

print('Model Validation:')
metrics = model.val()

print('Model Inference:')
image_file = '/home/zachary/UVI_Training/data/images/TCRMP20180228_clip_SRD/TCRMP20180228_clip_SRD_T101.jpg'
results = model(image_file)
print(results)



# for interactive debugger in terminal:
import code
code.interact(local=dict(globals(), **locals()))