#! /usr/bin/env python3

# make empty textfiles if not in given folder

import os
import glob

dataset_dir = '/home/zachary/UVI_Training/data/yolo_seg/dataset_20230606'

# original label directory
label_dir_in = os.path.join(dataset_dir, 'labels_combined_2')
import shutil


# output label directory
label_dir_out = os.path.join(dataset_dir, 'labels_combined_with_empty_2')
os.makedirs(label_dir_out, exist_ok=True)
image_dir = os.path.join(dataset_dir, 'images')


# copy over labels from original directory
label_list_orig = sorted(glob.glob(os.path.join(label_dir_in, '*.txt')))
for lbl_path in label_list_orig:
    shutil.copy(lbl_path,os.path.join(label_dir_out, os.path.basename(lbl_path)))
print('copied over files')
# NOTE: copying instead of symlinks, so be careful about disk space/usage


image_list = sorted(glob.glob(os.path.join(image_dir, '*.jpg')))
label_list = sorted(glob.glob(os.path.join(label_dir_out, '*.txt')))

# import code
# code.interact(local=dict(globals(), **locals()))

for i, image_path in enumerate(image_list):
    print(f'{i}/{len(image_list)}')
    
    image_name = os.path.basename(image_path)
    expected_label_name = image_name.rsplit('.')[0] + '.txt'
    expected_label_path = os.path.join(label_dir_out, expected_label_name)
    
    if not os.path.isfile(expected_label_path):
        # if file doesn't exist, create an empty text file
        with open(expected_label_path, 'w'):
            pass
        

print('done')