import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont
import numpy as np
import json
import datetime
import os

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

_CHART_COLOR_MODE = {
    'single_color': 0,
    'gradient_color': 1

}


class Chart:
    """
    Rectangle chart creation. Image, and JSON files.
    """
    def __init__(self,
                 frame_size: str = 'QQVGA',
                 width: int = 5,
                 height: int = 5,
                 offset: int = 10,
                 offset_at_start: bool = True,
                 border: bool = False,
                 color_background: tuple = (0, 0, 0)
                 ):
        """
        :param frame_size: image size
        :param width: rectangle width
        :param height: rectangle height
        :param offset: offset size between rectangles
        :param offset_at_start: TRUE or FALSE; offset to start first rectangle on left top corner
        :param border: FALSE or TRUE; draw border and pointers
        :param color_background: color as RGB list, be default is [0, 0, 0]
        """
        self.frame_size = frame_size
        self.width = width
        self.height = height
        self.offset = offset
        self.offset_at_start = offset_at_start
        # self.color_mode = color_mode
        # self.color = color
        self.color_background = color_background
        self.border = border

        if frame_size is None:
            raise ValueError("The frame size must be non-empty.")
        if frame_size not in _FRAME_SIZE:
            raise ValueError("The frame size is not exist.")
        if width is None or width <= 0:
            raise ValueError("The rectangle width must be non-empty or > 0.")
        if height is None or height <= 0:
            raise ValueError("The rectangle height must be non-empty or > 0.")
        if offset is None or offset < 0:
            raise ValueError("The offset must be non-empty or >= 0.")
        if color_background is None:
            raise ValueError("The color background must be non-empty.")

        # allocate output image
        frame = _FRAME_SIZE[frame_size]
        f_width = frame['w']
        f_height = frame['h']
        b_size = 0  # border size
        if border is True:
            b_size = f_width // 46  # border size
            f_width += b_size * 2
            f_height += b_size * 2

        img = PIL.Image.new(mode='RGB', size=(f_width, f_height), color=color_background)
        # draw border
        if border is True:
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
            font_h = 9
            font = PIL.ImageFont.truetype("tahoma.ttf", font_h)
            draw.text((b_size + 1, f_height - 1 - font_h - b_size), frame['ratio'], font=font, fill="black")

        self.img = np.array(img)
        # deal with offsets
        self.x_offset = b_size
        self.y_offset = b_size
        if offset_at_start is True:
            self.x_offset += offset
            self.y_offset += offset
        if self.x_offset + width > f_width:
            raise ValueError("The object width or offset is too big. offset + width > frame width")
        if self.y_offset + height > f_height:
            raise ValueError("The object height or offset is too big. offset + height > frame height")
        # calculate number of rectangles
        self.c_h = (f_height - self.y_offset - b_size) // (height + offset)
        self.c_w = (f_width - self.x_offset - b_size) // (width + offset)
        self.qy = self.c_h * self.c_w  # number of rectangles

    def chart_rectangles(self,
                         color_mode: str = 'single_color',
                         color: list = None,
                         image_name: str = None,
                         json_name: str = None
                         ):
        """
        Create chart and save image and JSON files.

        :param color_mode: 'single_color' - all rectangles will be same color,
                           'gradient_color' - colors will be interpolated between first and last colors.
        :param color: color as RGB list, for 'single_color' - [[R, G, B]],
                      for 'gradient_color' - [[R0, G0, B0], [R1, G1, B1]]
        :param image_name: output image file name
        :param json_name: output JSON file name
        :return: chart image as numpy array
        """
        if color_mode is None:
            raise ValueError("The color mode must be non-empty.")
        if color is None:
            raise ValueError("The color list must be non-empty.")

        timestamp = datetime.datetime.now().strftime("%d-%b-%Y(%H-%M-%S)")
        stats = []  # rectangle start coordinates, width, height, color
        # create color table
        color_table = np.zeros(shape=(self.qy, 3), dtype=np.uint8)
        if color_mode == 'gradient_color':
            r_step = (color[1][0] - color[0][0]) / self.qy
            g_step = (color[1][1] - color[0][1]) / self.qy
            b_step = (color[1][2] - color[0][2]) / self.qy
            r = color[0][0]
            g = color[0][1]
            b = color[0][2]
            for i in range(self.qy):
                color_table[i] = [int(r), int(g), int(b)]
                r += r_step
                g += g_step
                b += b_step
            color_table[self.qy - 1] = color[1]  # last color must be exact color, but not a step error approximation
        elif color_mode == 'single_color':
            for i in range(self.qy):
                color_table[i] = color[0]
        # paint rectangles
        color_pos = 0
        y_pos = self.y_offset
        for y in range(self.c_h):
            x_pos = self.x_offset
            for x in range(self.c_w):
                self.img[y_pos:y_pos + self.height, x_pos: x_pos + self.width] = color_table[color_pos]
                stats.append(
                    {'x': x_pos, 'y': y_pos, 'w': self.width, 'h': self.height, 'c': color_table[color_pos].tolist()})
                color_pos += 1
                x_pos = x_pos + self.width + self.offset
            y_pos = y_pos + self.height + self.offset
        # save image
        if image_name is not None:
            os.makedirs(os.path.dirname(image_name), exist_ok=True)
            pil_img = PIL.Image.fromarray(self.img).convert('RGB')
            pil_img.save(image_name)
        # save JSON
        if json_name is not None:
            os.makedirs(os.path.dirname(json_name), exist_ok=True)
            dt_json = {'exporter': 'Leesa Exporter v0.0.1', 'time': timestamp, 'type': 'rectangle', 'objects': stats}
            with open(json_name, 'w') as outfile:
                json.dump(dt_json, outfile, indent=2)

        return self.img
