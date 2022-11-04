from leesa.chart import Chart
import time

if __name__ == '__main__':
    time_start = time.time()  # Log the time

    ct = Chart(frame_type='HD', color_background=(255, 255, 255))
    ct.rectangles(color_mode='single_color',
                  rectangle_color=[[0, 255, 0]],
                  border=True,
                  image_name='img/out/single_color.png',
                  json_name='img/out/single_color.json')

    ct = Chart(frame_type='HD', color_background=(255, 255, 255))
    ct.rectangles(color_mode='gradient_color',
                  rectangle_color=[[255, 255, 0], [0, 0, 255]],
                  border=True,
                  image_name='img/out/gradient_color.png',
                  json_name='img/out/gradient_color.json')

    time_end = time.time()  # Log the time
    print("It took %f seconds for all processing." % (time_end - time_start))
