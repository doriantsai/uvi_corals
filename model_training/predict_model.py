#! /usr/bin/env/python3

"""
predict_model.py

Predict using trained model
"""

from ultralytics import YOLO
import os
import glob
import cv2 as cv
# import torch
import matplotlib.pyplot as plt

# load model
print('loading model')
# location of model
model_path = '/home/zachary/UVI_Training/code/uvi_corals/model_training/runs/segment/train10/weights/best.pt'

# output directory (for plots/detections)
out_dir = '/home/zachary/UVI_Training/data/yolo_seg/segments_best'
os.makedirs(out_dir, exist_ok=True)

# image directory
img_dir = '/home/zachary/UVI_Training/data/yolo_seg/train/images'

# load custom model (YOLOv8)
model = YOLO(model_path)

print('predicting on images')
img_list = sorted(glob.glob(os.path.join(img_dir, '*.jpg')))
img_list = img_list[0:10]

for i, img_name in enumerate(img_list):
    print(f'{i}/{len(img_list)}: {os.path.basename(img_name)}')
    
    # model inference
    results = model(img_name, 
                    save=True, 
                    save_txt=True, 
                    save_conf=True, 
                    boxes=True,
                    conf=0.1, # intentionally very low for debugging purposes
                    agnostic_nms=False)

    # res = model(img)
    res_plotted = results[0].plot()
    # cv.imshow("result", res_plotted)
    
    res_rgb = cv.cvtColor(res_plotted, cv.COLOR_BGR2RGB)
    # plt.imshow(res_rgb)
    
    
    # save image
    img_save_name = os.path.basename(img_name).rsplit('.')[0] + '_seg.jpg'
    plt.imsave(os.path.join(out_dir, img_save_name), res_rgb)
    # plt.show()
    boxes = results[0].boxes
    print(boxes.xyxy)



# for interactive debugger in terminal:
#import code
#code.interact(local=dict(globals(), **locals()))