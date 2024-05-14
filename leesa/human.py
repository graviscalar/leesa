"""Contains the Sensor parameters.
"""
from leesa.image import *
import math
from leesa.camera import Camera


class Human:
    """The Sensor parameters.

    :param frame_type: current active resolution, not a real sensor size
    """

    def __init__(self):
        self.eyes_d = 0.063
        self.face_w = 0.14
        self.human_h = 1.72

    def camera_to_distance(self, eyes_d: int = 10, face_w: int = 10, human_h: int = 100, cam: Camera = None,
                           mode: int = 0) -> float:
        distance = 0.0

        if mode == 0:
            distance = cam.os.focal_length * self.eyes_d / (cam.sr.pixel_size * eyes_d)
        elif mode == 1:
            distance = cam.os.focal_length * self.face_w / (cam.sr.pixel_size * face_w)
        elif mode == 2:
            distance = cam.os.focal_length * self.human_h / (cam.sr.pixel_size * human_h)

        return distance

    def distance_to_focal(self, eyes_d: int = 10, face_w: int = 10, human_h: int = 100, cam: Camera = None,
                          distance: float = 0.0,
                          mode: int = 0) -> float:
        focal_length = 0.0

        if mode == 0:
            focal_length = (cam.sr.pixel_size * eyes_d * distance) / self.eyes_d
        elif mode == 1:
            focal_length = (cam.sr.pixel_size * face_w * distance) / self.face_w
        elif mode == 2:
            focal_length = (cam.sr.pixel_size * human_h * distance) / self.human_h

        return focal_length

    # estimate pixels quantity by using distance
    def distance_to_pixels(self, distance: float = 1.0, cam: Camera = None,
                           mode: int = 0) -> float:
        pixels = 0

        if mode == 0:
            pixels = cam.os.focal_length * self.eyes_d / (cam.sr.pixel_size * distance)
        elif mode == 1:
            pixels = cam.os.focal_length * self.face_w / (cam.sr.pixel_size * distance)
        elif mode == 2:
            pixels = cam.os.focal_length * self.human_h / (cam.sr.pixel_size * distance)

        return pixels
