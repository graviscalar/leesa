import PIL.Image
from leesa.image import *


def rgb_to_bayer(image_name: str = None, dir_name: str = None, bayer_type: str = 'RGGB') -> list:
    """
    Convert RGB image to the Bayer images.

    :param image_name: input RGB image name
    :param dir_name: output directory for Bayer images
    :param bayer_type: Bayer type:
    :return: list of the Bayer images names
    """
    bt = {'RGGB', 'BGGR'}
    r = []

    if bayer_type not in bt:
        print('This Bayer type is not supported yet')
        return r

    img = PIL.Image.open(image_name)
    dt = np.array(img).astype(int)

    # R channel
    c = dt[:, :, 0]
    for y in range(len(c)):
        for x in range(len(c[0])):
            if y % 2 != 1:
                if x % 2 != 0:
                    c[y, x] = 0
            else:
                c[y, x] = 0
    filepath = os.path.join(dir_name, 'r.png')
    if bayer_type == 'BGGR':
        filepath = os.path.join(dir_name, 'b.png')
    img = PIL.Image.fromarray(c).convert('L')
    img_save(img=img, image_name=filepath)
    r.append(filepath)
    # G channel
    c = dt[:, :, 1]
    for y in range(len(c)):
        for x in range(len(c[0])):
            if y % 2 == 0:
                if x % 2 == 0:
                    c[y, x] = 0
            else:
                if x % 2 != 0:
                    c[y, x] = 0
    filepath = os.path.join(dir_name, 'g.png')
    img = PIL.Image.fromarray(c).convert('L')
    img_save(img=img, image_name=filepath)
    r.append(filepath)
    # B channel
    c = dt[:, :, 2]
    for y in range(len(c)):
        for x in range(len(c[0])):
            if y % 2 == 1:
                if x % 2 == 0:
                    c[y, x] = 0
            else:
                c[y, x] = 0
    filepath = os.path.join(dir_name, 'b.png')
    if bayer_type == 'BGGR':
        filepath = os.path.join(dir_name, 'r.png')
    img = PIL.Image.fromarray(c).convert('L')
    img_save(img=img, image_name=filepath)
    r.append(filepath)