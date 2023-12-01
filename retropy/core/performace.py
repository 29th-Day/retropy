# libretro.h: 2409 - 2523

from ctypes import *
from typing import Callable
from enum import IntFlag

class SIMD(IntFlag):
    SSE     = (1 << 0)
    SSE2    = (1 << 1)
    VMX     = (1 << 2)
    VMX128  = (1 << 3)
    AVX     = (1 << 4)
    NEON    = (1 << 5)
    SSE3    = (1 << 6)
    SSSE3   = (1 << 7)
    MMX     = (1 << 8)
    MMXEXT  = (1 << 9)
    SSE4    = (1 << 10)
    SSE42   = (1 << 11)
    AVX2    = (1 << 12)
    VFPU    = (1 << 13)
    PS      = (1 << 14)
    AES     = (1 << 15)
    VFPV3   = (1 << 16)
    VFPV4   = (1 << 17)
    POPCNT  = (1 << 18)
    MOVBE   = (1 << 19)
    CMOV    = (1 << 20)
    ASIMD   = (1 << 21)

class retro_perf_counter(Structure):
    _fields_ = [
        ('indent', c_char_p),
        ('start', c_uint64),
        ('total', c_uint64),
        ('call_cnt', c_uint64),
        ('registered', c_bool)
    ]

    indent: c_char_p
    start: c_uint64
    total: c_uint64
    call_cnt: c_uint64
    registered: c_bool

retro_perf_get_time_usec_t = CFUNCTYPE(c_int64)
retro_perf_get_counter_t = CFUNCTYPE(c_uint64)
retro_get_cpu_features_t = CFUNCTYPE(c_uint64)
retro_perf_log_t = CFUNCTYPE(None)
retro_perf_register_t = CFUNCTYPE(None, POINTER(retro_perf_counter))
retro_perf_start_t = CFUNCTYPE(None, POINTER(retro_perf_counter))
retro_perf_stop_t = CFUNCTYPE(None, POINTER(retro_perf_counter))

class retro_perf_callback(Structure):
    _fields_ = [
        ('get_time_usec', retro_perf_get_time_usec_t),
        ('get_cpu_features', retro_get_cpu_features_t),
        ('get_perf_counter', retro_perf_get_counter_t),
        ('perf_register', retro_perf_register_t),
        ('perf_start', retro_perf_start_t),
        ('perf_stop', retro_perf_stop_t),
        ('perf_log', retro_perf_log_t),
    ]

    get_time_usec: Callable[[None], c_int64]
    get_cpu_features: Callable[[None], c_uint64]
    get_perf_counter: Callable[[None], c_uint64]
    perf_register: Callable[[None], None]
    perf_start: Callable[[POINTER(retro_perf_counter)], None]
    perf_stop: Callable[[POINTER(retro_perf_counter)], None]
    perf_log: Callable[[POINTER(retro_perf_counter)], None]
