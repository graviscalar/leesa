"""Contains the geometry base classes and functions for 2D and 3D cartesian space.
   The directions of the XYZ coordinates is the same as for Autodesk 3ss Max 2010
"""
import sys
import numpy as np
import math


class Point2D:
    """The point in 2D cartesian space.

    Arguments:
      x: x coordinate
      y: y coordinate
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Rectangle2D:
    """The rectangle in 2D cartesian space.

    Arguments:
      p_0: x coordinate
      p_1: y coordinate
    """

    def __init__(self, p_0: Point2D, p_1: Point2D):
        self.p_0 = p_0
        self.p_1 = p_1

    def __eq__(self, other):
        return self.p_0 == other.p_0 and self.p_1 == other.p_1


def test_point_in_rectangle2d(r: Rectangle2D, p: Point2D) -> bool:
    """Test if point inside rectangle.

    Arguments:
      r: rectangle type Rectangle2D
      p: point type Point2D
    Returns:
      t: test result; False - not in rectangle, True - inside rectangle
    """
    t = False
    if r.p_0.x <= p.x and p.x <= r.p_1.x and r.p_0.y <= p.y and p.y <= r.p_1.y:
        t = True

    return t


class Circle2D:
    """The circle in 2D cartesian space.

    Arguments:
      c: centre as Point2D
      r: radius
    """

    def __init__(self, c, r):
        self.c = c
        self.r = r

    def __eq__(self, other):
        return self.c == other.c and self.r == other.r


class Point3D:
    """The point in 3D cartesian space.

    Arguments:
      x: x coordinate
      y: y coordinate
      z: z coordinate
    """

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z




def points2d_distance(a, b):
    """Distance between 2 points in 2D space.

    Arguments:
      a: 2D point
      b: 2D point
    Returns:
      A distance between 2 points in 2D space.
    """
    x = a.x - b.x
    y = a.y - b.y
    return np.sqrt((x * x) + (y * y))



class Line3D:
    """The line in 3D cartesian space.
    """

    def __init__(self):
        self.pc_x_0 = 0  # x = x0 + at = x0 + (x1-x0)t
        self.pc_y_0 = 0  # y = y0 + bt = y0 + (y1-y0)t
        self.pc_z_0 = 0  # z = z0 + ct = z0 + (z1-z0)t
        self.pc_a = 0
        self.pc_b = 0
        self.pc_c = 0
        self.p_0 = Point3D(0, 0, 0)  # point p0 on the line
        self.p_1 = Point3D(0, 0, 0)  # point p1 on the line

    def get_parametric_equation(self, p_0, p_1):
        self.p_0 = p_0
        self.p_1 = p_1
        self.pc_x_0 = p_0.x
        self.pc_y_0 = p_0.y
        self.pc_z_0 = p_0.z
        temp = vec3d_sub(p_1, p_0)
        self.pc_a = temp.x
        self.pc_b = temp.y
        self.pc_c = temp.z




class Plane:
    """The plane in 3D cartesian space.

    Arguments:
      a: a coefficient from equation ax + by + cz + d = 0
      b: b coefficient from equation ax + by + cz + d = 0
      c: c coefficient from equation ax + by + cz + d = 0
      d: d coefficient from equation ax + by + cz + d = 0
    """

    def __init__(self, a=sys.float_info.epsilon, b=sys.float_info.epsilon, c=sys.float_info.epsilon,
                 d=sys.float_info.epsilon):
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def __eq__(self, other):
        return self.a == other.a and self.b == other.b and self.c == other.c and self.d == other.d

    def get_z(self, x, y):
        return (- self.a * x - self.b * y - self.d) / self.c

    def get_y(self, x, z):
        return (- self.a * x - self.c * z - self.d) / self.b

    def get_x(self, y, z):
        return (- self.b * y - self.c * z - self.d) / self.a

    # def get_plane_from_points(self, p_1, p_2, p_3):
    #     self.a = (p_2.y * p_3.z) - (p_3.y * p_2.z) - (p_1.y * (p_3.z - p_2.z)) + (p_1.z * (p_3.y - p_2.y))
    #     self.b = p_1.x * (p_3.z - p_2.z) - (p_2.x * p_3.z - p_3.x * p_2.z) + p_1.z * (p_2.x - p_3.x)
    #     self.c = p_1.x * (p_2.y - p_3.y) - p_1.y * (p_2.x - p_3.x) + (p_2.x * p_3.y - p_3.x * p_2.y)
    #     self.d = -1 * p_1.x * (p_2.y * p_3.z - p_3.y * p_2.z) + p_1.y * (p_2.x * p_3.z - p_3.x * p_2.z)
    #     - p_1.z * (p_2.x * p_3.y - p_3.x * p_2.y)

    def get_plane_from_points(self, a, b, c):
        self.a = ((b.y - a.y) * (c.z - a.z)) - ((c.y - a.y) * (b.z - a.z))
        self.b = ((b.z - a.z) * (c.x - a.x)) - ((c.z - a.z) * (b.x - a.x))
        self.c = ((b.x - a.x) * (c.y - a.y)) - ((c.x - a.x) * (b.y - a.y))
        self.d = -((self.a * a.x) + (self.b * a.y) + (self.c * a.z))


def vec3d_sub(a, b):
    return Point3D(a.x - b.x, a.y - b.y, a.z - b.z)


def intersection3d_plane_line(plane, line):
    """Intersection between 3D point and 3D plane.

    Arguments:
      plane: 3D plane
      line: 3D line
    Returns:
      ret: result of intersection; -1 - no intersection, 0 - intersection
      point: 3D point or Intersection between 3D point and 3D plane
    """
    ret = -1
    point = Point3D(0, 0, 0)
    parallel = plane.a * line.pc_a + plane.b * line.pc_b + plane.c * line.pc_c
    if abs(parallel) > sys.float_info.epsilon:
        t = -1 * (plane.a * line.pc_x_0 + plane.b * line.pc_y_0 + plane.c * line.pc_z_0 + plane.d) / parallel
        point.x = line.pc_x_0 + line.pc_a * t
        point.y = line.pc_y_0 + line.pc_b * t
        point.z = line.pc_z_0 + line.pc_c * t
        ret = 0
    return ret, point


def intersection2d_line_line(p1=Point2D(0, 0), p2=Point2D(0, 0), p3=Point2D(0, 0), p4=Point2D(0, 0)):
    """2D intersection between 2 2D lines.

    Arguments:
      p1: the first 2D point in the first 2D line
      p2: the second 2D point in the first 2D line
      p3: the first 2D point in the second 2D line
      p4: the second 2D point in the second 2D line
    Returns:
      ret: result of intersection; -1 - no intersection, 0 - intersection
      point: 2D point or Intersection between between 2 2D lines
    """
    ret = -1
    point = Point2D(0, 0)
    div = (p2.x - p1.x) * (p4.y - p3.y) - (p4.x - p3.x) * (p2.y - p1.y)
    if abs(div) > sys.float_info.epsilon:
        ret = 0
        x = int(((p2.x * p1.y - p1.x * p2.y) * (p4.x - p3.x) - (p4.x * p3.y - p3.x * p4.y) * (p2.x - p1.x)) / div)
        y = int(((p2.x * p1.y - p1.x * p2.y) * (p4.y - p3.y) - (p4.x * p3.y - p3.x * p4.y) * (p2.y - p1.y)) / div)
        point = Point2D(x, y)
    return ret, point



