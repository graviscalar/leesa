import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont
import json
import datetime
import itertools
import numpy as np
from leesa.image import *
from leesa.tools import *
from datetime import datetime


class ODChart:
    """
    Object Detection chart creation. Image, and JSON files in the output.


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
        self.color_background = color_background
        self.scales = []
        self.scales_fixed = [35, 34, 33, 32, 31, 30, 29, 28, 27, 26, 25, 24, 23, 22, 21, 20, 19,
                             18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3]
        self.scale_size = 4  # the size of scale unit in the pixels

    def scale_mode_to_string(self, mode):
        r = ''
        if mode == 0:
            r = 'Scale by rectangle width. '
        elif mode == 1:
            r = 'Scale by face width. '
        elif mode == 2:
            r = 'Scale by eyes distance. '
        return r

    def rect_rect_inside_test(self, r1, r2):
        inside = 0
        if r2['a']['x'] >= r1['a']['x']:
            if r2['a']['x'] <= r1['b']['x']:
                if r2['a']['y'] >= r1['a']['y']:
                    if r2['a']['y'] <= r1['d']['y']:
                        inside = inside + 1
        if r2['b']['x'] >= r1['a']['x']:
            if r2['b']['x'] <= r1['b']['x']:
                if r2['b']['y'] >= r1['a']['y']:
                    if r2['b']['y'] <= r1['d']['y']:
                        inside = inside + 1
        if r2['c']['x'] >= r1['a']['x']:
            if r2['c']['x'] <= r1['b']['x']:
                if r2['c']['y'] >= r1['a']['y']:
                    if r2['c']['y'] <= r1['d']['y']:
                        inside = inside + 1
        if r2['d']['x'] >= r1['a']['x']:
            if r2['d']['x'] <= r1['b']['x']:
                if r2['d']['y'] >= r1['a']['y']:
                    if r2['d']['y'] <= r1['d']['y']:
                        inside = inside + 1
        return inside

    def rect_rect_intersection_test(self, r1, r2):
        inside = self.rect_rect_inside_test(r1, r2)
        inside = inside + self.rect_rect_inside_test(r2, r1)
        return inside

    def search_free_position(self, obj_map, scale, size, offset, img_w, img_h, font_v, font_h):
        # x_step = scale
        # y_step = scale
        x_step = scale
        y_step = scale
        free_pos = False
        ret_x = 0
        ret_y = 0

        x_start, y_start = 0, 0

        x_end = img_w - size['w'] - 1 - font_v
        y_end = img_h - size['h'] - 1 - font_h

        y = y_start
        while y < y_end:
            x = x_start
            while x < x_end:
                a = {'x': x, 'y': y}
                b = {'x': x + size['w'], 'y': y}
                c = {'x': x, 'y': y + size['h'] + font_h}
                d = {'x': x + size['w'] + font_v, 'y': y + size['h'] + font_h}
                obj_rec = {'a': a, 'b': b, 'c': c, 'd': d, 'scale': scale, 'offset': offset}

                inside = 0
                for i in range(0, len(obj_map)):
                    inside = inside + self.rect_rect_intersection_test(obj_map[i], obj_rec)
                if inside == 0:
                    if d['x'] < img_w:
                        if d['y'] < img_h:
                            obj_map.append(obj_rec)
                            free_pos = True
                            ret_x = x
                            ret_y = y
                            x = img_w + 1
                            y = img_h + 1
                x = x + x_step
            y = y + y_step
        return free_pos, ret_x, ret_y

    def scale(self, img_detect, scale, rect, scale_mode: int = 0):
        h = 10
        w = 10
        d = rect['w'] / rect['h']

        if scale_mode == 0:
            w = self.scale_size * scale
        elif scale_mode == 1:
            c = rect['w'] / rect['face_w']
            d = rect['w'] / rect['h']
            w = c * self.scale_size * scale
        elif scale_mode == 2:
            c = rect['w'] / rect['eyes_d']
            d = rect['w'] / rect['h']
            w = c * self.scale_size * scale

        h = w / d

        w = int(w)
        h = int(h)

        img = img_detect.crop((rect['x'], rect['y'], rect['x'] + rect['w'], rect['y'] + rect['h']))
        img = img.resize((w, h))
        # print(scale)
        return [0, 0, w, h], img

    def chart_render_unit_timestamp_text(self, img, font, w, h, unit, timestamp, scale_mode):
        draw = PIL.ImageDraw.Draw(img)
        sequence = self.scale_mode_to_string(scale_mode) + ' 1 scale unit = ' + str(unit) + ' pixels  ' + timestamp
        sequence_width = font.getmask(sequence).getbbox()[2]
        sequence_height = font.getmask(sequence).getbbox()[3]
        draw.text((w - sequence_width, h - sequence_height), sequence, (0, 0, 0), font=font)

    def chart_render_text_from_obj_map(self, img, obj_map, font, w, h, unit, timestamp, scale_mode):
        draw = PIL.ImageDraw.Draw(img)
        # font = PIL.ImageFont.truetype("arial.ttf", 12)
        for i in range(0, len(obj_map)):
            sequence = 'S=' + str(obj_map[i]['scale'])
            # sequence_width = font.getmask(sequence).getbbox()[2]
            sequence_height = font.getmask(sequence).getbbox()[3]
            draw.text((obj_map[i]['a']['x'], obj_map[i]['c']['y'] - sequence_height), sequence, (0, 0, 0), font=font)
        self.chart_render_unit_timestamp_text(img=img, font=font, w=w, h=h, unit=unit, timestamp=timestamp,
                                              scale_mode=scale_mode)

    def all_scales_one_image(self,
                             img,
                             img_name,
                             detect_name,
                             detect_position,
                             rect,
                             dir_out: str = None,
                             scale_mode: int = 0) -> dict:
        img_chart = PIL.Image.new(mode='RGB', size=(self.frame['w'], self.frame['h']), color=self.color_background)
        results = dict()
        stats = []
        # Create empty map
        obj_map = []
        # allocate the font
        font = PIL.ImageFont.truetype("arial.ttf", 12)

        # cycle over scales
        for i in range(0, len(self.scales)):
            # scale string for print
            sequence = 'S=' + str(self.scales[i])
            sequence_width = font.getmask(sequence).getbbox()[2]
            sequence_height = font.getmask(sequence).getbbox()[3]
            # scale image
            rect_scaled, img_scaled = self.scale(img_detect=img, scale=self.scales[i], rect=rect, scale_mode=scale_mode)
            scale_c_h = {'w': rect_scaled[2] - rect_scaled[0], 'h': rect_scaled[3] - rect_scaled[1]}
            free_pos, x, y = self.search_free_position(obj_map, self.scales[i], scale_c_h, 0, self.frame['w'],
                                                       self.frame['h'], sequence_width, sequence_height)
            if free_pos is True:
                img_chart.paste(img_scaled, (x, y))
                stats.append({'x': x, 'y': y, 'w': rect_scaled[2], 'h': rect_scaled[3], 'scale': self.scales[i]})

        date_obj = datetime.now()
        timestamp = date_obj.strftime("%d-%b-%Y(%H-%M-%S-%f)")
        # print scales text
        self.chart_render_text_from_obj_map(img=img_chart, obj_map=obj_map, font=font, w=self.frame['w'],
                                            h=self.frame['h'], unit=self.scale_size, timestamp=timestamp,
                                            scale_mode=scale_mode)

        s_img_ne = os.path.splitext(os.path.basename(img_name))
        s_s_used = str(self.scales[0]) + '-' + str(self.scales[-1])
        s_d_pos = str(detect_position)
        name = dir_out + '/' + '{0}_scales-{1}_detect-{2}-{3}_{4}'.format(s_img_ne[0], s_s_used, detect_name, s_d_pos,
                                                                          timestamp)
        img_name = name + '.png'
        os.makedirs(os.path.dirname(img_name), exist_ok=True)
        img_save(img=img_chart, image_name=img_name)
        json_name = name + '.json'
        dt_json = {'exporter': 'Leesa Exporter v0.1.6', 'time': timestamp, 'type': 'object detection',
                   'scale_size': self.scale_size, 'detect_type': detect_name, 'scale_mode': scale_mode,
                   'objects': stats}
        with open(json_name, 'w') as outfile:
            json.dump(dt_json, outfile, indent=2)

        results = {'image': img_name, 'json': json_name}
        return results

    def object_to_one_image(self,
                            dir_img: str = None,
                            dir_json: str = None,
                            dir_out: str = None,
                            scales: list = None,
                            scale_size: int = 4,
                            scale_mode: int = 0,
                            ) -> list:
        """
        Create object detection chart and save image and JSON files.

        :param dir_img: the directory with images
        :param dir_json: the directory with JSON files
        :param dir_out: the directory to save result - image and JSON
        :param scales: list of the scales
        :param scale_size: size of the 1 scale unit in pixels
        :param scale_mode: 0 - scale by detect width, 1 - scale by face width, 2 = scale by distance between eyes
        :return: list of images and jsons
        """
        # an object dictionaries for comparison
        sm_0 = {"obj": "face", "x": 672, "y": 42, "w": 970, "h": 1134}
        sm_1 = {"obj": "face", "x": 672, "y": 42, "w": 970, "h": 1134, "face_w": 460}
        sm_2 = {"obj": "face", "x": 672, "y": 42, "w": 970, "h": 1134, "eyes_d": 236}

        if dir_img is None:
            raise ValueError("The image directory must be non-empty.")
        if dir_json is None:
            raise ValueError("The JSON directory must be non-empty.")
        if scale_size is None or scale_size < 1:
            raise ValueError("The scale_size be non-empty or > 0.")
        else:
            self.scale_size = scale_size
        # select the proper scales
        if scales is None or len(scales) == 0:
            self.scales = self.scales_fixed
        else:
            self.scales = scales
        # get the pairs of image and JSON
        result, pairs = get_image_json_pair_dir(directory_img=dir_img, pattern_img=['*.png', '*.jpg'],
                                                directory_json=dir_json, pattern_json=['*.json'])

        results = []

        if result is True:
            for e in pairs:
                img = PIL.Image.open(e[0])
                fp = open(e[1], 'r')
                img_json = json.load(fp)
                fp.close()

                i = 0
                for d in img_json:
                    if scale_mode == 0 and dictionary_compare_keys(etalon=sm_0, d=d) is False:
                        print("Some keys in object is absent. Please verify format. Must be a {0}".format(sm_0.keys()))
                    elif scale_mode == 1 and dictionary_compare_keys(etalon=sm_1, d=d) is False:
                        print("Some keys in object is absent. Please verify format. Must be a {0}".format(sm_1.keys()))
                    elif scale_mode == 2 and dictionary_compare_keys(etalon=sm_2, d=d) is False:
                        print("Some keys in object is absent. Please verify format. Must be a {0}".format(sm_2.keys()))
                    else:
                        r = self.all_scales_one_image(img=img,
                                                      img_name=e[0],
                                                      detect_name=d['obj'],
                                                      detect_position=i,
                                                      rect=d,
                                                      dir_out=dir_out,
                                                      scale_mode=scale_mode)
                        results.append(r)
                    i += 1
        print(results)
        return results
