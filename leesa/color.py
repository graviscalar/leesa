import numpy as np
from PIL import Image


def image_open_np(fn: str = None) -> np.ndarray:
    img = Image.open(fn)
    dt = np.array(img).astype(float)
    return dt


def image_save_np(img: np.ndarray = None, fn: str = None, mode: str = 'RGB') -> None:
    d = Image.fromarray(img).convert(mode)
    d.save(fn)
    return None


def image_rgb_to_lum_itu7096(img: np.ndarray = None) -> np.ndarray:
    """
    Convert RGB values to luminance values as described in the ITU-R  BT.709-6
    https://www.itu.int/rec/R-REC-BT.709-6-201506-I/en
    :param img: RGB pixels
    :return: Derivation of luminance signal from table 3 "Signal Format"
    """
    if img is None:
        raise ValueError("Image object must be non-empty.")

    itu7096 = np.array([0.2126, 0.7152, 0.0722])
    r_lum = np.dot(img, itu7096)
    return r_lum
