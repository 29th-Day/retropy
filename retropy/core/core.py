# libretro.h

from ctypes import *
from enum import IntEnum, Enum
from typing import Callable, List

from .game import retro_game_info
from .system import retro_system_av_info, retro_system_info

# region 258 - 259

class RETRO_REGION(Enum):
    NTSC = 0
    PAL = 1

# endregion

# region 3656 - 3865


class retro_core_option_display(Structure):
    _fields_ = [
        ('key', c_char_p),
        ('visible', c_bool),
    ]

    key: bytes
    visible: c_bool

CORE_OPTION_VALUES_MAX = 128


class retro_core_option_value(Structure):
    _fields_ = [
        ('value', c_char_p),
        ('label', c_char_p),
    ]

    value: bytes
    label: bytes


class retro_core_option_definition(Structure):
    _fields_ = [
        ('key', c_char_p),
        ('desc', c_char_p),
        ('info', c_char_p),
        ('values', retro_core_option_value * CORE_OPTION_VALUES_MAX),
        ('default_value', c_char_p),
    ]

    key: bytes
    desc: bytes
    info: bytes
    values: POINTER(retro_core_option_value)
    default_value: bytes

class retro_core_options_intl(Structure):
    _fields_ = [
        ('us', POINTER(retro_core_option_definition)),
        ('local', POINTER(retro_core_option_definition)),
    ]

    us: POINTER(retro_core_option_definition)
    local: POINTER(retro_core_option_definition)


class retro_core_option_v2_category(Structure):
    _fields_ = [
        ('key', c_char_p),
        ('desc', c_char_p),
        ('info', c_char_p),
    ]

    key: bytes
    desc: bytes
    info: bytes


class retro_core_option_v2_definition(Structure):
    _fields_ = [
        ('key', c_char_p),
        ('desc', c_char_p),
        ('desc_categorized', c_char_p),
        ('info', c_char_p),
        ('info_categorized', c_char_p),
        ('category_key', c_char_p),
        ('values', retro_core_option_value * CORE_OPTION_VALUES_MAX),
        ('default_value', c_char_p),
    ]

    key: bytes
    desc: bytes
    desc_categorized: bytes
    info: bytes
    info_categorized: bytes
    category_key: bytes
    values: POINTER(retro_core_option_value)
    default_value: bytes


class retro_core_options_v2(Structure):
    _fields_ = [
        ('categories', POINTER(retro_core_option_v2_category)),
        ('definitions', POINTER(retro_core_option_v2_definition)),
    ]

    categories: POINTER(retro_core_option_v2_category)
    definitions: POINTER(retro_core_option_v2_definition)


class retro_core_options_v2_intl(Structure):
    _fields_ = [
        ('us', POINTER(retro_core_options_v2)),
        ('local', POINTER(retro_core_options_v2)),
    ]

    us: POINTER(retro_core_options_v2)
    local: POINTER(retro_core_options_v2)


retro_core_options_update_display_callback_t = CFUNCTYPE(c_bool)


class retro_core_options_update_display_callback(Structure):
    _fields_ = [
        ('callback', retro_core_options_update_display_callback_t),
    ]

    callback: Callable[[None], c_bool]


# endregion

# region 3913 - 3989


class retro_fastforwarding_override(Structure):
    _fields_ = [
        ('ratio', c_float),
        ('fastforward', c_bool),
        ('notification', c_bool),
        ('inhibit_toggle', c_bool),
    ]

    ratio: c_float
    fastforward: c_bool
    notification: c_bool
    inhibit_toggle: c_bool


class THROTTLE_MODE(IntEnum):
    NONE = 0
    FRAME_STEPPING = 1
    FAST_FORWARD = 2
    SLOW_MOTION = 3
    REWINDING = 4
    VSYNC = 5
    UNBLOCKED = 6


class retro_throttle_state(Structure):
    _fields_ = [
        ('mode', c_uint),
        ('rate', c_float),
    ]

    mode: c_uint
    rate: c_float


# endregion

# region 4322 - 4420


class CoreDLL:
    # Callbacks
    def retro_set_environment(
        self, callback: Callable[[c_uint, c_void_p], c_bool]
    ) -> None:
        ...

    def retro_set_video_refresh(
        self, callback: Callable[[c_void_p, c_uint, c_uint, c_size_t], None]
    ) -> None:
        ...

    def retro_set_audio_sample(
        self, callback: Callable[[c_int16, c_int16], None]
    ) -> None:
        ...

    def retro_set_audio_sample_batch(
        self, callback: Callable[[POINTER(c_int16), c_size_t], c_size_t]
    ) -> None:
        ...

    def retro_set_input_poll(self, callback: Callable[[None], None]) -> None:
        ...

    def retro_set_input_state(
        self, callback: Callable[[c_uint, c_uint, c_uint, c_uint], c_int16]
    ) -> None:
        ...

    def retro_init(self) -> None:
        ...

    def retro_deinit(self) -> None:
        ...

    def retro_api_version(self) -> c_uint:
        ...

    def retro_get_system_info(self, info: POINTER(retro_system_info)) -> None:
        ...

    def retro_get_system_av_info(self, info: POINTER(retro_system_av_info)) -> None:
        ...

    def retro_set_controller_port_device(self, port: c_uint, device: c_uint) -> None:
        ...

    def retro_reset(self) -> None:
        ...

    def retro_run(self) -> None:
        ...

    def retro_serialize_size(self) -> c_size_t:
        ...

    def retro_serialize(self, data: c_void_p, size: c_size_t) -> c_bool:
        ...

    def retro_unserialize(self, data: c_void_p, size: c_size_t) -> c_bool:
        ...

    def retro_cheat_reset(self) -> None:
        ...

    def retro_cheat_set(self, index: c_uint, enabled: c_bool, code: c_char_p):
        ...

    def retro_load_game(self, game: POINTER(retro_game_info)) -> c_bool:
        ...

    def retro_load_game_special(
        self, game_type: c_uint, info: POINTER(retro_game_info), num_info: c_size_t
    ) -> c_bool:
        ...

    def retro_unload_game(self) -> None:
        ...

    def retro_get_region(self) -> c_uint:
        ...

    def retro_get_memory_data(self, id: c_uint) -> c_void_p:
        ...

    def retro_get_memory_size(self, id: c_uint) -> c_size_t:
        ...


# endregion
