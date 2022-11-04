import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont
import numpy as np
import json
import datetime
import os

# frame size and frame ratio
_FRAME_SIZE = {
    'QQVGA': {'w': 160, 'h': 120, 'ratio': '4:3'},
    'SXGA': {'w': 1280, 'h': 1024, 'ratio': '5:4'},
    'XGA': {'w': 1024, 'h': 768, 'ratio': '4:3'},
    'SXGAminus': {'w': 1280, 'h': 960, 'ratio': '4:3'},
    's2592': {'w': 2592, 'h': 1944, 'ratio': '4:3'},
    'WXGA_1152': {'w': 1152, 'h': 768, 'ratio': '3:2'},
    'WXGA_1280': {'w': 1280, 'h': 800, 'ratio': '16:10'},
    'HD': {'w': 1280, 'h': 720, 'ratio': '16:9'},
    'FHD': {'w': 1920, 'h': 1080, 'ratio': '16:9'},
    's1440': {'w': 1440, 'h': 720, 'ratio': '18:9'},
    's2560': {'w': 2560, 'h': 1080, 'ratio': '21:9'}
}
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
        if image_name is not None:
            os.makedirs(os.path.dirname(image_name), exist_ok=True)
            self.img.save(image_name)

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
            dt_json = {'exporter': 'Leesa Exporter v0.0.2', 'time': timestamp, 'type': 'rectangle', 'color': 'RGB',
                       'objects': stats}
            with open(json_name, 'w') as outfile:
                json.dump(dt_json, outfile, indent=2)

        return np.array(self.img)
