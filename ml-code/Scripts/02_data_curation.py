from PIL import Image
import numpy as np
from skimage.morphology import closing, disk
import sys
import cv2
import os.path as osp
import os

os.environ["CUDA_VISIBLE_DEVICES"] = str(0)

CURRENT_DIR = os.path.dirname(os.path.abspath("__file__"))
ROOT_DIR = osp.join(CURRENT_DIR, '..')
sys.path.append(CURRENT_DIR)

dataset_path = osp.join(ROOT_DIR, 'Dataset')
class_bal_sav_path = osp.join(ROOT_DIR, 'additional_dataset')
save_dir_path = osp.join(ROOT_DIR, 'Curated_Dataset')
ad_data_save_dir_path = osp.join(ROOT_DIR, 'Curated_Additional_Dataset')
data_csv_path = osp.join(ROOT_DIR, "data.csv")

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


def data_curation(data_path, extra_data_path, save_path, extra_data_save_path, csv_path):
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    if not os.path.exists(extra_data_save_path):
        os.mkdir(extra_data_save_path)

    class_names = os.listdir(data_path)

    for name in class_names:
        sub_data_wrk_dir = osp.join(data_path, name)
        sub_extr_data_wrk_dir = osp.join(extra_data_path, name)
        cur_dir_path = osp.join(save_path, name)
        cur_additional_data_path = osp.join(extra_data_save_path, name)

        if not os.path.exists(cur_dir_path):
            os.mkdir(cur_dir_path)
        if not os.path.exists(cur_additional_data_path):
            os.mkdir(cur_additional_data_path)

        for file in os.listdir(sub_data_wrk_dir):
            file_path = osp.join(sub_data_wrk_dir, file)
            pil_image = Image.open(file_path)
            np_image = np.array(pil_image)
            masked_image = segment_plant(np_image, my_threshold, my_radius)
            sv_img = Image.fromarray(masked_image)
            file_sv_path = osp.join(cur_dir_path, file)
            sv_img.save(file_sv_path)
            csv_file = open(csv_path, "a")
            csv_file.write(file_sv_path + ',' + file + ',' + name)
            csv_file.write("\n")
            csv_file.close()
        print(name + ' data curation completed...')

        for file in os.listdir(sub_extr_data_wrk_dir):
            file_path = osp.join(sub_extr_data_wrk_dir, file)
            pil_image = Image.open(file_path)
            np_image = np.array(pil_image)
            masked_image = segment_plant(np_image, my_threshold, my_radius)
            sv_img = Image.fromarray(masked_image)
            file_sv_path = osp.join(cur_additional_data_path, file)
            sv_img.save(file_sv_path)
            csv_file = open(csv_path, "a")
            csv_file.write(file_sv_path + ',' + file + ',' + name)
            csv_file.write("\n")
            csv_file.close()
        print(name + ' additional data curation completed...')

#### Have to do apply gaussian filter for masked_image


def main():

    if not os.path.exists(data_csv_path):
        data_csv_file = open(data_csv_path, "w")
        data_csv_file.close()

    data_curation(dataset_path, class_bal_sav_path, save_dir_path, ad_data_save_dir_path, data_csv_path)


if __name__ == "__main__":
    main()