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
        'OS02C10': {'resolution': 'FHD', 'diagonal': 0.0, 'fps': 40, 'pixel_size': 2.9e-06,
                    'link': 'https://www.ovt.com/wp-content/uploads/2023/06/OS02C10-PB-v1.4-WEB.pdf'},
        'OS02G10': {'resolution': 'FHD', 'diagonal': 0.0, 'fps': 30, 'pixel_size': 2.8e-06,
                    'link': 'https://www.ovt.com/wp-content/uploads/2023/06/OS02G10-PB-v1.3-WEB.pdf'},
        'OS02H10': {'resolution': 'FHD', 'diagonal': 0.0, 'fps': 60, 'pixel_size': 2.9e-06,
                    'link': 'https://www.ovt.com/wp-content/uploads/2023/06/OS02H10-PB-v1.1-WEB.pdf'},
        'OS02N10': {'resolution': 'FHD', 'diagonal': 0.0, 'fps': 30, 'pixel_size': 2.5e-06,
                    'link': 'https://www.ovt.com/wp-content/uploads/2023/09/OS02N10-PB-v1.0-WEB.pdf'},
        'OS03B10': {'resolution': 'OS03B10', 'diagonal': 0.0, 'fps': 30, 'pixel_size': 2.5e-06,
                    'link': 'https://www.ovt.com/wp-content/uploads/2022/03/OS03B10-PB-v1.0-WEB.pdf'},
        'OS04A10': {'resolution': 'IMX664', 'diagonal': 0.0, 'fps': 30, 'pixel_size': 2.9e-06,
                    'link': 'https://www.ovt.com/wp-content/uploads/2023/06/OS04A10-PB-v1.2-WEB.pdf'},
        'OS04C10': {'resolution': 'IMX664', 'diagonal': 0.0, 'fps': 240, 'pixel_size': 1.998e-06,
                    'link': 'https://www.ovt.com/wp-content/uploads/2022/10/OS04C10-PB-v1.1-WEB.pdf'},
        'OS04D10': {'resolution': 'QHD', 'diagonal': 0.0, 'fps': 30, 'pixel_size': 1.998e-06,
                    'link': 'https://www.ovt.com/wp-content/uploads/2023/03/OS04D10-PB-v1.0-WEB.pdf'},
        'OS04E10': {'resolution': 'OS04E10', 'diagonal': 0.0, 'fps': 240, 'pixel_size': 1.998e-06,
                    'link': 'https://www.ovt.com/wp-content/uploads/2022/10/OS04E10-PB-v1.0-WEB.pdf'},
        'OS04L': {'resolution': 'QHD', 'diagonal': 0.0, 'fps': 30, 'pixel_size': 2e-06,
                    'link': 'https://www.ovt.com/wp-content/uploads/2022/10/OS04L-PB-v1.0-WEB.pdf'},
        'OS05A10': {'resolution': 'OS05A10', 'diagonal': 0.0, 'fps': 60, 'pixel_size': 2e-06,
                  'link': 'https://www.ovt.com/wp-content/uploads/2023/06/OS05A10-PB-v1.4-WEB.pdf'},
        'OS05A20': {'resolution': 'OS05A10', 'diagonal': 0.0, 'fps': 60, 'pixel_size': 2e-06,
                    'link': 'https://www.ovt.com/wp-content/uploads/2023/07/OS05A20-PB-v1.4-WEB.pdf'},
        'OS05B': {'resolution': 'IMX675', 'diagonal': 0.0, 'fps': 360, 'pixel_size': 1.998e-06,
                    'link': 'https://www.ovt.com/wp-content/uploads/2022/10/OS05B-PB-v1.0-WEB.pdf'},
        'OS08A10': {'resolution': '4K_UHD', 'diagonal': 0.0, 'fps': 120, 'pixel_size': 2e-06,
                  'link': 'https://www.ovt.com/wp-content/uploads/2023/06/OS08A10-PB-v1.6-WEB.pdf'},
        'OS08A20': {'resolution': '4K_UHD', 'diagonal': 0.0, 'fps': 120, 'pixel_size': 2e-06,
                    'link': 'https://www.ovt.com/wp-content/uploads/2023/07/OS08A20-PB-v1.3-WEB.pdf'},
        'OS08C10': {'resolution': 'OS08C10', 'diagonal': 0.0, 'fps': 60, 'pixel_size': 1.449e-06,
                    'link': 'https://www.ovt.com/wp-content/uploads/2023/10/OS08C10-PB-v1.0-WEB-1.pdf'},
        'OS12D40': {'resolution': 'OS12D40', 'diagonal': 0.0, 'fps': 60, 'pixel_size': 1.404e-06,
                    'link': 'https://www.ovt.com/wp-content/uploads/2023/07/OS12D40-PB-v1.2-WEB.pdf'},
        'OV2718': {'resolution': 'FHD', 'diagonal': 0.0, 'fps': 30, 'pixel_size': 2.8e-06,
                    'link': 'https://www.ovt.com/wp-content/uploads/2023/07/OV2718-PB-v1.4-WEB.pdf'},
        'OV2732': {'resolution': 'FHD', 'diagonal': 0.0, 'fps': 240, 'pixel_size': 2e-06,
                   'link': 'https://www.ovt.com/wp-content/uploads/2023/07/OV2732-PB-v1.2-WEB.pdf'},
        'OV2735': {'resolution': 'FHD', 'diagonal': 0.0, 'fps': 60, 'pixel_size': 3e-06,
                   'link': 'https://www.ovt.com/wp-content/uploads/2023/07/OV2735-PB-v1.4-WEB.pdf'},
        'OV4689': {'resolution': 'IMX664', 'diagonal': 0.0, 'fps': 60, 'pixel_size': 3e-06,
                   'link': 'https://www.ovt.com/wp-content/uploads/2023/08/OV4689-PB-v1.8-WEB.pdf'},
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
            if 'pixel_size' not in sr:
                r = frame['w'] / frame['h']
                self.s_h = sr['diagonal'] / math.sqrt(r * r + 1)
                self.pixel_size = self.s_h / frame['h']
            else:
                self.s_h = sr['pixel_size'] * frame['h']
                self.pixel_size = sr['pixel_size']
        else:
            if frame_type is None:
                raise ValueError("The frame size must be non-empty.")
            if sensor_diagonal is None or sensor_diagonal <= 0:
                raise ValueError("The sensor diagonal ize be non-empty or > 0.")

            frame = _FRAME_SIZE[frame_type]
            r = frame['w'] / frame['h']
            self.s_h = sensor_diagonal / math.sqrt(r * r + 1)
            self.frame_width = frame['w']
            self.frame_height = frame['h']
            self.pixel_size = self.s_h / frame['h']
