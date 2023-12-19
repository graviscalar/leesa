from leesa.chart import Chart
from leesa.bayer import *
import time

if __name__ == '__main__':
    time_start = time.time()  # Log the time

    ct = Chart(frame_type='nHD', color_background=(127, 127, 127))
    ct.ramps(image_name='img/out/ramps.png',
             json_name='img/out/ramps.json')

    rgb_to_bayer(image_name='img/out/ramps.png', dir_name='img/out', bayer_type='RGGB')

    ct = Chart(frame_type='nHD', color_background=(127, 127, 127))
    ct.combinations(image_name='img/out/combinations.png',
                    json_name='img/out/combinations.json')

    ct = Chart(frame_type='nHD', color_background=(255, 255, 255))
    ct.rectangles(color_mode='single_color',
                  rectangle_width=50,
                  rectangle_height=50,
                  gap_x=14,
                  gap_y=10,
                  rectangle_color=[[0, 255, 0]],
                  border=False,
                  image_name='img/out/single_color.png',
                  json_name='img/out/single_color.json')

    ct = Chart(frame_type='nHD', color_background=(255, 255, 255))
    ct.rectangles(color_mode='gradient_color',
                  rectangle_width=50,
                  rectangle_height=50,
                  gap_x=14,
                  gap_y=10,
                  rectangle_color=[[255, 255, 0], [0, 0, 255]],
                  border=False,
                  image_name='img/out/gradient_color.png',
                  json_name='img/out/gradient_color.json')

    time_end = time.time()  # Log the time
    print("It took %f seconds for all processing." % (time_end - time_start))
