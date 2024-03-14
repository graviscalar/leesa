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
        'QWXGA': {'w': 2048, 'h': 1152, 'ratio': '16:9'},
        'QXGA': {'w': 2048, 'h': 1536, 'ratio': '4:3'},
        'OS03B10': {'w': 2304, 'h': 1296, 'ratio': '16:9'},
        's2560': {'w': 2560, 'h': 1080, 'ratio': '21:9'},
        'QHD': {'w': 2560, 'h': 1440, 'ratio': '16:9'},
        'WQXGA': {'w': 2560, 'h': 1600, 'ratio': '16:10'},
        's2592': {'w': 2592, 'h': 1944, 'ratio': '4:3'},
        'IMX675': {'w': 2592, 'h': 1944, 'ratio': '16:9'},
        'IMX664': {'w': 2688, 'h': 1520, 'ratio': '16:9'},
        'IMX178': {'w': 3096, 'h': 2080, 'ratio': '16:9'},
        'UWQHD': {'w': 3440, 'h': 1440, 'ratio': '21:9'},
        '4K_UHD': {'w': 3840, 'h': 2160, 'ratio': '16:9'},
        'IMX294': {'w': 4168, 'h': 2176, 'ratio': '17:9'},
        'IMX571': {'w': 6244, 'h': 4168, 'ratio': '3:2'},
        'IMX455': {'w': 9568, 'h': 6380, 'ratio': '3:2'},
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
