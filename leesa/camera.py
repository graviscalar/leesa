"""Contains the Optical and Sensor parameters.
"""
from .optics import Optics
from .sensor import Sensor
import math
from .geometry import *


class Camera:
    """The Sensor and Optics parameters.

    frame_width: the sensor class
    optics: the optics class
    """

    def __init__(self, sensor: Sensor, optics: Optics, angle: CamAngle = CamAngle(0, 0, 0), altitude: float = 1.72):
        self.sr = sensor
        self.os = optics
        self.fov_horizontal = 2 * math.atan(self.sr.s_w / 2 / self.os.focal_length)
        self.fov_vertical = 2 * math.atan(self.sr.s_h / 2 / self.os.focal_length)
        self.angle = angle
        self.altitude = altitude
        self.estimate_poly_on_ground()
        # print(math.degrees(self.fov_horizontal))
        # print(math.degrees(self.fov_vertical))

    def estimate_poly_on_ground(self):
        """
         The camera FOV intersection with ground. A very simple method with Pitch angle only.

         A     B
         ------
         \    /
          \__/
          C  D
        """
        y_inf = 10 # let's assume the maximum distance
        an = math.radians(self.angle.pitch) + self.fov_vertical / 2
        c = Point3D(0, 0, 0)
        if an < math.radians(90):
            c.y = self.altitude / math.tan(an)
            c.x = - math.tan(self.fov_horizontal / 2) * c.y
        c = Point3D(-c.x, c.y, 0)
        a = Point3D(0, 0, 0)
        b = Point3D(0, 0, 0)
        # verifying A and B in infinity
        if math.radians(self.angle.pitch) <= self.fov_vertical / 2: # infinity
            a.y = y_inf
            a.x = - math.tan(self.fov_horizontal / 2) * a.y
            b.y = y_inf
            b.x = - a.x
        else:
            an = math.radians(self.angle.pitch) - self.fov_vertical / 2
            a.y = self.altitude / math.tan(an)
            a.x = - math.tan(self.fov_horizontal / 2) * a.y
            b.y = a.y
            b.x = - a.x

        print()