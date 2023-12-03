from ctypes import *

from . import VALUES_MAX, OptionValue


class OptionCategory(Structure):
    """retro_core_option_v2_category"""

    _fields_ = [
        ("key", c_char_p),
        ("desc", c_char_p),
        ("info", c_char_p),
    ]

    key: bytes
    desc: bytes
    info: bytes


class OptionDefinition(Structure):
    """retro_core_option_v2_definition"""

    _fields_ = [
        ("key", c_char_p),
        ("desc", c_char_p),
        ("desc_categorized", c_char_p),
        ("info", c_char_p),
        ("info_categorized", c_char_p),
        ("category_key", c_char_p),
        ("values", OptionValue * VALUES_MAX),
        ("default_value", c_char_p),
    ]

    key: bytes
    desc: bytes
    desc_categorized: bytes
    info: bytes
    info_categorized: bytes
    category_key: bytes
    values: POINTER(OptionValue)
    default_value: bytes


class CoreOptions(Structure):
    """retro_core_options_v2"""

    _fields_ = [
        ("categories", POINTER(OptionCategory)),
        ("definitions", POINTER(OptionDefinition)),
    ]

    categories: POINTER(OptionCategory)
    definitions: POINTER(OptionDefinition)


class OptionIntl(Structure):
    """retro_core_options_v2_intl"""

    _fields_ = [
        ("us", POINTER(CoreOptions)),
        ("local", POINTER(CoreOptions)),
    ]

    us: POINTER(CoreOptions)
    local: POINTER(CoreOptions)
