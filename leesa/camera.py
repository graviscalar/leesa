"""Contains the Optical and Sensor parameters.
"""
from .optics import Optics
from .sensor import Sensor


class Camera:
    """The Sensor and Optics parameters.

    frame_width: the sensor class
    optics: the optics class
    """

    def __init__(self, sensor: Sensor, optics: Optics):
        self.sr = sensor
        self.os = optics
