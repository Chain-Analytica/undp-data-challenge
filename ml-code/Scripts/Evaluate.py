import sys
import os.path as osp
import os
from keras.models import model_from_json
from keras_preprocessing.image import ImageDataGenerator


CURRENT_DIR = os.path.dirname(os.path.abspath("__file__"))
ROOT_DIR = osp.join(CURRENT_DIR, '..')
sys.path.append(CURRENT_DIR)

model_json_path = osp.join(ROOT_DIR, "models", "model.json")
model_weight_path = osp.join(ROOT_DIR, "models", "model.h5")
test_dir = osp.join(ROOT_DIR, 'data', 'test')


IMAGE_SIZE = 128


def main():

    datagen = ImageDataGenerator()

    json_file = open(model_json_path, 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights(model_weight_path)
    print("Loaded model from disk")

    loaded_model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    test_gen = datagen.flow_from_directory(test_dir,
                                        target_size=(IMAGE_SIZE, IMAGE_SIZE),
                                        batch_size=1,
                                        class_mode='categorical',
                                        shuffle=False)

    val_loss, val_acc = loaded_model.evaluate_generator(test_gen, steps=len(test_gen)/2)

    print('val_loss:', val_loss)
    print('val_acc:', val_acc)

    print(len(test_gen))

if __name__ == "__main__":
    main()