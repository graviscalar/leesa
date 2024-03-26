"""Contains the Optical and Sensor parameters.
"""
from .optics import Optics
from .sensor import Sensor
import math


class Camera:
    """The Sensor and Optics parameters.

    frame_width: the sensor class
    optics: the optics class
    """

    def __init__(self, sensor: Sensor, optics: Optics):
        self.sr = sensor
        self.os = optics
        self.fov_horizontal = 2 * math.atan(self.sr.s_w / 2 / self.os.focal_length)
        self.fov_vertical = 2 * math.atan(self.sr.s_h / 2 / self.os.focal_length)
        print(math.degrees(self.fov_horizontal))
        print(math.degrees(self.fov_vertical))