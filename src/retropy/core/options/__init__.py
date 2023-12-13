from ctypes import *
from typing import Callable

VALUES_MAX = 128
"""RETRO_NUM_CORE_OPTION_VALUES_MAX"""

core_options_update_display_callback_t = CFUNCTYPE(c_bool)
"""retro_core_options_update_display_callback_t"""


class OptionValue(Structure):
    """retro_core_option_value"""

    _fields_ = [
        ("value", c_char_p),
        ("label", c_char_p),
    ]

    value: bytes
    label: bytes


class OptionsDisplay(Structure):
    """retro_core_option_display"""

    _fields_ = [
        ("key", c_char_p),
        ("visible", c_bool),
    ]

    key: bytes
    visible: c_bool


class UpdateOptionsDisplayCallback(Structure):
    """retro_core_options_update_display_callback"""

    _fields_ = [
        ("callback", core_options_update_display_callback_t),
    ]

    callback: Callable[[None], bool]
