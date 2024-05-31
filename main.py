from leesa.chart import Chart
from leesa.odchart import ODChart
from leesa.bayer import *
from leesa.camera import *
from leesa.human import *
import time
from leesa.color import *
from leesa.geometry import *
from leesa.objwf import *
from leesa.edge import *

if __name__ == '__main__':
    time_start = time.time()  # Log the time

    # An example of usage for chart with ramp colors
    ct = Chart(frame_type='nHD', color_background=(127, 127, 127))
    ct.ramps(image_name='img/out/ramps.png',
             json_name='img/out/ramps.json')

    # An example of usage for converting RGB to Bayer images
    # for RGGB Bayer type
    rgb_to_bayer(image_name='img/out/ramps.png', dir_name='img/out', bayer_type='RGGB')
    # for BGGR Bayer type
    rgb_to_bayer(image_name='img/out/ramps.png', dir_name='img/out', bayer_type='BGGR')
    # for X-TRANS Bayer type
    rgb_to_bayer(image_name='img/out/ramps.png', dir_name='img/out', bayer_type='X-TRANS')

    # An example of usage for chart with color combinations
    ct = Chart(frame_type='nHD', color_background=(127, 127, 127))
    ct.combinations(image_name='img/out/combinations.png',
                    json_name='img/out/combinations.json')

    # An example of usage for chart for edge detection test
    ct = Chart(frame_type='FHD', color_background=(127, 127, 127))
    ct.edge_test(image_name='img/out/edge_test.png',
                 json_name='img/out/edge_test.json')

    # An example of usage for chart with single color and without border
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

    # An example of usage for chart with gradient color and no border
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

    # An example of usage for object detection chart
    ct = ODChart(frame_type='HD', color_background=(255, 255, 255))
    ct.object_to_one_image(dir_img='tests/data_sample/sample_2/',
                           dir_json='tests/data_sample/sample_2/',
                           dir_out='img/out',
                           # scales=[30, 25, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5],
                           scale_size=3,
                           scale_mode=0,
                           )

    # An example of usage for object detection chart with multiple images
    ct = ODChart(frame_type='HD', color_background=(255, 255, 255))
    ct.object_to_images(dir_img='tests/data_sample/sample_2/',
                        dir_json='tests/data_sample/sample_2/',
                        dir_out='img/out',
                        scales=[17, 18, 19, 20],
                        scale_size=3,
                        gap_x=8,
                        gap_y=8
                        )

    # An example of usage for distance estimation
    sr = Sensor(sensor_name='IMX482LQJ')
    os = Optics(focal_length=4e-03)
    c = Camera(sensor=sr, optics=os)
    h = Human()
    r = h.camera_to_distance(eyes_d=146, cam=c, mode=0)
    print(r)
    r = h.camera_to_distance(face_w=342, cam=c, mode=1)
    print(r)
    r = h.camera_to_distance(human_h=4672, cam=c, mode=2)
    print(r)
    # An example of usage for focal length estimation
    r = h.distance_to_focal(eyes_d=146, cam=c, distance=0.3, mode=0)
    print(r)
    r = h.distance_to_focal(face_w=342, cam=c, distance=0.3, mode=1)
    print(r)
    r = h.distance_to_focal(human_h=4672, cam=c, distance=0.3, mode=2)
    print(r)
    # An example of usage for pixel size estimation
    r = h.distance_to_pixels(distance=0.3, cam=c, mode=0)
    print('distance between eyes in pixels = ', r)
    r = h.distance_to_pixels(distance=0.3, cam=c, mode=1)
    print('face width in pixels = ', r)
    r = h.distance_to_pixels(distance=0.3, cam=c, mode=2)
    print('human height in pixels = ', r)

    time_end = time.time()  # Log the time
    print("It took %f seconds for all processing." % (time_end - time_start))
