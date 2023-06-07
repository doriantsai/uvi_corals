# TODO


# given all images in img_dir
# copy over images to val/images
# copy corresponding label files over to val/labels (if they exist, might not due to negative images)


""" 
split_data.py
Splits data from training into val

authors: Java Terry & Dorian Tsai 
date: 2023 June 06
"""

import os
import glob
import shutil
import random

dataset_dir = '/home/zachary/UVI_Training/data/yolo_seg/dataset_20230606'

label_dir = os.path.join(dataset_dir, 'labels_combined_with_empty_2')
image_dir = os.path.join(dataset_dir, 'images')

train_dir = 'train'
val_dir = 'val'
test_dir = 'test'

out_dir = '/home/zachary/UVI_Training/data/yolo_seg/dataset_20230606/combined_classes_2'

train_ratio = 0.8
val_ratio = 0.1
test_ratio = 0.1

def check_ratio(test_ratio,train_ratio,valid_ratio):
    if(test_ratio>1 or test_ratio<0): ValueError(test_ratio,f'test_ratio must be > 1 and test_ratio < 0, test_ratio={test_ratio}')
    if(train_ratio>1 or train_ratio<0): ValueError(train_ratio,f'train_ratio must be > 1 and train_ratio < 0, train_ratio={train_ratio}')
    if(valid_ratio>1 or valid_ratio<0): ValueError(valid_ratio,f'valid_ratio must be > 1 and valid_ratio < 0, valid_ratio={valid_ratio}')
    if not((train_ratio+test_ratio+valid_ratio)==1): ValueError("sum of train/val/test ratio must equal 1")
    
check_ratio(test_ratio,train_ratio,val_ratio)


def clean_dirctory(savepath):
    if os.path.isdir(savepath):
        shutil.rmtree(savepath)
    os.makedirs(savepath, exist_ok=True)
    
clean_dirctory(out_dir)


imagelist = sorted(glob.glob(os.path.join(image_dir, '*.jpg')))
txtlist = sorted(glob.glob(os.path.join(label_dir, '*.txt')))

validimg = []
validtext = []
testimg = []
testtext = []

def seperate_files(number,imglist,textlist):
    for i in range(int(number)):
        r = random.randint(0, len(imglist))
        
        imglist.append(imagelist[r])
        imagelist.remove(imagelist[r])
        textlist.append(txtlist[r])
        txtlist.remove(txtlist[r])
        # text file might not exist, in which case
        # if 
        #     textlist.append(txtlist[r])
        #     txtlist.remove(txtlist[r])
        

#pick some random files
seperate_files(len(imagelist) * val_ratio, validimg, validtext) #get some valid images
seperate_files(len(imagelist) * test_ratio, testimg, testtext)

# function to preserve symlinks of src file, otherwise default to copy
def copy_link(src, dst):
    if os.path.islink(src):
        linkto = os.readlink(src)
        os.symlink(linkto, os.path.join(dst, os.path.basename(src)))
    else:
        shutil.copy(src, dst)
        
def move_file(filelist,savepath,second_path):
    output_path = os.path.join(savepath, second_path)
    clean_dirctory(output_path)
    os.makedirs(output_path, exist_ok=True)
    for i, item in enumerate(filelist):
        # shutil.move(item, os.path.join(savepath,second_path))
        copy_link(item, output_path)
        
move_file(imagelist,out_dir,'train/images')
move_file(validimg,out_dir,'valid/images')
move_file(testimg,out_dir,'test/images')

move_file(txtlist,out_dir,'train/labels')
move_file(validtext,out_dir,'valid/labels')
move_file(testtext,out_dir,'test/labels')

print('done')
# now move files for text by trying to find corresponding files from these image folders
# since text files might not exist due to negative examples

