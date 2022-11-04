import unittest
from leesa.chart import Chart


class ChartTests(unittest.TestCase):
    def test_frame_type_none(self):
        """ Test frame type is None """
        try:
            _ = Chart(frame_type='')
        except ValueError as e:
            self.assertEqual(type(e), ValueError)
        else:
            self.fail('ValueError for frame type is None not raised')

    def test_frame_type_unknown(self):
        """ Test frame type is Unknown """
        try:
            _ = Chart(frame_type='a')
        except ValueError as e:
            self.assertEqual(type(e), ValueError)
        else:
            self.fail('ValueError for frame type is unknown not raised')

    def test_frame_color_none(self):
        """ Test frame background color is empty """
        try:
            _ = Chart(color_background=None)
        except ValueError as e:
            self.assertEqual(type(e), ValueError)
        else:
            self.fail('ValueError for frame background color is empty not raised')

    def test_frame_color_non_right_tuple(self):
        """ Test frame background color is not 3 elements """
        try:
            _ = Chart(color_background=(0, 0))
        except ValueError as e:
            self.assertEqual(type(e), ValueError)
        else:
            self.fail('ValueError for frame background color must be 3 elements tuple is not raised')

    def test_rectangles_color_mode_none(self):
        """ Test rectangles function the color mode is none """
        try:
            ct = Chart()
            ct.rectangles(color_mode='')
        except ValueError as e:
            self.assertEqual(type(e), ValueError)
        else:
            self.fail('ValueError for color mode must be non-empty is not raised')

    def test_rectangles_color_mode_not_exist(self):
        """ Test rectangles function the color mode is not exist """
        try:
            ct = Chart()
            ct.rectangles(color_mode='a')
        except ValueError as e:
            self.assertEqual(type(e), ValueError)
        else:
            self.fail('ValueError for color mode is not exist is not raised')

    def test_rectangle_width_negative(self):
        """ Test rectangle width is negative """
        try:
            ct = Chart()
            ct.rectangles(rectangle_width=-1)
        except ValueError as e:
            self.assertEqual(type(e), ValueError)
        else:
            self.fail('ValueError for rectangle width must be non-empty or > 0 not raised')

    def test_rectangle_height_negative(self):
        """ Test rectangle height is negative """
        try:
            ct = Chart()
            ct.rectangles(rectangle_height=-1)
        except ValueError as e:
            self.assertEqual(type(e), ValueError)
        else:
            self.fail('ValueError for rectangle height must be non-empty or > 0 not raised')

    def test_rectangle_start_x_negative(self):
        """ Test start_x is negative """
        try:
            ct = Chart()
            ct.rectangles(start_x=-1)
        except ValueError as e:
            self.assertEqual(type(e), ValueError)
        else:
            self.fail('ValueError for start_x must be non-empty or = 0 not raised')

    def test_rectangle_start_y_negative(self):
        """ Test start_y is negative """
        try:
            ct = Chart()
            ct.rectangles(start_y=-1)
        except ValueError as e:
            self.assertEqual(type(e), ValueError)
        else:
            self.fail('ValueError for start_y must be non-empty or = 0 not raised')

    def test_rectangle_gap_x_negative(self):
        """ Test gap_x is negative """
        try:
            ct = Chart()
            ct.rectangles(gap_x=-1)
        except ValueError as e:
            self.assertEqual(type(e), ValueError)
        else:
            self.fail('ValueError for gap_x must be non-empty or = 0 not raised')

    def test_rectangle_gap_y_negative(self):
        """ Test gap_y is negative """
        try:
            ct = Chart()
            ct.rectangles(gap_y=-1)
        except ValueError as e:
            self.assertEqual(type(e), ValueError)
        else:
            self.fail('ValueError for gap_y must be non-empty or = 0 not raised')



if __name__ == '__main__':
    unittest.main()
