"""Contains the geometry base classes and functions for 2D and 3D cartesian space.
   The directions of the XYZ coordinates is the same as for Autodesk 3ss Max 2010
"""
import sys
import numpy as np
import math


class CamAngle:
    def __init__(self, pitch: float = 0, roll: float = 0, yaw: float = 0):
        self.pitch = pitch
        self.roll = roll
        self.yaw = yaw


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

    def sub(self, a):
        return Point3D(self.x - a.x, self.y - a.y, self.z - a.z)

    def add(self, a):
        return Point3D(self.x + a.x, self.y + a.y, self.z + a.z)


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

    parametric form ----------------------------------
    x = x0 + at
    y = y0 + bt
    z = z0 + ct

    a, b, c from directional vector (colinear to line)
    p = ai + bj + ck

    canonical form -----------------------------------
    x - x0    y - y0   z - z0
    ------ = ------- = ------
      a         b        c
    """

    def __init__(self, x0: float = 0, y0: float = 0, z0: float = 0, a: float = 0, b: float = 0, c: float = 0):
        self.x0 = x0  # x = x0 + at = x0 + (x1-x0)t
        self.y0 = y0  # y = y0 + bt = y0 + (y1-y0)t
        self.z0 = z0  # z = z0 + ct = z0 + (z1-z0)t
        self.a = a
        self.b = b
        self.c = c
        self.p0 = Point3D(0, 0, 0)  # point p0 on the line
        self.p1 = Point3D(0, 0, 0)  # point p1 on the line

    def get_parametric_equation(self, p0, p1):
        self.p0 = p0
        self.p1 = p1
        self.x0 = p0.x
        self.y0 = p0.y
        self.z0 = p0.z
        temp = vec3d_sub(p1, p0)
        self.a = temp.x
        self.b = temp.y
        self.c = temp.z

    def get_point_by_t(self, t) -> Point3D:
        return Point3D(self.x0 + t * self.a, self.y0 + t * self.b, self.z0 + t * self.c)


def line3d_intersection(a: Line3D, b: Line3D):
    i = None
    c = np.array([[b.x0 - a.x0, b.y0 - a.y0, b.z0 - a.z0], [a.a, a.b, a.c], [b.a, b.b, b.c]])
    d = np.linalg.det(c)
    c = np.array([[a.a, a.b, a.c], [b.a, b.b, b.c]])
    r = np.linalg.matrix_rank(c)
    # print(d, r)
    if d == 0 and r == 2:
        t = (b.x0 * b.b + b.a * a.y0 - b.a * b.y0 - a.x0 * b.b) / (a.a * b.b - b.a * a.b)
        i = a.get_point_by_t(t)

    return i


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

    def get_plane_from_points(self, a, b, c):
        self.a = ((b.y - a.y) * (c.z - a.z)) - ((c.y - a.y) * (b.z - a.z))
        self.b = ((b.z - a.z) * (c.x - a.x)) - ((c.z - a.z) * (b.x - a.x))
        self.c = ((b.x - a.x) * (c.y - a.y)) - ((c.x - a.x) * (b.y - a.y))
        self.d = -((self.a * a.x) + (self.b * a.y) + (self.c * a.z))

    def get_normal(self) -> Point3D:
        return Point3D(self.a, self.b, self.c)


def vec3d_sub(a, b):
    return Point3D(a.x - b.x, a.y - b.y, a.z - b.z)


def vec3d_dot(a: Point3D, b: Point3D):
    return a.x * b.x + a.y * b.y + a.z * b.z


def vec3d_cross(a: Point3D, b: Point3D) -> Point3D:
    return Point3D(a.y * b.z - a.z * b.y, a.z * b.x - a.x * b.z, a.x * b.y - a.y * b.x)


def intersection_plane_plane(a: Plane, b: Plane):
    l = None
    # verify determinants
    cx = np.array([[a.b, a.c], [b.b, b.c]])
    dx = np.linalg.det(cx)
    cy = np.array([[a.c, a.a], [b.c, b.a]])
    dy = np.linalg.det(cy)
    cz = np.array([[a.a, a.b], [b.a, b.b]])
    dz = np.linalg.det(cz)
    if dx != 0 or dy != 0 or dz != 0:
        # calculating line vector
        an = a.get_normal()
        bn = b.get_normal()
        lv = vec3d_cross(an, bn)  # line vector
        # calculating point on line
        # selecting the right determinant
        if dx != 0:
            a1 = cx
            b1 = np.array([-a.d, -b.d])
            p = np.linalg.solve(a1, b1)  # point on the line
            l = Line3D(x0=0, y0=p[0], z0=p[1], a=lv.x, b=lv.y, c=lv.z)
        elif dy != 0:
            a1 = cy
            b1 = np.array([-a.d, -b.d])
            p = np.linalg.solve(a1, b1)  # point on the line
            l = Line3D(x0=p[0], y0=0, z0=p[1], a=lv.x, b=lv.y, c=lv.z)
        elif dz != 0:
            a1 = cz
            b1 = np.array([-a.d, -b.d])
            p = np.linalg.solve(a1, b1)  # point on the line
            l = Line3D(x0=p[0], y0=p[1], z0=0, a=lv.x, b=lv.y, c=lv.z)

    return l


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


#  polyhedras


class Trapezoid:
    """The Square pyramid in 3D cartesian space.

   A-----B
   |     |
   |     |
   |     |
   |     |
   |     |
   C-----D

    Arguments:
      a: a coordinate
      b: b coordinate
      c: c coordinate
      d: d coordinate
    """

    def __init__(self,
                 a: Point3D = Point3D(0, 0, 0), b: Point3D = Point3D(0, 1, 0),
                 c: Point3D = Point3D(1, 1, 0), d: Point3D = Point3D(1, 0, 0)):
        self.a = a
        self.b = b
        self.c = c
        self.d = d


    def create_from_lines(self, ca: Line3D, ab: Line3D, bd: Line3D, dc: Line3D):
        self.c = line3d_intersection(a=ca, b=dc)
        self.a = line3d_intersection(a=ca, b=ab)
        self.b = line3d_intersection(a=ab, b=bd)
        self.d = line3d_intersection(a=bd, b=dc)


class SquarePyramid:
    """The Square pyramid in 3D cartesian space.

   A-----B
   |\   /|
   | \ / |
   |  S  |
   | / \ |
   |/   \|
   C-----D

    Arguments:
      a: a coordinate
      b: b coordinate
      c: c coordinate
      d: d coordinate
      s: s coordinate
    """

    def __init__(self, a: Point3D, b: Point3D, c: Point3D, d: Point3D, s: Point3D):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.s = s
        self.sca = Plane()
        self.sca.get_plane_from_points(s, c, a)
        self.sab = Plane()
        self.sab.get_plane_from_points(s, a, b)
        self.sbd = Plane()
        self.sbd.get_plane_from_points(s, b, d)
        self.sdc = Plane()
        self.sdc.get_plane_from_points(s, d, c)


def square_pyramid_from_fov(s, fov_vertical, fov_horizontal,
                            pyramid_height: float = 50,
                            angle_pitch: float = 0) -> SquarePyramid:
    # Square triangle oriented to vector (0, 1, 0)
    # A calculation
    a = Point3D(x=s.x - pyramid_height * math.tan(fov_horizontal / 2),
                y=s.y + pyramid_height,
                z=s.z + pyramid_height * math.tan(fov_vertical / 2))
    # B calculation
    b = Point3D(x=-a.x, y=a.y, z=a.z)
    # C calculation
    c = Point3D(x=a.x, y=a.y, z=2 * s.z - a.z)
    # D calculation
    d = Point3D(x=b.x, y=b.y, z=c.z)
    # Pitch or X rotation
    a = rotation_matrix_x(a=a, angle=angle_pitch, c=s)
    b = rotation_matrix_x(a=b, angle=angle_pitch, c=s)
    c = rotation_matrix_x(a=c, angle=angle_pitch, c=s)
    d = rotation_matrix_x(a=d, angle=angle_pitch, c=s)

    return SquarePyramid(a=a, b=b, c=c, d=d, s=s)


# rotations with simple basis translation

def rotation_matrix_x(a: Point3D, angle: float, c: Point3D) -> Point3D:
    co = math.cos(math.radians(angle))
    si = math.sin(math.radians(angle))
    b = a.sub(a=c)
    m1 = [b.x, b.y, b.z]
    # x rotate
    m2 = [[1, 0, 0],
          [0, co, -si],
          [0, si, co]]
    b = np.dot(m1, m2)
    return Point3D(b[0], b[1], b[2]).add(a=c)


def rotation_matrix_y(a: Point3D, angle: float, c: Point3D) -> Point3D:
    co = math.cos(math.radians(angle))
    si = math.sin(math.radians(angle))
    b = a.sub(a=c)
    m1 = [b.x, b.y, b.z]
    # y rotate
    m2 = [[co, 0, si],
          [0, 1, 0],
          [-si, 0, co]]
    b = np.dot(m1, m2)
    return Point3D(b[0], b[1], b[2]).add(a=c)
