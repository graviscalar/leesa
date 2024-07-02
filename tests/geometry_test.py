import unittest
from leesa.geometry import *


class TestSum(unittest.TestCase):

    def test_vec3d_dot(self):
        a = Point3D(1, 1, 1)
        b = Point3D(1, 1, 1)
        ret = vec3d_dot(a=a, b=b)
        ground = 3
        self.assertEqual(ret, ground, "Should be empty poly")

    def test_vec3d_cross(self):
        a = Point3D(1, 2, 3)
        b = Point3D(4, 5, 6)
        ret = vec3d_cross(a=a, b=b)
        ground = Point3D(-3, 6, -3)
        self.assertEqual(ret, ground, "Should be empty poly")

    def test_rotation_matrix_x_0(self):
        a = Point3D(-6.96, 10, 5.635)
        c = Point3D(0, 0, 1.72)
        ret = rotation_matrix_x(a=a, angle=10, c=c)
        ground = Point3D(-6.96, 10.527910145688113, 3.839040576373491)
        self.assertEqual(ret, ground, "Should be  Point3D(-6.96, 10.527910145688113, 3.839040576373491)")

    def test_rotation_matrix_x_1(self):
        a = Point3D(-6.96, 10, -2.195)
        c = Point3D(0, 0, 1.72)
        ret = rotation_matrix_x(a=a, angle=10, c=c)
        ground = Point3D(-6.96, 9.168244914556047, -3.8720041297120975)
        self.assertEqual(ret, ground, "Should be  Point3D(-6.96, 9.168244914556047, -3.8720041297120975)")

    def test_plane_from_3points(self):
        a = Point3D(1, 0, 2)
        b = Point3D(2, 1, 1)
        c = Point3D(-1, 2, 1)
        ret = Plane()
        ret.get_plane_from_points(a=a, b=b, c=c)
        ground = Plane(1, 3, 4, -9)
        self.assertEqual(ret, ground, "Should be Plane(1, 3, 4, -9)")

    def test_triangle_area(self):
        a = Point3D(-1, 0, 0)
        b = Point3D(0, 2, 1)
        c = Point3D(1, -1, 2)
        ret = triangle_area(a, b, c)
        ground = 3.5355339059327355
        self.assertEqual(ret, ground, "Should be 3.5355339059327355")



if __name__ == '__main__':
    unittest.main()
