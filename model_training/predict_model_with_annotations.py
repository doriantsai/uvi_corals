#! /usr/bin/env/python3

"""
predict_model.py

Predict using trained model on images that have corresponding labels/groundtruth annotations
"""

from ultralytics import YOLO
import os
import glob
import cv2 as cv
# import torch
import matplotlib.pyplot as plt
import numpy as np

from Plotter import Plotter as pplot


# def pred2array(self, pred):
#         """pred2array
#         take detector model predictions and convert them to an array

#         Args:
#             results (list?): detector results, raw

#         Returns:
#             np_array: array = xmin, xmax, ymin, ymax, confidence, class
#         """           
#         # pred = results.pred[0]
#         # pred = results.keypoints
#         predarray = []
#         if pred is not None:    
#             for i in range(len(pred)):
#                 row = []
#                 for j in range(6):
#                     row.append(pred[i,j].item())
#                 predarray += (row)    
#             predarray = np.array(predarray)
#             predarray = predarray.reshape(len(pred),6)
#         return predarray
    
# load model
print('loading model')
# location of model
model_path = '/home/dorian/Code/uvi_corals/model_training/weights/yolov8x_box_100epochs_2class_last.pt'

# output directory (for plots/detections)
out_dir = '/home/dorian/Data/uvi/yolo_box/dataset_20230607/predict'
os.makedirs(out_dir, exist_ok=True)

# image directory
img_dir = '/home/dorian/Data/uvi/yolo_box/dataset_20230607/test/images'

# label directory
lbl_dir = '/home/dorian/Data/uvi/yolo_box/dataset_20230607/test/labels'



# load custom model (YOLOv8)
model = YOLO(model_path)

print('predicting on images with annotations')
img_list = sorted(glob.glob(os.path.join(img_dir, '*.jpg')))
lbl_list = sorted(glob.glob(os.path.join(lbl_dir, '*.txt')))

# shorten for debugging purposes:
img_list = img_list[0:5]
lbl_list = lbl_list[0:5]

# TODO ensure that custom_yaml file has validation set to relevant folder
# data_file = '/home/dorian/Code/uvi_corals/model_training/uvi_custom_val.yaml'
# model.val(data_file)

# init plotter:



for i, img_name in enumerate(img_list):
    print(f'{i}/{len(img_list)}: {os.path.basename(img_name)}')
    
    # model inference
    results = model(img_name, 
                    save=True, 
                    save_txt=True, 
                    save_conf=True, 
                    boxes=True,
                    conf=0.3, # intentionally very low for debugging purposes
                    agnostic_nms=True)

    # plot just the results via yolo
    # res_plotted = results[0].plot()
    # res_rgb = cv.cvtColor(res_plotted, cv.COLOR_BGR2RGB)    
    
    # save image
    # img_save_name = os.path.basename(img_name).rsplit('.')[0] + '_box.jpg'
    # plt.imsave(os.path.join(out_dir, img_save_name), res_rgb)
    # plt.show()
    

   
    # TODO make boxes 2D numpy array, x1 y1 x2 y2 conf class
    # print(boxes.xyxy)

    # open image
    img = cv.imread(img_name)
    img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    
    image_width, image_height = img.shape[1], img.shape[0]
    PlotCorals = pplot(image_width, image_height)
    
    # convert boxes to numpy array
    boxes = results[0].boxes.data
    boxes = boxes.cpu().numpy()
    # predictions = pred2array(boxes)
    
    # draw annotations to image
    PlotCorals.groundtruth2box(lbl_list[i], img)
    
    # draw detections/predictions to image
    PlotCorals.predarray2box(boxes, img)
    
    # save image
    save_img_name = os.path.join(out_dir, os.path.basename(img_name).rsplit('.')[0] + '_box.jpg')
    PlotCorals.save_image(img, save_img_name, 'RGB')
    
    
    
    


# for interactive debugger in terminal:
#import code
#code.interact(local=dict(globals(), **locals()))