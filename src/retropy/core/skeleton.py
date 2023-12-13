from ctypes import *
from typing import Callable

from .game import GameInfo
from .os.system import SystemAvInfo


class CoreDLL:
    # Callbacks
    def retro_set_environment(self, callback: Callable[[int, c_void_p], bool]) -> None:
        ...

    def retro_set_video_refresh(
        self, callback: Callable[[c_void_p, int, int, int], None]
    ) -> None:
        ...

    def retro_set_audio_sample(self, callback: Callable[[int, int], None]) -> None:
        ...

    def retro_set_audio_sample_batch(
        self, callback: Callable[[POINTER(c_int16), int], int]
    ) -> None:
        ...

    def retro_set_input_poll(self, callback: Callable[[None], None]) -> None:
        ...

    def retro_set_input_state(
        self, callback: Callable[[int, int, int, int], int]
    ) -> None:
        ...

    def retro_init(self) -> None:
        ...

    def retro_deinit(self) -> None:
        ...

    def retro_api_version(self) -> int:
        ...

    def retro_get_system_info(self, info: POINTER(retro_system_info)) -> None:
        ...

    def retro_get_system_av_info(self, info: POINTER(SystemAvInfo)) -> None:
        ...

    def retro_set_controller_port_device(self, port: int, device: int) -> None:
        ...

    def retro_reset(self) -> None:
        ...

    def retro_run(self) -> None:
        ...

    def retro_serialize_size(self) -> int:
        ...

    def retro_serialize(self, data: c_void_p, size: int) -> int:
        ...

    def retro_unserialize(self, data: c_void_p, size: int) -> int:
        ...

    def retro_cheat_reset(self) -> None:
        ...

    def retro_cheat_set(self, index: int, enabled: int, code: int):
        ...

    def retro_load_game(self, game: POINTER(GameInfo)) -> int:
        ...

    def retro_load_game_special(
        self, game_type: int, info: POINTER(GameInfo), num_info: int
    ) -> bool:
        ...

    def retro_unload_game(self) -> None:
        ...

    def retro_get_region(self) -> int:
        ...

    def retro_get_memory_data(self, id: int) -> c_void_p:
        ...

    def retro_get_memory_size(self, id: int) -> int:
        ...
