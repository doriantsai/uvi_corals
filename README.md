# uvi_corals
Image segmentation/Object detection of deep sea corals with University of the Virgin Islands, United States and the Queensland University of Technology, Australia.

# virtual environment setup
To make virtual python environment, run `make_uvi_venv.sh` to automatically create virtual environment.

      chmod +x make_uvi_venv.sh
      ./make_uvi_venv.sh
      conda activate uvi

- git clone the ultralytics repository
- cd to the ultralytics repo

      pip install -e .

Now, ultralytics is installed from source, and python should know that when importing yolov8, it is running locally. This allows us to do image augmentations (see below).


# Machine Learning Pipeline
Follow the install process and documentation:
https://github.com/ultralytics/ultralytics

# Annotation Pipeline
- Download all images and put them into a single image directory folder (this can contain sub-folders)
- Export dataset annotations from CVAT in COCO format (due to current YOLO format exported from CVAT unable to register polygons)
- In `annotation_pipeline.py`, specify the image directories and label directories and the final dataset directory.
- Run `annotation_pipeline.py`
- In `model_training`, specify the YOLOv8 model type and data yaml file.
- Run `train_model.py`
- For predictions, specify the model and image library in `predict_model.py`
- Run `predict_model.py`

# Albumentations (Image Augmentation)

- pip install albumentations
- in the yolov8 ultralytics repo, edit the file:

      /ultralytics/ultralytics/yolo/data/dataloaders/v5augmentations.py

- NOTE: potential confusion to which yolov8 ultralytics version is being used, disambiguate via `which ultralytics`
- NOTE: Yolov8 architecture is changing, and so most recently (2023/08/09) Serena and Dorian found the same functionality in `/ultralytics/ultralytics/data/augment.py`
- made the following changes (namely added ColorJitter, and RandomResizedCrop)

      T = [
            A.RandomResizedCrop(height=s640, width=640, scale=(0.8, 1.0), ratio=(0.9, 1.11), p=0.5),
            A.Blur(p=0.01),
            A.MedianBlur(p=0.01),
            A.ToGray(p=0.01),
            A.CLAHE(p=0.01),
            A.ColorJitter(brightness=0.2,
                        contrast=0.3,
                        saturation=0.3,
                        hue=0.2,
                        p=0.5),
            A.RandomBrightnessContrast(p=0.0),
            A.RandomGamma(p=0.0),
            A.ImageCompression(quality_lower=75, p=0.0)]

# Training Model

- setup a wandb.com account to see/records of trainin results online
- setup folders, model architecture/size, epochs, etc
- Run train_model.py
