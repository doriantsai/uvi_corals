#! /usr/bin/env python3

"""
annotation_pipeline.py

String together annotation process from COCO labels exported from CVAT to YOLO bbox labels and sorted into train/test/val folders
"""

import os
import glob
import shutil

import general_json2yolo
import aggregate_annotations
import remove_classes
import make_empty_textfiles
import split_data

## image folders
# img_dir = []
img_dir = '/home/zachary/UVI_Training/data/images'
lbl_dir = '/home/zachary/UVI_Training/data/labels'


## ======= convert COCO to YOLO BBOX ================

ann_list = []
out_list = []

ann_list.append(os.path.join(lbl_dir,'TCRMP20180511_clip_HBE_COCO/'))
out_list.append(os.path.join(lbl_dir,'TCRMP20180511_clip_HBE_YOLO_BBOX'))

ann_list.append(os.path.join(lbl_dir,'TCRMP20180227_clip_CBD_COCO/'))
out_list.append(os.path.join(lbl_dir,'TCRMP20180227_clip_CBD_YOLO_BBOX'))

ann_list.append(os.path.join(lbl_dir,'TCRMP20180302_clip_LBH_COCO/'))
out_list.append(os.path.join(lbl_dir,'TCRMP20180302_clip_LBH_YOLO_BBOX'))

ann_list.append(os.path.join(lbl_dir,'TCRMP20180605_clip_MRS_COCO/'))
out_list.append(os.path.join(lbl_dir,'TCRMP20180605_clip_MRS_YOLO_BBOX'))

ann_list.append(os.path.join(lbl_dir,'TCRMP20181104_clip_SRD_COCO/'))
out_list.append(os.path.join(lbl_dir,'TCRMP20181104_clip_SRD_YOLO_BBOX'))

ann_list.append(os.path.join(lbl_dir,'TCRMP20181212_clip_GBF_COCO/'))
out_list.append(os.path.join(lbl_dir,'TCRMP20181212_clip_GBF_YOLO_BBOX'))

ann_list.append(os.path.join(lbl_dir,'TCRMP20221021_clip_LBP_COCO/'))
out_list.append(os.path.join(lbl_dir,'TCRMP20221021_clip_LBP_YOLO_BBOX'))

ann_list.append(os.path.join(lbl_dir,'TCRMP20180228_clip_SRD_COCO/'))
out_list.append(os.path.join(lbl_dir,'TCRMP20180228_clip_SRD_YOLO_BBOX'))

ann_list.append(os.path.join(lbl_dir,'TCRMP20180522_clip_GBF_COCO/'))
out_list.append(os.path.join(lbl_dir,'TCRMP20180522_clip_GBF_YOLO_BBOX'))

for i, ann_file in enumerate(ann_list):
    general_json2yolo.convert_coco_json(ann_file,  # directory with *.json
                                        use_segments=False, # true segments, false for bbox
                                        cls91to80=False,
                                        out_dir=out_list[i])
    


## ============= grab all images and annotations and put them into the same folder ===============

print('copy over all images and text files')

dataset_dir = '/home/zachary/UVI_Training/data/yolo_box/blur'
dataset_img_dir = os.path.join(dataset_dir, 'images')
dataset_lbl_dir = os.path.join(dataset_dir, 'labels')
os.makedirs(dataset_img_dir, exist_ok=True)
os.makedirs(dataset_lbl_dir, exist_ok=True)
    
# NOTE: copying over image files, not using symlinks, so be careful wrt storage
# actually, we can just recursively grab all the images in the folders here
img_list = sorted(glob.glob(os.path.join(img_dir, '**/*.jpg'), recursive=True))
for img_name in img_list:
    shutil.copy(img_name, os.path.join(dataset_img_dir, os.path.basename(img_name)))

txt_list = sorted(glob.glob(os.path.join(lbl_dir, '*BBOX/*/*/*.txt'), recursive=True))
for txt_name in txt_list:
    shutil.copy(txt_name, os.path.join(dataset_lbl_dir, os.path.basename(txt_name)))
    

## =========== aggregate annotations =================== 

class_change = {
        '0': '0', # Agaricia lamarki -> Agaricia
        '1': '0', # Agaricia undata -> Agaricia
        '2': '0', # Agaricia agaricites -> Agaricia
        '3': '0', # Agaricia fragilis -> Agaricia
        '4': '2', # Montastrea cavernosa -> same
        '5': '0', # Agaricia grahamae -> Agaricia
        '6': '3', # Sidastrea siderea -> same
        '7': '4', # Unknown coral -> same
        '8': '1', # Orbicella anularis -> Orbicella
        '9': '1', # Orbicella franksi -> Orbicella
        '10': '5', # Solanastrea intersepta -> same
        '11': '6', # Colpophyllia natans -> same
        '12': '1', # Orbicella sp. -> Orbicella
        '13': '7', # Porites porites -> same
        '14': '8', # Porites asteroides -> same
        '15': '9', # Pseudodiplora strigosa -> same
        '16': '10', # Millepora alcicornis -> same
        '17': '0', # Agaricia sp. -> Agaricia
        '18': '11', # Mycetophyllia sp. -> same
        '19': '12'  # Meandrina meandrites -> same
    }
aggregate_annotations.aggregate_annotations(lbl_dir=dataset_lbl_dir,
                                            out_dir=dataset_lbl_dir,
                                            class_change=class_change)


## =========== remove classes ======================

remove_classes.remove_classes(lbl_dir=dataset_lbl_dir,
                              out_dir=dataset_lbl_dir,
                              classes_to_keep=['0'])


## ============ make empty text files =================

make_empty_textfiles.make_empty_textfiles(dataset_lbl_dir, dataset_lbl_dir, dataset_img_dir)

## ============= blur images =======================

#for i, img_name in enumerate(img_list):
#    print(f'{i}/{len(img_list)}: {os.path.basename(img_name)}')
#    img_blur = cv.blur(img,(5,5))




## ============= split_data ========================

dataset_dir_out = '/home/zachary/UVI_Training/data/yolo_box/dataset_20230608_agaricia'
train_ratio = 0.85
val_ratio = 0.14
test_ratio = 0.01
split_data.split_data(dataset_img_dir, dataset_lbl_dir, dataset_dir_out, train_ratio, val_ratio, test_ratio)

import code
code.interact(local=dict(globals(), **locals()))