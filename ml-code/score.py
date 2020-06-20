import sys
import os.path as osp
import os
import time
from keras.models import load_model
import cv2
from skimage.morphology import closing, disk
import numpy as np
import json
from PIL import Image
import io

# Called when the deployed service starts
def init():
    global loaded_model
    global class_names
    # Get the path where the deployed model can be found.
    model_path = os.path.join(os.getenv('AZUREML_MODEL_DIR'), './models')
    loaded_model = load_model(model_path + '/model.h5')
    loaded_model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    class_names = ['Black-grass', 'Charlock', 'Cleavers', 'Common Chickweed', 'Common wheat', 'Fat Hen', 'Loose Silky-bent', 'Maize', 'Scentless Mayweed', 'ShepherdGÇÖs Purse', 'Small-flowered Cranesbill', 'Sugar beet']

# Handle requests to the service
def run(raw_data):
    try:
        start_at = time.time()
        pil_image = Image.open(io.BytesIO(bytearray(json.loads(raw_data)['data'])))
        np_image = np.array(pil_image)
#np_image = np.array(pil_image)
        my_threshold = 121
        my_radius = 2
        masked_image = segment_plant(np_image, my_threshold, my_radius)
        resized = cv2.resize(masked_image, (128, 128), interpolation=cv2.INTER_AREA)
        dim_expanded_image = np.expand_dims(resized, axis=0)
        prediction = loaded_model.predict_classes(dim_expanded_image)
        print("Prediction completed")
        #Return prediction
        return {"result": class_names[prediction[0]],"elapsed_time": time.time()-start_at}
        #return {"result": "sugar beet","elapsed_time": time.time()-start_at}
    except Exception as e:
        error = str(e)
        return error

def get_mask(image, threshold, radius):
    mask = np.where(image < threshold, 1, 0)
    selem = disk(radius)
    mask = closing(mask, selem)
    return mask

def segment_plant(np_image, threshold, radius):
    image_lab = cv2.cvtColor(np_image, cv2.COLOR_BGR2LAB)
    mask = get_mask(image_lab[:, :, 1], threshold, radius)
    masked_image = np_image.copy()
    for n in range(3):
        masked_image[:, :, n] = np_image[:, :, n] * mask
    return masked_image
