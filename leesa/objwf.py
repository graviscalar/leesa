"""Contains the OBJ exporter
   Simple version
"""
from leesa.geometry import *


class OBJExport():
    def __init__(self):
        self.obj = []
        self.vc = 0

    def add_triangle(self, name: str, a: Point3D, b: Point3D, c: Point3D):
        self.obj.append("#")
        self.obj.append("# object {0}".format(name))
        self.obj.append("#")
        self.obj.append("\n")
        self.obj.append("v  {0:.4f} {1:.4f} {2:.4f}".format(a.x, a.y, a.z))
        self.obj.append("v  {0:.4f} {1:.4f} {2:.4f}".format(b.x, b.y, b.z))
        self.obj.append("v  {0:.4f} {1:.4f} {2:.4f}".format(c.x, c.y, c.z))
        self.obj.append("# 3 vertices")
        self.obj.append("\n")
        self.obj.append("o {0}".format(name))
        self.obj.append("g {0}".format(name))
        self.obj.append("f {0} {1} {2}".format(self.vc + 1, self.vc + 2, self.vc + 3))
        self.obj.append("\n")
        self.vc += 3

    def add_line(self, name: str, a: Point3D, b: Point3D):
        self.obj.append("#")
        self.obj.append("# shape {0}".format(name))
        self.obj.append("#")
        self.obj.append("\n")
        self.obj.append("v  {0:.4f} {1:.4f} {2:.4f}".format(a.x, a.y, a.z))
        self.obj.append("v  {0:.4f} {1:.4f} {2:.4f}".format(b.x, b.y, b.z))
        self.obj.append("# 2 vertices")
        self.obj.append("\n")
        self.obj.append("o {0}".format(name))
        self.obj.append("g {0}".format(name))
        self.obj.append("l {0} {1}".format(self.vc + 1, self.vc + 2))
        self.obj.append("\n")
        self.vc += 2

    def save(self, fn: str):
        with open(fn, "w") as obj_file:
            for e in self.obj:
                obj_file.write(e)
                if e != "\n":
                    obj_file.write("\n")
