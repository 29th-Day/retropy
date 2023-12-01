# libretro.h

from ctypes import *

# region 4274 - 4320

retro_environment_t = CFUNCTYPE(c_bool, c_uint, c_void_p)
retro_video_refresh_t = CFUNCTYPE(None, c_void_p, c_uint, c_uint, c_size_t)
retro_audio_sample_t = CFUNCTYPE(None, c_int16, c_int16)
retro_audio_sample_batch_t = CFUNCTYPE(c_size_t, POINTER(c_int16), c_size_t)
retro_input_poll_t = CFUNCTYPE(None)
retro_input_state_t = CFUNCTYPE(c_int16, c_uint, c_uint, c_uint, c_uint)

# endregion
