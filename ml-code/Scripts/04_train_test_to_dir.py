import sys
import os.path as osp
import os
from PIL import Image

CURRENT_DIR = os.path.dirname(os.path.abspath("__file__"))
ROOT_DIR = osp.join(CURRENT_DIR, '..')
sys.path.append(CURRENT_DIR)

train_csv_path = osp.join(ROOT_DIR, "train.csv")
val_csv_path = osp.join(ROOT_DIR, "val.csv")
test_csv_path = osp.join(ROOT_DIR, "val.csv")

save_path = osp.join(ROOT_DIR, 'data')
save_path_train = osp.join(save_path, 'train')
save_path_val = osp.join(save_path, 'val')
save_path_test = osp.join(save_path, 'test')


def main():
    if not os.path.exists(save_path):
        os.mkdir(save_path)

    if not os.path.exists(save_path_train):
        os.mkdir(save_path_train)
        train_csv_file = open(train_csv_path, "r")

        for line in train_csv_file:
            img = Image.open(line.split(',')[0].strip())
            class_label = line.split(',')[2].strip()
            file_save_dir_path = osp.join(save_path_train, class_label)
            if not os.path.exists(file_save_dir_path):
                os.mkdir(file_save_dir_path)
            img.save(osp.join(file_save_dir_path, line.split(',')[1].strip()))
        train_csv_file.close()

    print("Train data shifting completed..")

    if not os.path.exists(save_path_val):
        os.mkdir(save_path_val)
        val_csv_file = open(val_csv_path, "r")

        for line in val_csv_file:
            img = Image.open(line.split(',')[0].strip())
            class_label = line.split(',')[2].strip()
            file_save_dir_path = osp.join(save_path_val, class_label)
            if not os.path.exists(file_save_dir_path):
                os.mkdir(file_save_dir_path)
            img.save(osp.join(file_save_dir_path, line.split(',')[1].strip()))
        val_csv_file.close()

    print("Validation data shifting completed..")

    if not os.path.exists(save_path_test):
        os.mkdir(save_path_test)
        test_csv_file = open(test_csv_path, "r")

    for line in test_csv_file:
        img = Image.open(line.split(',')[0].strip())
        class_label = line.split(',')[2].strip()
        file_save_dir_path = osp.join(save_path_test, class_label)
        if not os.path.exists(file_save_dir_path):
            os.mkdir(file_save_dir_path)
        img.save(osp.join(file_save_dir_path, line.split(',')[1].strip()))
    test_csv_file.close()

    print("Test data shifting completed..")


if __name__ == "__main__":
    main()