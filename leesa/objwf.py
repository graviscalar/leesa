"""Contains the OBJ exporter
   Simple version
"""
from leesa.geometry import *


class OBJExport():
    def __init__(self):
        self.obj = []
        self.vc = 0

    def add_triangle(self, name: str, a: Point3D, b: Point3D, c: Point3D):
        self.obj.append("v {0} {1} {2}".format(a.x, a.y, a.z))
        self.obj.append("v {0} {1} {2}".format(b.x, b.y, b.z))
        self.obj.append("v {0} {1} {2}".format(c.x, c.y, c.z))
        self.obj.append("o {0}".format(name))
        self.obj.append("f {0} {1} {2}".format(self.vc + 1, self.vc + 2, self.vc + 3))
        self.vc += 3

    def add_line(self, name: str, a: Point3D, b: Point3D):
        self.obj.append("v {0} {1} {2}".format(a.x, a.y, a.z))
        self.obj.append("v {0} {1} {2}".format(b.x, b.y, b.z))
        self.obj.append("o {0}".format(name))
        self.obj.append("l {0} {1}".format(self.vc + 1, self.vc + 2))
        self.vc += 2


    def save(self, fn: str):
        with open(fn, "w") as obj_file:
            for e in self.obj:
                obj_file.write(e)
                obj_file.write("\n")
