import numpy as np
import sys
import os.path as osp
import os
import pandas as pd
from tensorflow.python.client import device_lib
import tensorflow as tf
from keras_preprocessing.image import ImageDataGenerator
from keras.layers import Dense, Activation, Flatten, Dropout, BatchNormalization
from keras.layers import Conv2D, MaxPooling2D
from keras import Sequential

os.environ["CUDA_VISIBLE_DEVICES"] = str(0)

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

gpu_options = tf.GPUOptions(allow_growth=True)
session = tf.InteractiveSession(config=tf.ConfigProto(gpu_options=gpu_options))

CURRENT_DIR = os.path.dirname(os.path.abspath("__file__"))
ROOT_DIR = osp.join(CURRENT_DIR, '..')
sys.path.append(CURRENT_DIR)

batch_size = 16
random_seed = 12
mode = "categorical"
img_size = 128

train_csv_path = osp.join(ROOT_DIR, "train.csv")
val_csv_path = osp.join(ROOT_DIR, "val.csv")
test_csv_path = osp.join(ROOT_DIR, "test.csv")
data_csv_path = osp.join(ROOT_DIR, "data.csv")
model_json_path = osp.join(ROOT_DIR, "models", "model.json")
model_weight_path = osp.join(ROOT_DIR, "models", "model.h5")
u_train_csv_path = osp.join(ROOT_DIR, "u_train.csv")
u_val_csv_path = osp.join(ROOT_DIR, "u_val.csv")
u_test_csv_path = osp.join(ROOT_DIR, "u_test.csv")


def create_model_net():
    kernel_size = (3, 3)
    pool_size = (2, 2)
    first_filters = 32
    second_filters = 64
    third_filters = 128

    dropout_conv = 0.3
    dropout_dense = 0.3

    model = Sequential()
    model.add(Conv2D(first_filters, kernel_size, activation='relu',
                     input_shape=(img_size, img_size, 3)))
    model.add(Conv2D(first_filters, kernel_size, activation='relu'))
    model.add(Conv2D(first_filters, kernel_size, activation='relu'))
    model.add(MaxPooling2D(pool_size=pool_size))
    model.add(Dropout(dropout_conv))

    model.add(Conv2D(second_filters, kernel_size, activation='relu'))
    model.add(Conv2D(second_filters, kernel_size, activation='relu'))
    model.add(Conv2D(second_filters, kernel_size, activation='relu'))
    model.add(MaxPooling2D(pool_size=pool_size))
    model.add(Dropout(dropout_conv))

    model.add(Conv2D(third_filters, kernel_size, activation='relu'))
    model.add(Conv2D(third_filters, kernel_size, activation='relu'))
    model.add(Conv2D(third_filters, kernel_size, activation='relu'))
    model.add(MaxPooling2D(pool_size=pool_size))
    model.add(Dropout(dropout_conv))

    model.add(Flatten())
    model.add(Dense(256, activation="relu"))
    model.add(Dropout(dropout_dense))
    model.add(Dense(12, activation="softmax"))

    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    return model


def main():
    datagen = ImageDataGenerator()

    val_datagen = ImageDataGenerator()

    train_generator = datagen.flow_from_directory(
        osp.join(ROOT_DIR, 'data/train/'),
        class_mode=mode,
        batch_size=batch_size,
        target_size=(img_size, img_size))

    valid_generator = val_datagen.flow_from_directory(
        osp.join(ROOT_DIR, 'data/val/'),
        class_mode=mode,
        batch_size=batch_size,
        target_size=(img_size, img_size))

    model = create_model_net()

    model.fit_generator(
        generator=train_generator,
        steps_per_epoch=525,
        validation_data=valid_generator,
        validation_steps=50,
        epochs=20)

    if not os.path.exists(osp.join(ROOT_DIR, 'models')):
        os.mkdir(osp.join(ROOT_DIR, 'models'))

    # serialize model to JSON
    model_json = model.to_json()
    with open(model_json_path, "w") as json_file:
        json_file.write(model_json)
    # serialize weights to HDF5
    model.save_weights(model_weight_path)
    print("Saved model to disk")




if __name__ == "__main__":
    main()