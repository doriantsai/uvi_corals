#! /usr/bin/env python3

import os
import glob
import cv2 as cv


def blur_images(img_dir, out_dir, kernel=(11,11)):
    os.makedirs(out_dir, exist_ok=True)
    img_list = sorted(glob.glob(os.path.join(img_dir, '*.jpg')))
    # iterate over images
    for i, img_name in enumerate(img_list):
        print(f'{i}/{len(img_list)}: {os.path.basename(img_name)}')

        img = cv.imread(img_name)
        img = cv.blur(img, kernel)

        save_img_name = os.path.join(out_dir, os.path.basename(img_name))

        cv.imwrite(save_img_name, img)

    print('done')

if __name__ == '__main__':

    # get list of images
    img_dir = '/home/zachary/UVI_Training/data/yolo_box/dataset_20230608_agaricia/test/images'
    # out/save directory
    out_dir = '/home/zachary/UVI_Training/data/yolo_box/dataset_20230608_agaricia/test/images_blur'
    blur_images(img_dir, out_dir)