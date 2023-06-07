#! /usr/bin/env python3

"""Plotter.py
A collection of common plotting functions used by the Detector, Tracker and Classifier
Dorian Tsai & Java Terry
"""

import os
import matplotlib.pyplot as plt
import numpy as np
import cv2 as cv


class Plotter:
    
    # RGB
    White = (250, 250, 250)
    Blue = (57,127,252)
    # Purple = (198,115,255)
    Green = (0,200,120)
    BrightGreen = (0, 255, 120)
    Black = (0,0,0)
    Red = (250,0,0)
    Yellow = (205,195,2)
    Purple = (176, 18, 204)
    Orange = (255, 165, 0)
    
    
    def __init__(self, 
                 width: int, 
                 height: int):
        self.image_width = width
        self.image_height = height
        
        self.font = cv.FONT_HERSHEY_SIMPLEX
        self.img_size = 640
        
        
    def groundtruth2box(self, 
                 textfile,
                 image,
                 colour=Red,
                 line_thickness=8,
                 font_thickness=4):
        '''
        takes a groundtruth text file with xy cords and plots a boxes
        on the linked image in specified colour
        '''
        
        imgw, imgh = image.shape[1], image.shape[0]
        x1,y1,x2,y2,i = [],[],[],[],0
        with open(textfile) as f:
            for line in f:
                a,b,c,d,e = line.split()
                w = round(float(b)*imgw)
                h = round(float(c)*imgh)
                y1.append(h+round(float(e)*imgh/2))
                y2.append(h-round(float(d)*imgh/2))
                x1.append(w+round(float(d)*imgw/2))
                x2.append(w-round(float(d)*imgw/2))
                cv.rectangle(image, (x1[i], y1[i]), (x2[i], y2[i]), colour, line_thickness)
                
                # plot text
                #change results depending on class
                cls = int(a)
                if cls == 0: colour, text = self.Red, 'GT: Agaricia' #normal turtle = 0
                elif cls == 1: colour, text = self.Purple, 'GT: Orbicella' #painted turtle = 1
                else: colour, text = self.Black, 'Unknown class number' #something weird is happening
                
                self.boxwithtext(image, int(x2[i]), int(y2[i] + imgh*0.015), text, colour, font_thickness)
                i += 1
                
                
    def predarray2box(self, 
                      predarray,
                      img, 
                      line_thickness=4):
        '''
        from a prediction array draws boxes around the object as well as labeling
        the boxes on the linked in specified colour
        '''
        for p in predarray:
            # if i>4:
            #     break
            x1, y1, x2, y2 = p[0:4].tolist()
            conf, cls = p[4], int(p[5])
            #change results depending on class
            if cls == 0: colour, text = self.Yellow, 'Agaricia' #normal turtle = 0
            elif cls == 1: colour, text = self.Orange, 'Orbicella' #painted turtle = 1
            else: colour, text = self.Black, 'Unknown class number' #something weird is happening
            
            conf_str = format(conf*100.0, '.0f')
            detect_str = '{}: {}'.format(text, conf_str)
            
            #print(x1)
            # i += 1
            #plotting
            cv.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), 
                    colour, line_thickness) #box around tutle
            
            imgw, imgh = img.shape[1], img.shape[0]
            self.boxwithtext(img, int(x1), int(y1 + 0.0025*imgh), detect_str, colour, line_thickness)
    
    
    def boxwithtext(self, img, x1, y1, text, colour, thickness=4):
        '''
        Given a img, starting x,y cords, text and colour, create a filled in box of specified colour
        and write the text
        '''
        #font_scale = 0.5 # 
        font_scale = max(1,0.000005*max(img.shape))
        p = 5 #padding
        text_size, _ = cv.getTextSize(text, self.font, font_scale, thickness)
        cv.rectangle(img, (x1-p, y1-p), (x1+text_size[0]+p, y1-text_size[1]-(2*p)), colour, -1)
        cv.putText(img, text, (x1,int(y1-p*2)), self.font, font_scale, self.White, thickness)
        
        
    def save_image(self, image, save_path, color_format='RGB'):
        """save_image

        Args:
            image (_type_): _description_
            save_path (_type_): _description_
        """
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        if color_format == 'RGB':
            image = cv.cvtColor(image, cv.COLOR_RGB2BGR)
        cv.imwrite(save_path, image)