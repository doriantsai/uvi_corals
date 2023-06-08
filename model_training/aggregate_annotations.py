#! /usr/bin/env/python3

"""
aggregate_annotations.py

Look into annotations files, convert all of a certain class to a certain higher class
1) All Agaricia's to agaricia
2) all orbicella's to orbicella
3) leave all others untouched
"""

import glob
import os


# read in all label files
# find all 0's, 1's, 2's, 3's, 17's

# Original class denomination: 
# names:
#   0: Agaricia lamarki
#   1: Agaricia undata
#   2: Agaricia agaricites
#   3: Agaricia fragilis
#   4: Montastrea cavernosa
#   5: Agaricia grahamae
#   6: Sidastrea siderea
#   7: Unkown Coral
#   8: Oribcella anularis
#   9: Orbicella franksi
#   10: Solanastrea intersepta
#   11: Colpophyllia natans
#   12: Orbicella sp.
#   13: Porites porites
#   14: Porites asteroides
#   15: Pseudodiploria strigosa
#   16: Millepora alcicornis
#   17: Agaricia sp.
#   18: Mycetophyllia sp.
#   19: Meandrina meandrites

# Output class denomination:
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

def replace_first_column(input_file, output_file, class_change):
    with open(input_file, 'r') as file:
        lines = file.readlines()
        
    modified_lines = []
    for line in lines:
        columns = line.strip().split(' ')
        columns[0] = class_change[columns[0]]
        modified_lines.append(' '.join(columns) + '\n')
        
    with open(output_file, 'w') as file:
        file.writelines(modified_lines)
        
        
def aggregate_annotations(lbl_dir, out_dir, class_change):

    print('aggregate annotations')
    # find all examples of the given classes, and change them to just agaricia or or
    # actually, since it's YOLO, I just have to change numbers
    # just create a dictionary:
    

    # read in all label files
    lbl_files = sorted(glob.glob(os.path.join(lbl_dir, '*.txt')))
    
    # make output directory
    os.makedirs(out_dir, exist_ok=True)

    # for each lbl_file
    # iterate through each line in the label file
    # for the first character, apply class_change

    for i, lbl_path in enumerate(lbl_files):
        # print(f'{i}/{len(lbl_files)}')
        
        out_file = os.path.join(out_dir, os.path.basename(lbl_path))
        replace_first_column(lbl_path, out_file, class_change)
        
    print('done')


if __name__ == '__main__':
    
    lbl_dir = '/home/zachary/UVI_Training/data/yolo_seg/dataset_20230606/labels'
    out_dir = '/home/zachary/UVI_Training/data/yolo_seg/dataset_20230606/labels_combined'
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
    aggregate_annotations(lbl_dir, out_dir, class_change)
    
    # # debug
    # import code
    # code.interact(local=dict(globals(), **locals()))