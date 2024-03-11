import os


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
        'SXGA': {'w': 1280, 'h': 1024, 'ratio': '5:4'},
        'XGA': {'w': 1024, 'h': 768, 'ratio': '4:3'},
        'SXGAminus': {'w': 1280, 'h': 960, 'ratio': '4:3'},
        's2592': {'w': 2592, 'h': 1944, 'ratio': '4:3'},
        'WXGA_1152': {'w': 1152, 'h': 768, 'ratio': '3:2'},
        'WXGA_1280': {'w': 1280, 'h': 800, 'ratio': '16:10'},
        'nHD': {'w': 640, 'h': 360, 'ratio': '16:9'},
        'HD': {'w': 1280, 'h': 720, 'ratio': '16:9'},
        'FHD': {'w': 1920, 'h': 1080, 'ratio': '16:9'},
        's1440': {'w': 1440, 'h': 720, 'ratio': '18:9'},
        's2560': {'w': 2560, 'h': 1080, 'ratio': '21:9'},
        'IMX664': {'w': 2688, 'h': 1520, 'ratio': '16:9'},
        '4K_UHD': {'w': 3840, 'h': 2160, 'ratio': '16:9'},
        'IMX294': {'w': 4168, 'h': 2176, 'ratio': '17:9'},
        'IMX571': {'w': 6244, 'h': 4168, 'ratio': '3:2'},
        'IMX455': {'w': 9568, 'h': 6380, 'ratio': '3:2'},
        'IMX178': {'w': 3096, 'h': 2080, 'ratio': '16:9'},
        'IMX675': {'w': 2592, 'h': 1944, 'ratio': '16:9'}
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
