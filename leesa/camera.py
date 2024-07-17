"""Contains the Optical and Sensor parameters.
"""
from .optics import Optics
from .sensor import Sensor
import math
from .geometry import *
from .objwf import *


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
        y_inf = 10  # let's assume the maximum distance
        an = math.radians(self.angle.pitch) + self.fov_vertical / 2
        c = Point3D(0, 0, 0)
        if an < math.radians(90):
            c.y = self.altitude / math.tan(an)
            c.x = - math.tan(self.fov_horizontal / 2) * c.y
        c = Point3D(-c.x, c.y, 0)
        a = Point3D(0, 0, 0)
        b = Point3D(0, 0, 0)
        # verifying A and B in infinity
        if math.radians(self.angle.pitch) <= self.fov_vertical / 2:  # infinity
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


def fov_vs_ground_intersection(cam: Camera = None, distance_maximum=50, debug_obj: str = None) -> list:
    results = []

    if cam is None:
        raise ValueError("The Camera must be non-empty.")

    # create a FOV pyramid
    sp = square_pyramid_from_fov(s=Point3D(0, 0, cam.altitude),
                                 fov_vertical=cam.fov_vertical,
                                 fov_horizontal=cam.fov_horizontal,
                                 angle_pitch=cam.angle.pitch)
    # ground plane
    fl = Plane()
    fl.get_plane_from_points(Point3D(0, 0, 0), Point3D(-10, 10, 0), Point3D(10, 10, 0))
    # intersection between ground plane and FOV pyramid
    l_ca = intersection_plane_plane(sp.sca, fl)
    # the line AB must exist in the front of camera but not behind
    l_ab = Line3D()
    if cam.angle.pitch > math.degrees(cam.fov_vertical / 2):
        l_ab = intersection_plane_plane(sp.sab, fl)
    else:
        l_ab.get_parametric_equation(Point3D(-10, distance_maximum, 0), Point3D(10, distance_maximum, 0))

    l_bd = intersection_plane_plane(sp.sbd, fl)
    l_dc = intersection_plane_plane(sp.sdc, fl)
    # the polygon or trapezoid as result of the intersection between FOV pyramid and floor plane
    tr = Trapezoid()
    tr.create_from_lines(ca=l_ca, ab=l_ab, bd=l_bd, dc=l_dc)
    # trapezoid area
    a = dict()
    a['area'] = trapezoid_area(tr.a, tr.b, tr.c, tr.d)
    results.append(a)

    # estimate the all available positions inside trapezoid for human
    fb_w = 0.5  # human sholder to shoulder width
    fb_d = 0.3  # human chest depth
    #
    # A--E--G-----------B
    #  \ |  |          /
    #   \|  |         /
    #    F--+--------J
    #     \ |       /
    #      \|      /
    #       C-----D
    t = tr.a
    m = []
    tang = (tr.c.x - tr.a.x) / (tr.a.y - tr.c.y)

    while fb_d <= (t.y - tr.c.y):
        # g = Point3D(tr.c.x, t.y, t.z)
        ae = fb_d * tang
        f = Point3D(t.x + ae, t.y - fb_d, t.z)
        j1 = Point3D(f.x + 1, f.y, f.z)
        fj1 = Line3D()
        fj1.get_parametric_equation(f, j1)
        j = line3d_intersection(a=fj1, b=tr.bd)
        l = j.x - f.x
        x = f.x
        while l >= fb_w:
            m.append(Point3D(x, f.y, f.z))
            x += fb_w
            l -= fb_w
        t = f

    a = dict()
    a['people_quantity'] = len(m)
    results.append(a)

    if debug_obj is not None:
        ob = OBJExport()
        ob.add_triangle('fov_sca', sp.s, sp.c, sp.a)
        ob.add_triangle('fov_sab', sp.s, sp.a, sp.b)
        ob.add_triangle('fov_sbd', sp.s, sp.b, sp.d)
        ob.add_triangle('fov_sdc', sp.s, sp.d, sp.c)

        ob.add_poly('floor', Point3D(-10, -10, 0), Point3D(-10, 10, 0), Point3D(10, 10, 0), Point3D(10, -10, 0))

        ob.add_line('fov_floor_ca', tr.c, tr.a)
        ob.add_line('fov_floor_ab', tr.b, tr.a)
        ob.add_line('fov_floor_bd', tr.b, tr.d)
        ob.add_line('fov_floor_dc', tr.c, tr.d)

        # save people positions
        c = 0
        for e in m:
            ob.add_poly(str(c), e, Point3D(e.x + fb_w, e.y, e.z), Point3D(e.x + fb_w, e.y + fb_d, e.z),
                        Point3D(e.x, e.y + fb_d, e.z))
            c += 1

        ob.save(debug_obj)

    return results
