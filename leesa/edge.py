from leesa.image import *
import math


def gradient_extract(img) -> tuple:
    """
    Gradients extraction from an image
    :param img: image object
    :return: tuple with X gradient and Y gradient
    """

    if img is None:
        raise ValueError("Image object must be non-empty.")
    n_height = len(img)
    n_width = len(img[0])
    r_grad_x = [[0.0 for _ in range(n_width)] for _ in range(n_height)]
    r_grad_y = [[0.0 for _ in range(n_width)] for _ in range(n_height)]

    for _n_y in range(n_height - 1):
        for _n_x in range(n_width - 1):
            _r_a = img[_n_y][_n_x]
            _r_b = img[_n_y][_n_x + 1]
            _r_c = img[_n_y + 1][_n_x]
            _r_d = img[_n_y + 1][_n_x + 1]
            r_grad_x[_n_y][_n_x] = (_r_b + _r_d - _r_a - _r_c) / 2
            r_grad_y[_n_y][_n_x] = (_r_c + _r_d - _r_a - _r_b) / 2

    return r_grad_x, r_grad_y


def gradient_amplitude_calc(r_grad_x: list = None, r_grad_y: list = None) -> list:
    """
    Calculate gradient amplitude by using X gradient and Y gradient
    :param r_grad_x: X gradient
    :param r_grad_y: Y gradient
    :return: gradient amplitude
    """
    if r_grad_x is None:
        raise ValueError("X gradient must be non-empty.")
    if r_grad_y is None:
        raise ValueError("Y gradient must be non-empty.")

    n_height = len(r_grad_x)
    n_width = len(r_grad_x[0])
    amp = [[0 for _ in range(n_width)] for _ in range(n_height)]

    for n_y in range(n_height):
        for n_x in range(n_width):
            r_gx = r_grad_x[n_y][n_x]
            r_gy = r_grad_y[n_y][n_x]
            amp[n_y][n_x] = (math.sqrt((r_gx * r_gx) + (r_gy * r_gy)))

    return amp


def gradient_angle_calc(r_grad_x: list = None, r_grad_y: list = None) -> list:
    """
    Calculate gradient angle by using X gradient and Y gradient
    :param r_grad_x: X gradient
    :param r_grad_y: Y gradient
    :return: gradient amplitude
    """
    if r_grad_x is None:
        raise ValueError("X gradient must be non-empty.")
    if r_grad_y is None:
        raise ValueError("Y gradient must be non-empty.")

    n_height = len(r_grad_x)
    n_width = len(r_grad_x[0])
    n_ang = [[0.0 for _ in range(n_width)] for _ in range(n_height)]

    for n_y in range(n_height):
        for n_x in range(n_width):
            r_gx = r_grad_x[n_y][n_x]
            r_gy = r_grad_y[n_y][n_x]

            r_angle = 0
            if r_gx != 0 and r_gy != 0:
                r_dab = r_gx / math.sqrt(r_gx * r_gx + r_gy * r_gy)
                r_angle = math.degrees(math.acos(r_dab))
                if r_gy < 0:
                    r_angle = 360 - r_angle
            n_ang[n_y][n_x] = r_angle

    return n_ang


def gradient_angle_quantization8(r_angle: float) -> int:
    n_angle_q = 1
    if (r_angle <= 23) or (r_angle > 338):
        n_angle_q = 1
    elif (r_angle > 23) and (r_angle < 68):
        n_angle_q = 2
    elif (r_angle >= 68) and (r_angle < 113):
        n_angle_q = 3
    elif (r_angle >= 113) and (r_angle < 158):
        n_angle_q = 4
    elif (r_angle >= 158) and (r_angle < 203):
        n_angle_q = 5
    elif (r_angle >= 203) and (r_angle < 248):
        n_angle_q = 6
    elif (r_angle >= 248) and (r_angle < 293):
        n_angle_q = 7
    elif (r_angle >= 293) and (r_angle <= 338):
        n_angle_q = 8
    return n_angle_q


def gradient_angle_quantization(r_angle: list = None, amp: list = None) -> np.ndarray:
    if r_angle is None:
        raise ValueError("Angle must be non-empty.")

    n_height = len(r_angle)
    n_width = len(r_angle[0])
    n_aq = np.zeros((n_height, n_width, 1), dtype=np.uint8)
    for n_y in range(n_height):
        for n_x in range(n_width):
            if amp[n_y][n_x] > 0:
                n_angle_q = gradient_angle_quantization8(r_angle[n_y][n_x])
                n_aq[n_y][n_x] = n_angle_q

    return n_aq


def image_paint_by_angle(n_aq: np.ndarray) -> np.ndarray:
    n_height, n_width, _ = n_aq.shape
    n_img = np.zeros((n_height, n_width, 3), dtype=np.uint8)
    for n_y in range(n_height):
        for n_x in range(n_width):
            n_angle = n_aq[n_y][n_x]
            if n_angle == 0:
                n_img[n_y][n_x] = [0, 0, 0]
            elif n_angle == 1:
                n_img[n_y][n_x] = [255, 0, 0]
            elif n_angle == 2:
                n_img[n_y][n_x] = [254, 179, 0]
            elif n_angle == 3:
                n_img[n_y][n_x] = [50, 255, 0]
            elif n_angle == 4:
                n_img[n_y][n_x] = [0, 254, 58]
            elif n_angle == 5:
                n_img[n_y][n_x] = [0, 255, 251]
            elif n_angle == 6:
                n_img[n_y][n_x] = [0, 22, 255]
            elif n_angle == 7:
                n_img[n_y][n_x] = [0, 180, 255]
            elif n_angle == 8:
                n_img[n_y][n_x] = [255, 0, 117]
    return n_img
