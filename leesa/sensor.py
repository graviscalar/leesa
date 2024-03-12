"""Contains the Sensor parameters.
"""
from leesa.image import *
import math


class SensorSony:
    _SENSORS = {
        'IMX482LQJ': {'resolution': 'FHD', 'diagonal': 0.0128, 'fps': 90,
                      'link': 'https://www.sony-semicon.com/files/62/flyer_security/IMX482LQJ_Flyer.pdf'},
        'IMX662-AAQR': {'resolution': 'FHD', 'diagonal': 0.00645, 'fps': 90,
                        'link': 'https://www.sony-semicon.com/files/62/flyer_security/IMX662-AAQR_AAQR1_Flyer.pdf'},
        'IMX462LQR': {'resolution': 'FHD', 'diagonal': 0.00646, 'fps': 120,
                      'link': 'https://www.sony-semicon.com/files/62/flyer_security/IMX462LQR_LQR1_Flyer.pdf'},
        'IMX327LQR': {'resolution': 'FHD', 'diagonal': 0.00646, 'fps': 60,
                      'link': 'https://www.sony-semicon.com/files/62/flyer_security/IMX327LQR_LQR1_Flyer.pdf'},
        'IMX307LQD': {'resolution': 'FHD', 'diagonal': 0.00646, 'fps': 60,
                      'link': 'https://www.sony-semicon.com/files/62/flyer_security/IMX307LQD_LQR_Flyer.pdf'},
        'IMX664-AAQR1': {'resolution': 'IMX664', 'diagonal': 0.00902, 'fps': 120,
                      'link': 'https://www.sony-semicon.com/files/62/flyer_security/IMX664-AAQR1_Flyer.pdf'},
        'IMX585-AAQJ1': {'resolution': '4K_UHD', 'diagonal': 0.01284, 'fps': 90,
                         'link': 'https://www.sony-semicon.com/files/62/flyer_security/IMX585-AAQJ1_Flyer.pdf'},
        'IMX294CJK': {'resolution': 'IMX294', 'diagonal': 0.02163, 'fps': 120,
                         'link': 'https://www.sony-semicon.com/files/62/flyer_security/IMX294CJK_Flyer.pdf'},
        'IMX571BQR-J': {'resolution': 'IMX571', 'diagonal': 0.0283, 'fps': 1125,
                      'link': 'https://www.sony-semicon.com/files/62/flyer_security/IMX571BQR-J_Flyer.pdf'},
        'IMX455AQK-K': {'resolution': 'IMX455', 'diagonal': 0.0433, 'fps': 558,
                        'link': 'https://www.sony-semicon.com/files/62/flyer_security/IMX455AQK-K_Flyer.pdf'},
        'IMX464LQR_LQR1': {'resolution': 'IMX664', 'diagonal': 0.00904, 'fps': 90,
                        'link': 'https://www.sony-semicon.com/files/62/flyer_security/IMX464LQR_LQR1_Flyer.pdf'},
        'IMX347LQR': {'resolution': 'IMX664', 'diagonal': 0.00904, 'fps': 90,
                           'link': 'https://www.sony-semicon.com/files/62/flyer_security/IMX347LQR_Flyer.pdf'},
        'IMX178LQJ': {'resolution': 'IMX178', 'diagonal': 0.00892, 'fps': 60,
                      'link': 'https://www.sony-semicon.com/files/62/flyer_security/IMX178LQJ_Flyer.pdf'},
        'IMX675-AAQR': {'resolution': 'IMX675', 'diagonal': 0.00653, 'fps': 80,
                      'link': 'https://www.sony-semicon.com/files/62/flyer_security/IMX675-AAQR_AAQR1_AATN_Flyer.pdf'},
        'IMX335LQN': {'resolution': 'IMX675', 'diagonal': 0.00652, 'fps': 60,
                        'link': 'https://www.sony-semicon.com/files/62/flyer_security/IMX335LQN_Flyer.pdf'},
        'IMX485LQJ_LQJ1': {'resolution': '4K_UHD', 'diagonal': 0.01286, 'fps': 90,
                      'link': 'https://www.sony-semicon.com/files/62/flyer_security/IMX485LQJ_LQJ1_Flyer.pdf'},
        'IMX678-AAQR1': {'resolution': '4K_UHD', 'diagonal': 0.00886, 'fps': 72,
                           'link': 'https://www.sony-semicon.com/files/62/flyer_security/IMX678-AAQR1_Flyer.pdf'},
        'IMX715-AAQR1': {'resolution': '4K_UHD', 'diagonal': 0.00643, 'fps': 90,
                         'link': 'https://www.sony-semicon.com/files/62/flyer_security/IMX715-AAQR1_Flyer.pdf'},
        'IMX515-AAQN': {'resolution': '4K_UHD', 'diagonal': 0.00643, 'fps': 61,
                         'link': 'https://www.sony-semicon.com/files/62/flyer_security/IMX515-AAQN_Flyer.pdf'},
        'IMX415-AAQR': {'resolution': '4K_UHD', 'diagonal': 0.00643, 'fps': 90,
                        'link': 'https://www.sony-semicon.com/files/62/flyer_security/IMX415-AAQR_Flyer.pdf'},
    }

    def get_dict(self):
        return self._SENSORS


class Sensor:
    """The Sensor parameters.

    :param frame_type: current active resolution, not a real sensor size
    """

    def __init__(self, sensor_name: str = 'IMX307LQD', frame_type: str = 'FHD', sensor_diagonal: float = 6.45e-03):
        self.sr_ne = sensor_name
        ss = SensorSony()
        _SENSORS = ss.get_dict()
        fr = FrameResolution()
        _FRAME_SIZE = fr.get_dict()

        if sensor_name is not None:
            sr = _SENSORS[sensor_name]
            frame = _FRAME_SIZE[sr['resolution']]
            self.frame_width = frame['w']
            self.frame_height = frame['h']
            r = frame['w'] / frame['h']
            self.s_h = sr['diagonal'] / math.sqrt(r * r + 1)
            self.pixel_size = self.s_h / frame['h']
        else:
            if frame_type is None:
                raise ValueError("The frame size must be non-empty.")
            if sensor_diagonal is None or sensor_diagonal <= 0:
                raise ValueError("The sensor diagonal ize be non-empty or > 0.")

            frame = _FRAME_SIZE[frame_type]
            r = frame['w'] / frame['h']
            self.s_h =sensor_diagonal / math.sqrt(r * r + 1)
            self.frame_width = frame['w']
            self.frame_height = frame['h']
            self.pixel_size = self.s_h / frame['h']
