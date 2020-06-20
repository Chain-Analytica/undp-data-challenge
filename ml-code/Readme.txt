Download the dataset from:
https://www.kaggle.com/vbookshelf/v2-plant-seedlings-dataset

Rename the dataset directory as 'dataset' and keep it in you working directory

Maintain the following directory structure

working directory(Root Dir)
----|Dataset
    ----|Black-grass
    ----|Charlock
        ....
----|Scripts
    ----|01_add_data.py
    ----|02_data_curation.py
        ....
----|predict_img
    ----|7.png  ### image to be predicted

For predicting a new image
***********
Run infer.py script. You will have to provide a valid absolute path of the image when prompted eg: E:\AngelHack\Dataset\Black-grass\1.png

OR

Edit the infer.py code. provide the valid path to the image ( change predict_img_path variable in line no.43 and run the script )
you can skip the prompt by just pressing enter


To train the model from scratch
*******************************

Run the python scripts in the following order:
01_add_data.py
02_data_curation.py
03_train_test_split.py
04_train_test_to_dir.py
05_train_from_directory.py

the models will be saved in the 'models' directory

For evaluation run
Evaluate.py

For inference run
infer.py
