"""Contains the Sensor parameters.
"""
from leesa.image import *


class Sensor:
    """The Sensor parameters.

    :param frame_type: current active resolution, not a real sensor size
    :param pixel_size: pixel size in meters
    """

    def __init__(self, frame_type: str = 'QQVGA', pixel_size:float = 2.8e-06):
        fr = FrameResolution()
        _FRAME_SIZE = fr.get_dict()

        if frame_type is None:
            raise ValueError("The frame size must be non-empty.")

        frame = _FRAME_SIZE[frame_type]

        self.frame_width = frame['w']
        self.frame_height = frame['h']
        self.pixel_size = pixel_size
