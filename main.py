from leesa.chart import Chart
import time

if __name__ == '__main__':
    time_start = time.time()  # Log the time

    ct = Chart(frame_size='HD', width=50, height=50, offset=25, offset_at_start=True, border=True, color_background=(255, 255, 255))
    ct.chart_rectangles(color_mode='single_color', color=[[0, 255, 0]], image_name='img/out/single_color.png', json_name='img/out/single_color.json')

    ct = Chart(frame_size='HD', width=50, height=50, offset=25, offset_at_start=True, border=True, color_background=(255, 255, 255))
    ct.chart_rectangles(color_mode='gradient_color', color=[[255, 255, 0], [0, 0, 255]], image_name='img/out/gradient_color.png', json_name='img/out/gradient_color.json')

    time_end = time.time()  # Log the time
    print("It took %f seconds for all processing." % (time_end - time_start))

    print()
