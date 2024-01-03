import PIL.Image
from leesa.image import *


def rgb_to_xtrans(c, channel):
    # filter red
    fr = [[0, 0, 1, 0, 1, 0],
          [1, 0, 0, 0, 0, 0],
          [0, 0, 0, 1, 0, 0],
          [0, 1, 0, 0, 0, 1],
          [0, 0, 0, 1, 0, 0],
          [1, 0, 0, 0, 0, 0]]
    # filter green
    fg = [[1, 0, 0, 1, 0, 0],
          [0, 1, 1, 0, 1, 1],
          [0, 1, 1, 0, 1, 1],
          [1, 0, 0, 1, 0, 0],
          [0, 1, 1, 0, 1, 1],
          [0, 1, 1, 0, 1, 1]]
    # filter blue
    fb = [[0, 1, 0, 0, 0, 1],
          [0, 0, 0, 1, 0, 0],
          [1, 0, 0, 0, 0, 0],
          [0, 0, 1, 0, 1, 0],
          [1, 0, 0, 0, 0, 0],
          [0, 0, 0, 1, 0, 0]]

    f = fr
    if channel == 1:
        f = fg
    elif channel == 2:
        f = fb
    # # limit height by multiplier of 6
    # h = len(c) // 6 * 6
    # # limit width by multiplier of 6
    # w = len(c[0]) // 6 * 6
    #
    # for y in range(0, h, 6):
    #     for x in range(0, w, 6):
    #         c[y:y + 6, x:x + 6] = c[y:y + 6, x:x + 6] * f

    ht = len(c) // 6 + 1
    wt = len(c[0]) // 6 + 1
    f = np.tile(f, (ht, wt))
    f = f[0:len(c), 0:len(c[0])]
    c = c * f
    return c


def rgb_to_rggb(c, channel):
    # filter red
    fr = [[1, 0],
          [0, 0]]
    # filter green
    fg = [[0, 1],
          [1, 0]]
    # filter blue
    fb = [[0, 0],
          [0, 1]]

    f = fr
    if channel == 1:
        f = fg
    elif channel == 2:
        f = fb

    ht = len(c) // 2 + 1
    wt = len(c[0]) // 2 + 1
    f = np.tile(f, (ht, wt))
    f = f[0:len(c), 0:len(c[0])]
    c = c * f
    return c

def rgb_to_bggr(c, channel):
    # filter red
    fr = [[0, 0],
          [0, 1]]
    # filter green
    fg = [[0, 1],
          [1, 0]]
    # filter blue
    fb = [[1, 0],
          [0, 0]]

    f = fr
    if channel == 1:
        f = fg
    elif channel == 2:
        f = fb

    ht = len(c) // 2 + 1
    wt = len(c[0]) // 2 + 1
    f = np.tile(f, (ht, wt))
    f = f[0:len(c), 0:len(c[0])]
    c = c * f
    return c


def rgb_to_bayer(image_name: str = None, dir_name: str = None, bayer_type: str = 'RGGB') -> list:
    """
    Convert RGB image to the Bayer images.

    :param image_name: input RGB image name
    :param dir_name: output directory for Bayer images
    :param bayer_type: Bayer type:
    :return: list of the Bayer images names
    """
    bt = {'RGGB', 'BGGR', 'X-TRANS'}
    r = []

    if bayer_type not in bt:
        print('This Bayer type is not supported yet')
        return r

    img = PIL.Image.open(image_name)
    dt = np.array(img).astype(int)

    # R channel
    c = dt[:, :, 0]
    if bayer_type == 'X-TRANS':
        c = rgb_to_xtrans(c=c, channel=0)
    elif bayer_type == 'RGGB':
        c = rgb_to_rggb(c=c, channel=0)
    elif bayer_type == 'BGGR':
        c = rgb_to_bggr(c=c, channel=0)
    filepath = os.path.join(dir_name, 'r.png')
    img = PIL.Image.fromarray(c).convert('L')
    img_save(img=img, image_name=filepath)
    r.append(filepath)
    # G channel
    c = dt[:, :, 1]
    if bayer_type == 'X-TRANS':
        c = rgb_to_xtrans(c=c, channel=1)
    elif bayer_type == 'RGGB':
        c = rgb_to_rggb(c=c, channel=1)
    elif bayer_type == 'BGGR':
        c = rgb_to_bggr(c=c, channel=1)
    filepath = os.path.join(dir_name, 'g.png')
    img = PIL.Image.fromarray(c).convert('L')
    img_save(img=img, image_name=filepath)
    r.append(filepath)
    # B channel
    c = dt[:, :, 2]
    if bayer_type == 'X-TRANS':
        c = rgb_to_xtrans(c=c, channel=2)
    elif bayer_type == 'RGGB':
        c = rgb_to_rggb(c=c, channel=2)
    elif bayer_type == 'BGGR':
        c = rgb_to_bggr(c=c, channel=2)
    filepath = os.path.join(dir_name, 'b.png')
    img = PIL.Image.fromarray(c).convert('L')
    img_save(img=img, image_name=filepath)
    r.append(filepath)
