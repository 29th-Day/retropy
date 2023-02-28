from ctypes import CFUNCTYPE, c_int16, c_size_t, c_bool, c_uint32, c_void_p, c_int32, c_char_p, c_float, POINTER

# directly used
retro_audio_sample_t = CFUNCTYPE(None, c_int16, c_int16)
retro_audio_sample_batch_t = CFUNCTYPE(c_size_t, POINTER(c_int16), c_size_t)
retro_environment_t = CFUNCTYPE(c_bool, c_uint32, c_void_p)
retro_input_poll_t = CFUNCTYPE(None)
retro_input_state_t = CFUNCTYPE(c_int16, c_uint32, c_uint32, c_uint32, c_uint32)
retro_video_refresh_t = CFUNCTYPE(None, c_void_p, c_uint32, c_uint32, c_size_t)

# env callbacks
retro_log_printf_t = CFUNCTYPE(None, c_int32, c_char_p)
retro_audio_buffer_status_callback_t = CFUNCTYPE(None, c_bool, c_uint32, c_bool)

retro_camera_start_t = CFUNCTYPE(c_bool)
retro_camera_stop_t = CFUNCTYPE(None)
retro_camera_frame_raw_framebuffer_t = CFUNCTYPE(None, POINTER(c_uint32), c_uint32, c_uint32, c_size_t)
retro_camera_frame_opengl_texture_t = CFUNCTYPE(None, c_uint32, c_uint32, POINTER(c_float))
retro_camera_lifetime_status_t = CFUNCTYPE(None)
