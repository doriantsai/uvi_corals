# uvi_corals
Image segmentation/Object detection of deep sea corals with University of the Virgin Islands, United States and the Queensland University of Technology, Australia.

# virtual environment setup
Optionally run make_uvi_venv.sh to automatically create virtual environment, but one can also simply run:

      pip install ultralytics
      
Which should also install all the required dependencies for Yolov8

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
