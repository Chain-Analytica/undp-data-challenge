from PIL import Image
import numpy as np
import sys
import os.path as osp
import os
from random import randint

np.set_printoptions(threshold=sys.maxsize)

# os.environ["CUDA_VISIBLE_DEVICES"] = 0

CURRENT_DIR = os.path.dirname(os.path.abspath("__file__"))
ROOT_DIR = osp.join(CURRENT_DIR, '..')
sys.path.append(CURRENT_DIR)

dataset_path = osp.join(ROOT_DIR, 'Dataset')
class_bal_sav_path = osp.join(ROOT_DIR, 'additional_dataset')
degrees_list_file_path = osp.join(ROOT_DIR, "degrees_completed.txt")


def create_additional_images(class_counts, class_names):
    total_count = class_counts
    inc = 0
    while True:
        flag = 0
        for x in total_count:
            if x < 1000:
                flag = 1
                break
        if flag > 0:
            inc += 35
            add_rotated_image(total_count, inc % 360, class_names, class_counts)
            total_count = find_total_count(class_names, class_counts)
        else:
            break


def find_total_count(class_names, class_counts):
    additional_class_counts = []
    for name in class_names:
        sub_data_wrk_dir = osp.join(class_bal_sav_path, name)
        images = os.listdir(sub_data_wrk_dir)
        additional_class_counts.append(len(images))

    total_count = []
    for i in range(0, len(additional_class_counts)):
        total_count.append(class_counts[i] + additional_class_counts[i])
    return total_count


def add_rotated_image(total_count, degree, class_names, class_counts):
    finish_degree_file = open(degrees_list_file_path, "r")
    line = finish_degree_file.readline().strip()
    for it in finish_degree_file:
        if int(it) == degree:
            return
    finish_degree_file.close()
    finish_degree_file = open(degrees_list_file_path, "a")
    finish_degree_file.write('\n' + str(degree))
    finish_degree_file.close()
    for idx, count in enumerate(total_count):
        sub_sav_path = osp.join(class_bal_sav_path, class_names[idx])
        if not os.path.exists(sub_sav_path):
            os.mkdir(sub_sav_path)
        req_no_of_img = 1000 - count
        if req_no_of_img > 0:
            for _ in range(req_no_of_img):
                value = randint(1, class_counts[idx])
                img_name = str(value) + '.png'
                img_path = osp.join(dataset_path, class_names[idx], img_name)
                if os.path.exists(img_path):
                    ima = Image.open(img_path)
                    ima = ima.rotate(degree)
                    sav_name = 'ad_' + str(value) + '_' + str(degree) + '.png'
                    ima.save(osp.join(sub_sav_path, sav_name))
        print(class_names[idx] + ' completed...')


def main():

    if not os.path.exists(class_bal_sav_path):
        os.mkdir(class_bal_sav_path)

    if not os.path.exists(degrees_list_file_path):
        completed_degree_file = open(degrees_list_file_path, "w")
        completed_degree_file.write(str(0))
        completed_degree_file.close()

    class_counts = []
    class_names = os.listdir(dataset_path)

    for name in class_names:
        sub_data_wrk_dir = osp.join(dataset_path, name)
        images = os.listdir(sub_data_wrk_dir)
        class_counts.append(len(images))
    print(class_names)
    print(class_counts)

    create_additional_images(class_counts, class_names)


if __name__ == "__main__":
    main()