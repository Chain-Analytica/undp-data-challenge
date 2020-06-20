import sys
import os.path as osp
import os
from keras.models import model_from_json
import cv2
from skimage.morphology import closing, disk
import numpy as np
from PIL import Image

CURRENT_DIR = os.path.dirname(os.path.abspath("__file__"))
ROOT_DIR = osp.join(CURRENT_DIR, '..')
sys.path.append(CURRENT_DIR)

model_json_path = osp.join(ROOT_DIR, "models", "model.json")
model_weight_path = osp.join(ROOT_DIR, "models", "model.h5")

my_threshold = 121
my_radius = 2


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


def main():

    abs_img_path = input('Please enter the absolute path of the image: \n')
    if len(abs_img_path) > 0:
        predict_img_path = abs_img_path
    else:
        predict_img_path = osp.join(ROOT_DIR, 'predict_img', '0.png')

    class_names = ['Black-grass', 'Charlock', 'Cleavers', 'Common Chickweed', 'Common wheat', 'Fat Hen', 'Loose Silky-bent', 'Maize', 'Scentless Mayweed', 'ShepherdGÇÖs Purse', 'Small-flowered Cranesbill', 'Sugar beet']

    json_file = open(model_json_path, 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights(model_weight_path)
    print("Loaded model from disk")

    loaded_model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    pil_image = Image.open(predict_img_path)

    np_image = np.array(pil_image)
    masked_image = segment_plant(np_image, my_threshold, my_radius)
    resized = cv2.resize(masked_image, (128, 128), interpolation=cv2.INTER_AREA)
    dim_expanded_image = np.expand_dims(resized, axis=0)

    print("Prediction on process...")
    prediction = loaded_model.predict_classes(dim_expanded_image)
    print("Prediction completed")

    print("result: " + class_names[prediction[0]])


if __name__ == "__main__":
    main()
