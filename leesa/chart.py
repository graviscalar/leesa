import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont
import numpy as np
import json
import datetime
import os
from enum import Enum
import itertools
from leesa.image import *

# chart color type
_CHART_COLOR_MODE = {
    'single_color': 0,
    'gradient_color': 1
}


class Chart:
    """
    Rectangle chart creation. Image, and JSON files in the output.

    Chart with single color:

    ct = Chart(frame_type='HD', color_background=(255, 255, 255))
    ct.rectangles(color_mode='single_color',
                  rectangle_color=[[0, 255, 0]],
                  image_name='img/out/single_color.png',
                  json_name='img/out/single_color.json')

    Chart with gradient colors:

    ct = Chart(frame_type='HD', color_background=(255, 255, 255))
    ct.rectangles(color_mode='gradient_color',
                  rectangle_color=[[255, 255, 0], [0, 0, 255]],
                  image_name='img/out/gradient_color.png',
                  json_name='img/out/gradient_color.json')

    """

    def __init__(self, frame_type: str = 'QQVGA', color_background: tuple = (0, 0, 0)):
        """

        :param frame_type: key value taken from the _FRAME_SIZE dictionary
        :param color_background: color for image background fill, color as RGB list
        """
        fr = FrameResolution()
        _FRAME_SIZE = fr.get_dict()

        self.frame_type = frame_type
        if frame_type is None:
            raise ValueError("The frame size must be non-empty.")
        if frame_type not in _FRAME_SIZE:
            raise ValueError("The frame size is not exist.")
        if color_background is None:
            raise ValueError("The color background must be non-empty.")
        if len(color_background) != 3:
            raise ValueError("The color background must be 3 elements tuple.")
        # allocate output image
        self.frame = _FRAME_SIZE[frame_type]
        self.img = PIL.Image.new(mode='RGB', size=(self.frame['w'], self.frame['h']), color=color_background)

    def border_draw(self) -> None:
        b_size = self.frame['w'] // 46  # border size
        f_width = self.frame['w'] + b_size * 2
        f_height = self.frame['h'] + b_size * 2
        img = PIL.Image.new(mode='RGB', size=(f_width, f_height), color=(0, 0, 0))

        draw = PIL.ImageDraw.Draw(img)
        # borders
        draw.polygon([(0, 0), (f_width - 1, 0), (f_width - 1, b_size - 1), (0, b_size - 1)], fill=(0, 0, 0))
        draw.polygon(
            [(0, f_height - b_size), (f_width - 1, f_height - b_size), (f_width - 1, f_height - 1),
             (0, f_height - 1)],
            fill=(0, 0, 0))
        draw.polygon([(0, 0), (b_size - 1, 0), (b_size - 1, f_height - 1), (0, f_height - 1)], fill=(0, 0, 0))
        draw.polygon(
            [(f_width - b_size, 0), (f_width - 1, 0), (f_width - 1, f_height - 1),
             (f_width - b_size, f_height - 1)],
            fill=(0, 0, 0))
        # triangles
        # white triangles
        b2 = b_size // 2
        w2 = f_width // 2
        h2 = f_height // 2
        # top triangle
        draw.polygon([(w2 - b2, 0),
                      (w2 + b2, 0),
                      (w2, b_size)],
                     fill=(255, 255, 255))
        # bottom triangle
        draw.polygon([(w2 - b2, f_height - 1),
                      (w2 + b2, f_height - 1),
                      (w2, f_height - 1 - b_size)],
                     fill=(255, 255, 255))
        # left side triangles
        draw.polygon([(0, h2 - b2),
                      (b_size, h2),
                      (0, h2 + b2)],
                     fill=(255, 255, 255))
        draw.polygon([(0, b_size),
                      (b_size, b2 + b_size),
                      (0, b_size + b_size)],
                     fill=(255, 255, 255))
        draw.polygon([(0, f_height - b_size * 2),
                      (b_size, f_height - b2 - b_size),
                      (0, f_height - b_size)],
                     fill=(255, 255, 255))
        # right side triangles
        draw.polygon([(f_width - 1, h2 - b2),
                      (f_width - 1 - b_size, h2),
                      (f_width - 1, h2 + b2)],
                     fill=(255, 255, 255))
        draw.polygon([(f_width - 1, b_size),
                      (f_width - 1 - b_size, b_size + b2),
                      (f_width - 1, b_size + b_size)],
                     fill=(255, 255, 255))
        draw.polygon([(f_width - 1, f_height - b_size * 2),
                      (f_width - 1 - b_size, f_height - b_size - b2),
                      (f_width - 1, f_height - b_size)],
                     fill=(255, 255, 255))
        # display ratio
        img.paste(self.img, (b_size, b_size))
        # print ratio
        font_h = 9
        font = PIL.ImageFont.truetype("tahoma.ttf", font_h)
        draw.text((b_size + 1, f_height - 1 - font_h - b_size), self.frame['ratio'], font=font, fill="black")
        self.img = img

    def img_save(self, image_name: str = None) -> None:
        """
        Save an image to carrier

        :param image_name: the image file name with path and extension
        :return: None
        """
        # save image
        img_save(img=self.img, image_name=image_name)

    def rectangles(self,
                   color_mode: str = 'single_color',
                   rectangle_color: list = None,
                   rectangle_width: int = 5,
                   rectangle_height: int = 5,
                   start_x: int = 0,
                   start_y: int = 0,
                   gap_x: int = 5,
                   gap_y: int = 5,
                   border: bool = False,
                   image_name: str = None,
                   json_name: str = None
                   ) -> np.ndarray:
        """
        Create chart and save image and JSON files.

        :param color_mode: 'single_color' - all rectangles will be same color,
                           'gradient_color' - colors will be interpolated between first and last colors.
        :param rectangle_color: color as RGB list, for 'single_color' - [[R, G, B]],
                      for 'gradient_color' - [[R0, G0, B0], [R1, G1, B1]]
        :param rectangle_width: rectangle width
        :param rectangle_height: rectangle height
        :param start_x: first rectangle start position on X axis
        :param start_y: first rectangle start position on Y axis
        :param gap_x: gap between 2 rectangles on X axis
        :param gap_y: gap between 2 rectangles on Y axis
        :param border: draw border with triangles. True or False.
        :param image_name: output image file name
        :param json_name: output JSON file name
        :return: chart image as numpy array
        """

        if color_mode is None:
            raise ValueError("The color mode must be non-empty.")
        if color_mode not in _CHART_COLOR_MODE:
            raise ValueError("The color mode is not exist.")
        if rectangle_color is None:
            raise ValueError("The color list must be non-empty.")
        if rectangle_width is None or rectangle_width <= 0:
            raise ValueError("The rectangle width must be non-empty or > 0.")
        if rectangle_height is None or rectangle_height <= 0:
            raise ValueError("The rectangle height must be non-empty or > 0.")
        if start_x is None or start_x < 0:
            raise ValueError("The start_x must be non-empty or >= 0.")
        if start_y is None or start_y < 0:
            raise ValueError("The start_y must be non-empty or >= 0.")
        if gap_x is None or gap_x < 0:
            raise ValueError("The gap_x must be non-empty or >= 0.")
        if gap_y is None or gap_y < 0:
            raise ValueError("The gap_y must be non-empty or >= 0.")

        # calculate number of rectangles
        # rectangles quantity in horizontal direction
        rqx = (self.frame['w'] - 2 * start_x) // (rectangle_width + gap_x)
        # rectangles quantity in vertical direction
        rqy = (self.frame['h'] - 2 * start_y) // (rectangle_height + gap_y)
        # rectangles quantity
        rq = rqx * rqy

        timestamp = datetime.datetime.now().strftime("%d-%b-%Y(%H-%M-%S)")

        stats = []  # rectangle start coordinates, width, height, color
        # create color table
        color_table = np.zeros(shape=(rq, 3), dtype=np.uint8)
        if color_mode == 'gradient_color':
            r_step = (rectangle_color[1][0] - rectangle_color[0][0]) / rq
            g_step = (rectangle_color[1][1] - rectangle_color[0][1]) / rq
            b_step = (rectangle_color[1][2] - rectangle_color[0][2]) / rq
            r = rectangle_color[0][0]
            g = rectangle_color[0][1]
            b = rectangle_color[0][2]
            for i in range(rq):
                color_table[i] = [int(r), int(g), int(b)]
                r += r_step
                g += g_step
                b += b_step
            color_table[rq - 1] = rectangle_color[
                1]  # last color must be exact color, but not a step error approximation
        elif color_mode == 'single_color':
            for i in range(rq):
                color_table[i] = rectangle_color[0]

        img = np.array(self.img)  # allocate numpy image
        # paint rectangles
        color_pos = 0
        pos_y = start_y
        for y in range(rqy):
            pos_x = start_x
            for x in range(rqx):
                img[pos_y:pos_y + rectangle_height, pos_x: pos_x + rectangle_width] = color_table[color_pos]
                stats.append(
                    {'x': pos_x, 'y': pos_y, 'w': rectangle_width, 'h': rectangle_height,
                     'c': color_table[color_pos].tolist()})
                color_pos += 1
                pos_x = pos_x + rectangle_width + gap_x
            pos_y = pos_y + rectangle_height + gap_y

        self.img = PIL.Image.fromarray(img).convert('RGB')  # convert numpy image to PIL image
        # add border if required
        if border is True:
            self.border_draw()
        # save image
        self.img_save(image_name)
        # save JSON
        if json_name is not None:
            os.makedirs(os.path.dirname(json_name), exist_ok=True)
            dt_json = {'exporter': 'Leesa Exporter v0.1.6', 'time': timestamp, 'type': 'rectangle', 'color': 'RGB',
                       'objects': stats}
            with open(json_name, 'w') as outfile:
                json.dump(dt_json, outfile, indent=2)

        return np.array(self.img)

    def ramp_draw(self,
                  start_x: int = 0,
                  start_y: int = 0,
                  element_width: int = 1,
                  element_height: int = 16,
                  start_color: tuple = (0, 0, 0),
                  end_color: tuple = (0, 0, 0),
                  ramp_size: int = 256,
                  direction: int = 0) -> list:
        stats = []

        img = np.array(self.img)  # allocate numpy image

        r_step = (end_color[0] - start_color[0]) / (ramp_size - 1)
        g_step = (end_color[1] - start_color[1]) / (ramp_size - 1)
        b_step = (end_color[2] - start_color[2]) / (ramp_size - 1)

        # create color table
        color_table = np.zeros(shape=(ramp_size, 3), dtype=np.uint8)
        r = start_color[0]
        g = start_color[1]
        b = start_color[2]
        for i in range(ramp_size - 1):
            color_table[i] = [int(r), int(g), int(b)]
            r += r_step
            g += g_step
            b += b_step
        color_table[ramp_size - 1] = end_color

        pos_x = start_x
        pos_y = start_y
        for i in range(ramp_size):
            img[pos_y:pos_y + element_height, pos_x: pos_x + element_width] = color_table[i]
            if direction == 0:
                pos_x += element_width
            else:
                pos_y += element_height
            e = {'x': pos_x, 'y': pos_y, 'w': element_width, 'h': element_height, 'c': color_table[i].tolist()}
            stats.append(e)

        self.img = PIL.Image.fromarray(img).convert('RGB')  # convert numpy image to PIL image

        return stats

    def ramps(self,
              element_width: int = 1,
              element_height: int = 16,
              ramp_size: int = 256,
              image_name: str = None,
              json_name: str = None,
              ):
        timestamp = datetime.datetime.now().strftime("%d-%b-%Y(%H-%M-%S)")

        c = Colors()
        _COLORS = c.get_dict()

        a = [[_COLORS['BL'], _COLORS['W']],
             [_COLORS['BL'], _COLORS['R']],
             [_COLORS['W'], _COLORS['R']],
             [_COLORS['BL'], _COLORS['G']],
             [_COLORS['W'], _COLORS['G']],
             [_COLORS['BL'], _COLORS['B']],
             [_COLORS['W'], _COLORS['B']],
             [_COLORS['BL'], _COLORS['C']],
             [_COLORS['W'], _COLORS['C']],
             [_COLORS['BL'], _COLORS['M']],
             [_COLORS['W'], _COLORS['M']],
             [_COLORS['BL'], _COLORS['Y']],
             [_COLORS['W'], _COLORS['Y']]
             ]
        x_step = 8
        y_step = 8
        start_x = x_step
        start_y = y_step

        stats = []

        for e in a:
            r = self.ramp_draw(start_x=start_x,
                               start_y=start_y,
                               start_color=e[0],
                               end_color=e[1],
                               element_width=element_width,
                               element_height=element_height,
                               ramp_size=ramp_size,
                               direction=0,
                               )
            start_y = start_y + y_step + element_height
            stats.extend(r)

        start_x = x_step + len(a) * element_height + (len(a)) * x_step
        start_y = y_step

        for e in a:
            r = self.ramp_draw(start_x=start_x,
                               start_y=start_y,
                               start_color=e[0],
                               end_color=e[1],
                               element_width=element_height,
                               element_height=element_width,
                               ramp_size=ramp_size,
                               direction=1)
            start_x = start_x + x_step + element_height
            stats.extend(r)

        # save image
        self.img_save(image_name)
        # save JSON
        if json_name is not None:
            os.makedirs(os.path.dirname(json_name), exist_ok=True)
            dt_json = {'exporter': 'Leesa Exporter v0.1.6', 'time': timestamp, 'type': 'ramps', 'color': 'RGB',
                       'objects': stats}
            with open(json_name, 'w') as outfile:
                json.dump(dt_json, outfile, indent=2)

    def combinations(self,
                     element_width: int = 16,
                     element_height: int = 16,
                     image_name: str = None,
                     json_name: str = None,
                     ):
        timestamp = datetime.datetime.now().strftime("%d-%b-%Y(%H-%M-%S)")

        c = Colors()
        _COLORS = c.get_dict()

        a = [_COLORS['BL'], _COLORS['W'], _COLORS['R'], _COLORS['G'],
             _COLORS['B'], _COLORS['C'], _COLORS['M'], _COLORS['Y']]
        ct = list(itertools.permutations(a, 2))

        gap_x = 8
        gap_y = 8
        start_x = gap_x
        start_y = gap_y
        x2 = element_width // 2
        y2 = element_height // 2

        stats = []
        #   estimating the maximum number of the elements in the image
        # rectangles quantity in horizontal direction
        rqx = (self.frame['w']) // (element_width + gap_x)
        # rectangles quantity in vertical direction
        rqy = (self.frame['h']) // (element_height + gap_y)
        c_limit = len(ct)
        if rqx * rqy < c_limit:
            c_limit = rqx * rqy

        img = np.array(self.img)  # allocate numpy image

        color_pos = 0

        # vertical combinations
        pos_y = start_y
        for y in range(rqy):
            if color_pos == c_limit:
                break
            pos_x = start_x
            for x in range(rqx):
                if color_pos == c_limit:
                    break
                img[pos_y:pos_y + element_height, pos_x: pos_x + x2] = ct[color_pos][0]
                img[pos_y:pos_y + element_height, pos_x + x2: pos_x + element_width] = ct[color_pos][1]
                stats.append(
                    {'x': pos_x, 'y': pos_y, 'w': x2, 'h': element_height,
                     'c': ct[color_pos][0]})
                stats.append(
                    {'x': pos_x + x2, 'y': pos_y, 'w': x2, 'h': element_height,
                     'c': ct[color_pos][0]})
                color_pos += 1
                pos_x = pos_x + element_width + gap_x
            pos_y = pos_y + element_height + gap_y

        # horizontal combinations
        color_pos = 0
        for y in range(rqy):
            if color_pos == c_limit:
                break
            pos_x = start_x
            for x in range(rqx):
                if color_pos == c_limit:
                    break
                img[pos_y:pos_y + y2, pos_x: pos_x + element_width] = ct[color_pos][0]
                img[pos_y + y2:pos_y + element_height, pos_x: pos_x + element_width] = ct[color_pos][1]
                stats.append(
                    {'x': pos_x, 'y': pos_y, 'w': element_width, 'h': y2,
                     'c': ct[color_pos][0]})
                stats.append(
                    {'x': pos_x, 'y': pos_y + y2, 'w': element_width, 'h': y2,
                     'c': ct[color_pos][0]})

                color_pos += 1
                pos_x = pos_x + element_width + gap_x
            pos_y = pos_y + element_height + gap_y

        self.img = PIL.Image.fromarray(img).convert('RGB')  # convert numpy image to PIL image
        # save image
        self.img_save(image_name)
        # save JSON
        if json_name is not None:
            os.makedirs(os.path.dirname(json_name), exist_ok=True)
            dt_json = {'exporter': 'Leesa Exporter v0.1.6', 'time': timestamp, 'type': 'ramps', 'color': 'RGB',
                       'objects': stats}
            with open(json_name, 'w') as outfile:
                json.dump(dt_json, outfile, indent=2)

    def edge_test(self,
                  element_width: int = 3,
                  element_height: int = 12,
                  image_name: str = None,
                  json_name: str = None,
                  ):
        timestamp = datetime.datetime.now().strftime("%d-%b-%Y(%H-%M-%S)")

        c = Colors()
        _COLORS = c.get_dict()

        a = [_COLORS['BL'], _COLORS['W'], _COLORS['R'], _COLORS['G'],
             _COLORS['B'], _COLORS['C'], _COLORS['M'], _COLORS['Y']]
        ct = list(itertools.permutations(a, 2))

        gap_x = 4
        gap_y = 3
        start_x = gap_x
        start_y = gap_y
        bar_border = 2
        x2 = element_width // 2
        y2 = element_height // 2

        stats = []
        # bar width
        bar_width = (gap_x + element_width) * 255 + gap_x
        bar_height = element_height + bar_border * 2

        #  estimating the maximum number of the elements in the image
        # rectangles quantity in vertical direction
        rqy = (self.frame['h']) // (bar_height + gap_y)
        c_limit = len(ct)
        if rqy < c_limit:
            c_limit = rqy

        img = np.array(self.img)  # allocate numpy image

        color_pos = 0

        # vertical combinations
        pos_y = start_y
        for y in range(rqy):
            if color_pos == c_limit:
                break
            img[pos_y:pos_y + bar_height, start_x: start_x + bar_width] = ct[color_pos][0]
            # add the vertical lines
            pos_x = start_x
            # prepare the color transition table
            color_table = np.zeros(shape=(256, 3), dtype=np.uint8)
            r_step = (ct[color_pos][1][0] - ct[color_pos][0][0]) / 255
            g_step = (ct[color_pos][1][1] - ct[color_pos][0][1]) / 255
            b_step = (ct[color_pos][1][2] - ct[color_pos][0][2]) / 255
            r = ct[color_pos][0][0]
            g = ct[color_pos][0][1]
            b = ct[color_pos][0][2]
            for i in range(256):
                color_table[i] = [int(r), int(g), int(b)]
                r += r_step
                g += g_step
                b += b_step
                color_table[-1] = ct[color_pos][1]

            for i in range(0, 256):
                img[pos_y + bar_border:pos_y + bar_border + element_height, pos_x: pos_x + element_width] = color_table[
                    i]
                pos_x = pos_x + element_width + gap_x
                stats.append(
                    {'x': pos_x, 'y': pos_y, 'w': element_width, 'h': element_height,
                     'c': color_table[i].tolist()})

            color_pos += 1
            pos_y = pos_y + bar_height + gap_y

        self.img = PIL.Image.fromarray(img).convert('RGB')  # convert numpy image to PIL image
        # save image
        self.img_save(image_name)
        # save JSON
        if json_name is not None:
            os.makedirs(os.path.dirname(json_name), exist_ok=True)
            dt_json = {'exporter': 'Leesa Exporter v0.1.6', 'time': timestamp, 'type': 'ramps', 'color': 'RGB',
                       'objects': stats}
            with open(json_name, 'w') as outfile:
                json.dump(dt_json, outfile, indent=2)
