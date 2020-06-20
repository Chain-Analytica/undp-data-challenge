import sys
import os.path as osp
import os
import random
from tensorflow.python.client import device_lib

os.environ["CUDA_VISIBLE_DEVICES"] = str(0)

CURRENT_DIR = os.path.dirname(os.path.abspath("__file__"))
ROOT_DIR = osp.join(CURRENT_DIR, '..')
sys.path.append(CURRENT_DIR)

train_csv_path = osp.join(ROOT_DIR, "train.csv")
val_csv_path = osp.join(ROOT_DIR, "val.csv")
test_csv_path = osp.join(ROOT_DIR, "test.csv")
data_csv_path = osp.join(ROOT_DIR, "data.csv")


def split_train_test(csv_path):
    fid = open(csv_path, "r")
    li = fid.readlines()
    fid.close()
    random.shuffle(li)
    train = li[int(len(li) * 0.3): len(li)]
    val = li[0: int(len(li) * 0.2)]
    test = li[int(len(li) * 0.2): int(len(li) * 0.3)]
    return train, val, test


def write_to_csv(path, category):
    fid = open(path, "w")
    fid.writelines(category)
    fid.close()

def main():
    print(device_lib.list_local_devices())
    train, val, test = split_train_test(data_csv_path)
    write_to_csv(train_csv_path, train)
    write_to_csv(val_csv_path, val)
    write_to_csv(test_csv_path, test)


if __name__ == "__main__":
    main()