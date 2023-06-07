#! /usr/bin/env/python3

"""
aggregate_annotations.py

Look into annotations files, convert all of a certain class to a certain higher class
1) All Agaricia's to agaricia
2) all orbicella's to orbicella
3) remove all otherds
"""

import glob
import os

# Input class denomination:
# names:
#     0: Agaricia
#     1: Orbicella
#     2: Montastrea cavernosa
#     3: Sidastrea siderea
#     4: Unkown Coral
#     5: Solanastrea intersepta
#     6: Colpophyllia natans
#     7: Porites porites
#     8: Porites asteroides
#     9: Pseudodiploria strigosa
#     10: Millepora alcicornis
#     11: Mycetophyllia sp.
#     12: Meandrina meandrites
    
# run through all yolo text files and remove all rows that are greater than X

def keep_classes(input_file, output_file, keep_classes):
    # read in file
    with open(input_file, 'r') as file:
        lines = file.readlines()
        
    modified_lines = []
    for line in lines:
        columns = line.strip().split(' ')
        if columns[0] in keep_classes:
            modified_lines.append(' '.join(columns) + '\n')    
    
    # write modified lines to output file
    with open(output_file, 'w') as file:
        file.writelines(modified_lines)
        
        
def remove_classes(lbl_dir, out_dir, classes_to_keep):
    # read in all label files

    lbl_files = sorted(glob.glob(os.path.join(lbl_dir, '*.txt')))


    os.makedirs(out_dir, exist_ok=True)

    # for each lbl_file
    # iterate through each line in the label file
    # for the first character, apply class_change
    


        
    # for each label file, remove_classes
    for i, lbl_path in enumerate(lbl_files):
        print(f'{i}/{len(lbl_files)}')
        
        out_file = os.path.join(out_dir, os.path.basename(lbl_path))
        keep_classes(lbl_path, out_file, classes_to_keep)
        
    print('done')


if __name__ == '__main__':
    
    lbl_dir = '/home/zachary/UVI_Training/data/yolo_seg/dataset_20230606/labels_combined'
    out_dir = '/home/zachary/UVI_Training/data/yolo_seg/dataset_20230606/labels_combined_2'
    classes_to_keep = ['0', '1']
    
    remove_classes(lbl_dir, out_dir, classes_to_keep)
    
    # # debug
    import code
    code.interact(local=dict(globals(), **locals()))