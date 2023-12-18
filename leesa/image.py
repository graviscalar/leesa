import PIL.Image
import numpy as np
import os


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
