import os
import numpy as np
import PIL.Image
import json
from leesa.geometry import *

class Colors:
    _COLORS = {
        'R': (255, 0, 0),
        'G': (0, 255, 0),
        'B': (0, 0, 255),
        'BL': (0, 0, 0),
        'W': (255, 255, 255),
        'C': (0, 255, 255),
        'M': (255, 0, 255),
        'Y': (255, 255, 0)
    }

    def get_dict(self):
        return self._COLORS


class FrameResolution:
    _FRAME_SIZE = {
        'QQVGA': {'w': 160, 'h': 120, 'ratio': '4:3'},
        'nHD': {'w': 640, 'h': 360, 'ratio': '16:9'},
        'VGA': {'w': 640, 'h': 480, 'ratio': '4:3'},
        'SVGA': {'w': 800, 'h': 600, 'ratio': '4:3'},
        'XGA': {'w': 1024, 'h': 768, 'ratio': '4:3'},
        'WXGA_1152': {'w': 1152, 'h': 768, 'ratio': '3:2'},
        'HD': {'w': 1280, 'h': 720, 'ratio': '16:9'},
        'WXGA_1280': {'w': 1280, 'h': 800, 'ratio': '16:10'},
        'SXGAminus': {'w': 1280, 'h': 960, 'ratio': '4:3'},
        'SXGA': {'w': 1280, 'h': 1024, 'ratio': '5:4'},
        's1440': {'w': 1440, 'h': 720, 'ratio': '18:9'},
        'HD+': {'w': 1600, 'h': 900, 'ratio': '16:9'},
        'UXGA': {'w': 1600, 'h': 1200, 'ratio': '4:3'},
        'WSXGA+': {'w': 1680, 'h': 1050, 'ratio': '16:10'},
        'FHD': {'w': 1920, 'h': 1080, 'ratio': '16:9'},
        'WUXGA': {'w': 1920, 'h': 1200, 'ratio': '16:10'},
        'CMV2000': {'w': 2048, 'h': 1088, 'ratio': '17:9'},
        'QWXGA': {'w': 2048, 'h': 1152, 'ratio': '16:9'},
        'QXGA': {'w': 2048, 'h': 1536, 'ratio': '4:3'},
        'OS04E10': {'w': 2048, 'h': 2048, 'ratio': '1:1'},
        'OS03B10': {'w': 2304, 'h': 1296, 'ratio': '16:9'},
        's2560': {'w': 2560, 'h': 1080, 'ratio': '21:9'},
        'QHD': {'w': 2560, 'h': 1440, 'ratio': '16:9'},
        'WQXGA': {'w': 2560, 'h': 1600, 'ratio': '16:10'},
        's2592': {'w': 2592, 'h': 1944, 'ratio': '4:3'},
        'IMX675': {'w': 2592, 'h': 1944, 'ratio': '16:9'},
        'IMX664': {'w': 2688, 'h': 1520, 'ratio': '16:9'},
        'OS05A10': {'w': 2688, 'h': 1944, 'ratio': '4:3'},
        'IMX178': {'w': 3096, 'h': 2080, 'ratio': '16:9'},
        'UWQHD': {'w': 3440, 'h': 1440, 'ratio': '21:9'},
        '4K_UHD': {'w': 3840, 'h': 2160, 'ratio': '16:9'},
        'OS08C10': {'w': 3872, 'h': 2192, 'ratio': '16:9'},
        'CMV1200': {'w': 4096, 'h': 3072, 'ratio': '4:3'},
        'IMX294': {'w': 4168, 'h': 2176, 'ratio': '17:9'},
        'OS12D40': {'w': 4512, 'h': 2512, 'ratio': '17:9'},
        'CMV20000': {'w': 5120, 'h': 3840, 'ratio': '4:3'},
        'IMX571': {'w': 6244, 'h': 4168, 'ratio': '3:2'},
        'CMV50000': {'w': 7920, 'h': 6004, 'ratio': '4:3'},
        'IMX455': {'w': 9568, 'h': 6380, 'ratio': '3:2'},
        'CHR70M': {'w': 10000, 'h': 7096, 'ratio': '4:3'},
    }

    def get_dict(self):
        return self._FRAME_SIZE


def img_save(img, image_name: str = None) -> None:
    """
    Save an image to carrier

    :param img: PIL image object
    :param image_name: the image file name with path and extension
    :return: None
    """
    # save image
    if image_name is not None:
        os.makedirs(os.path.dirname(image_name), exist_ok=True)
        img.save(image_name)


def image_open_np(fn: str = None) -> np.ndarray:
    img = PIL.Image.open(fn)
    dt = np.array(img).astype(float)
    return dt


def image_save_np(img: np.ndarray = None, fn: str = None, mode: str = 'RGB') -> None:
    d = PIL.Image.fromarray(img).convert(mode)
    d.save(fn)
    return None


def image_warping_2d_2d(img_auto, json_auto, img_plate, img_dst):
    img_a = PIL.Image.open(img_auto)
    img_p = PIL.Image.open(img_plate)

    fp = open(json_auto, 'r')
    dst_d = json.load(fp)
    fp.close()

    src = np.array([[0, 0],
                    [img_p.width, 0],
                    [0, img_p.height],
                    [img_p.width, img_p.height]])
    dst = np.array([dst_d['a'], dst_d['b'], dst_d['c'], dst_d['d']])
    m = warping_2d_2d_matrix(src, dst)

    img_a_1 = img_a.load()
    img_p_1 = img_p.load()

    for x in range(img_p.width):
        for y in range(img_p.height):
            p_hom = [x, y, 1]
            p1_hom = m @ p_hom
            p1 = [x / p1_hom[2] for x in p1_hom[:-1]]
            img_a_1[int(p1[0]), int(p1[1])] = img_p_1[x, y]

    directory = os.path.dirname(img_dst)
    if not os.path.exists(directory):
        os.makedirs(directory)
        print("The directory {0} created".format(directory))

    img_a.save(img_dst)

# convolution
# # Define a 2x2 matrix
# matrix = np.array([[1, 1], [-1, -1]])  # Replace a, b, c, d with your desired values
#
# c = np.zeros(image_array.shape)
#
# for y in range(c.shape[0]):
#     if y < c.shape[0] - matrix.shape[0]:
#         for x in range(c.shape[1]):
#             if x < c.shape[1] - matrix.shape[1]:
#                 c[y, x] = np.sum(np.multiply(image_array[y:y + matrix.shape[0], x: x + matrix.shape[1]], matrix))
