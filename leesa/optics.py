"""Contains the Optical parameters.
"""


class Optics:
    """The Optics parameters.

    Arguments:
      focal_length: the focal length for pin hole model
    """

    def __init__(self, focal_length: float = 2.8e-03):
        self.focal_length = focal_length
