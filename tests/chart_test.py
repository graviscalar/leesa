import unittest
from leesa.chart import Chart


class ChartTests(unittest.TestCase):
    def test_frame_size_none(self):
        """ Test frame size is None """
        try:
            ct = Chart(frame_size=None)
        except ValueError as e:
            self.assertEqual(type(e), ValueError)
        else:
            self.fail('ValueError for frame size is None not raised')

    def test_frame_size_unknown(self):
        """ Test frame size is None """
        try:
            ct = Chart(frame_size='a', width=1, height=1)
        except ValueError as e:
            self.assertEqual(type(e), ValueError)
        else:
            self.fail('ValueError for frame size is unknown not raised')

    def test_width_none(self):
        """ Test width is None """
        try:
            ct = Chart(width=None)
        except ValueError as e:
            self.assertEqual(type(e), ValueError)
        else:
            self.fail('ValueError for width is None not raised')

    def test_height_none(self):
        """ Test width is None """
        try:
            ct = Chart(height=None)
        except ValueError as e:
            self.assertEqual(type(e), ValueError)
        else:
            self.fail('ValueError for height is None not raised')

    def test_offset_negative(self):
        """ Test width is None """
        try:
            ct = Chart(offset=-1)
        except ValueError as e:
            self.assertEqual(type(e), ValueError)
        else:
            self.fail('ValueError for offset is negative not raised')


if __name__ == '__main__':
    unittest.main()
