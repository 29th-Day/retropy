from ctypes import *
from typing import Callable

midi_input_enabled_t = CFUNCTYPE(c_bool)
"""retro_midi_input_enabled_t"""

midi_output_enabled_t = CFUNCTYPE(c_bool)
"""retro_midi_output_enabled_t"""

midi_read_t = CFUNCTYPE(c_bool, POINTER(c_uint8))
"""retro_midi_read_t"""

midi_write_t = CFUNCTYPE(c_bool, c_uint8, c_uint32)
"""retro_midi_write_t"""

midi_flush_t = CFUNCTYPE(c_bool)
"""retro_midi_flush_t"""


class MidiInterface(Structure):
    """retro_midi_interface"""

    _fields_ = [
        ("input_enabled", midi_input_enabled_t),
        ("output_enabled", midi_output_enabled_t),
        ("read", midi_read_t),
        ("write", midi_write_t),
        ("flush", midi_flush_t),
    ]

    interface_type: Callable[[None], bool]
    output_enabled: Callable[[None], bool]
    read: Callable[[POINTER(c_uint8)], bool]
    write: Callable[[int, int], bool]
    flush: Callable[[None], bool]
