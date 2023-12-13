from ctypes import *


class FastforwardingOverride(Structure):
    """retro_fastforwarding_override"""

    _fields_ = [
        ("ratio", c_float),
        ("fastforward", c_bool),
        ("notification", c_bool),
        ("inhibit_toggle", c_bool),
    ]

    ratio: float
    fastforward: bool
    notification: bool
    inhibit_toggle: bool
