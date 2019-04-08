from typing import NoReturn, Tuple
import os
import numpy as np
from PIL import Image
from pdf2image import convert_from_path
from scipy import ndimage as nd
from scipy.linalg import norm
from skimage.color import rgb2gray
from skimage.filters import gabor_kernel

signature_location = {
    'ABCD': {
        'page': 1,
        'bounding_box': (700, 1600, 1700, 2200)
    },
    'PWRS': {
        'page': 1,
        'bounding_box': (700, 1600, 1700, 2200)
    },
    'DFGH': {
        'page': 1,
        'bounding_box': (700, 1600, 1700, 2200)
    },
    'EDFGH': {
        'page': 1,
        'bounding_box': (700, 1600, 1700, 2200)
    }
}


def convert_to_greyscale(img: Image) -> np.array:
    '''
    Convert the image to grey scale
    :param img:
    :return:
    '''
    return rgb2gray(img)


# crop image -> (700, 1600, 1700, 2200)
def crop_image(img: Image, dim: Tuple) -> np.array:
    '''
    To crop image
    :param img:
    :param dim:
    :return:
    '''
    img_crop = img.crop(dim)
    arr_img_crop = np.asarray(img_crop)
    return arr_img_crop


def normalize(arr: np.array) -> np.array:
    '''
    normalize to compensate for exposure difference
    :param arr:
    :return:
    '''
    rng = arr.max() - arr.min()
    amin = arr.min()
    return (arr-amin) * 255/rng


def save_image(arr: np.array) -> NoReturn:
    '''
    To Save image from numpy array
    :param arr:
    :return:
    '''
    img = Image.fromarray(arr, 'RGB')
    img.save('my.png')
    img.show()


def apply_gabor_filter(image_arr: np.array) -> np.array:
    '''
    Apply Gabor filter to image texture where changes has been made
    :param image_arr:
    :return:
    '''
    # to apply gabor filter
    # apply filter on a grey scale image
    kernel = np.real(gabor_kernel(frequency=0.4, theta=0, sigma_x=10, sigma_y=10))
    image_arr_gs = rgb2gray(image_arr)
    filtered = nd.convolve(image_arr_gs, kernel, mode='wrap')
    return filtered


def detect_signature(path1: str, path2: str, page_no: int, bounding_box: Tuple) -> bool:
    '''
    Function to detect signature
    :param path1:
    :param path2:
    :param page_no:
    :param bounding_box:
    :return:
    '''

    images1 = convert_from_path(path1)
    images2 = convert_from_path(path2)
    img_1 = images1[page_no-1]
    img_2 = images2[page_no-1]
    arr_crop_img1 = crop_image(img_1, bounding_box)
    arr_crop_img2 = crop_image(img_2, bounding_box)
    gb_arr1 = apply_gabor_filter(arr_crop_img1)
    gb_arr2 = apply_gabor_filter(arr_crop_img2)
    # calculate the difference and its norms
    diff = normalize(gb_arr1) - normalize(gb_arr2)
    z_norm = norm(diff.ravel(), 0)
    return z_norm > 1000 # empirical value


def is_signature_present(files_to_read: list):

    is_signature_present_flag = dict()

    for file in files_to_read:
        file_name = os.path.basename(file)
        prefix = file_name.split('_')[0]

        if prefix in signature_location.keys():
            is_signature_present_flag[file_name] = detect_signature(file,
                                                                    file,
                                                                    signature_location[prefix]['page'],
                                                                    signature_location[prefix]['bounding_box'])
        else:
            is_signature_present_flag[file_name] = '404 on template'

    return is_signature_present_flag


# # test function
# if __name__ == "__main__":
#     isSigned = detect_signature("sample.pdf", "sample-modified.pdf", 6, (700, 1600, 1700, 2200))
#     print(isSigned)
