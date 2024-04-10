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


if __name__ == '__main__':
    unittest.main()
