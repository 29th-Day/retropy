from ctypes import *

import logging
from pathlib import Path
from typing import Tuple, Union  # , TypeVar, Sequence, Callable, Any


from .callbacks import *
from .core import *
from .system import *
from .environment import *
from .framebuffer import *
from .input import *
from .logging import *
from .memory import *
from .camera import *
from .audio import *

from ._exceptions import *

from ..utils.savestate import Savestate
from ..utils.video import buffer_to_frame

logging.basicConfig(level=logging.WARNING)

# T = TypeVar('T')


class RetroPy:
    """Python(ic) frontend for libretro"""

    pixel_format: PIXEL_FORMAT
    variables: dict[bytes, dict[str, bytes | Tuple[bytes]]] = {}
    loaded: bool = False

    def __init__(self, path: str) -> None:
        """Loads needed DLL and initializes the libretro core

        Args:
            path (str): Path to valid ROM file
        """
        self.path = path

        # Load core dll
        self.core = cdll.LoadLibrary(self.path)

        # Create callback objects (and keep them in scope)
        self.__cb_env = retro_environment_t(self.environment)
        self.__cb_video = retro_video_refresh_t(self.video_refresh)
        self.__cb_audio = retro_audio_sample_t(self.audio_sample)
        self.__cb_audio_batch = retro_audio_sample_batch_t(self.audio_sample_batch)
        self.__cb_input_poll = retro_input_poll_t(self.input_poll)
        self.__cb_input_state = retro_input_state_t(self.input_state)

        # Register callbacks
        self.core.retro_set_environment(self.__cb_env)
        self.core.retro_set_video_refresh(self.__cb_video)
        self.core.retro_set_audio_sample(self.__cb_audio)
        self.core.retro_set_audio_sample_batch(self.__cb_audio_batch)
        self.core.retro_set_input_poll(self.__cb_input_poll)
        self.core.retro_set_input_state(self.__cb_input_state)

        # Initialize core
        self.core.retro_init()

    def __del__(self):
        self.unload()
        self.core.retro_deinit()

    # region Properties

    def version(self) -> int:
        """Retrieve API version

        Returns:
            int: version
        """
        return self.core.retro_api_version()

    def region(self) -> RETRO_REGION:
        """Retrieve cores regional code

        Returns:
            RETRO_REGION: region
        """
        return RETRO_REGION(self.core.retro_get_region())

    def system_info(self) -> retro_system_info:
        """Retrieve cores system information

        Returns:
            retro_system_info: core information (static w.r.t. core)
        """
        info = retro_system_info()
        self.core.retro_get_system_info(byref(info))
        return info

    def system_av_info(self) -> retro_system_av_info:
        """Retrieve cores system information specific for a game

        Returns:
            retro_system_av_info: core information (dynamic w.r.t. game)
        """
        info = retro_system_av_info()
        self.core.retro_get_system_av_info(byref(info))
        return info

    # endregion

    # region Functions

    def load(self, path: str) -> bool:
        """Load a game from ROM

        Args:
            path (str): Parh to ROM

        Returns:
            bool: Success
        """

        if self.loaded:
            logging.debug("Game already loaded")
            return False

        romPath = Path(path).resolve()
        if not romPath.is_file():
            raise FileNotFoundError(f"`path` ({romPath}) is not a file")

        game = retro_game_info(
            path=str(romPath).encode("utf-8"), data=None, size=0, meta=b"metadata"
        )

        self.loaded = bool(self.core.retro_load_game(byref(game)))

        logging.debug("Game loaded")

        return self.loaded

    def unload(self):
        """Unload current game

        Must be called before loading another game
        """
        self.core.retro_unload_game()
        self.loaded = False

        logging.debug("Game unloaded")

    def frame_advance(self):
        """
        Run core for a single video frame
        """
        self.core.retro_run()

    def reset(self):
        """
        Reset current game to intial state
        """
        self.core.retro_reset()
        logging.debug("Game reset")

    def saveState(self) -> Savestate | None:
        """Save current core state

        Returns:
            Savestate | None: Savestate if successful else None
        """

        size = self.core.retro_serialize_size()
        save = Savestate(size)

        success = bool(self.core.retro_serialize(save.data, save.size))

        logging.debug(f"Save State ({success})")

        return save if success else None

    def loadState(self, savestate: Savestate) -> bool:
        """Load previously saved core state

        Args:
            savestate (Savestate): state to load

        Returns:
            bool: Success
        """

        success = bool(self.core.retro_unserialize(savestate.data, savestate.size))

        logging.debug(f"Load State ({success})")

        return success

    # endregion

    # region Callbacks

    def environment(self, cmd: int, data) -> bool:
        """Handle diverse tasks

        Args:
            cmd (int): Command identifier (`RETRO_ENVIRONMENT`)
            data (c_void_p): Must be cast to correct type

        `data` has no type so it automatically recieves type when cast

        Raises:
            UnkownEnvironmentCommand: `cmd` invalid

        Returns:
            bool: Meaning depending on command
        """
        cmd = RETRO_ENVIRONMENT(cmd)

        # return False

        def foreach(array, cond):
            i = 0
            v = array[i]
            while cond(v):
                yield v
                i += 1
                v = array[i]

        if cmd == RETRO_ENVIRONMENT.UNKOWN:
            raise UnkownEnvironmentCommand()

        elif cmd == RETRO_ENVIRONMENT.GET_SYSTEM_DIRECTORY:
            data = cast(data, POINTER(c_char_p)).contents

            system_directory = Path("./core_dir/").absolute()

            data = c_char_p(str(system_directory).encode("utf-8"))

            logging.info(f"GET_SYSTEM_DIRECTORY: {system_directory}")

            return True

        elif cmd == RETRO_ENVIRONMENT.SET_PIXEL_FORMAT:
            data = cast(data, POINTER(c_int32)).contents.value

            format = PIXEL_FORMAT(data)
            self.pixel_format = format

            logging.info(f"SET_PIXEL_FORMAT: {format}")

            return True

        elif cmd == RETRO_ENVIRONMENT.SET_INPUT_DESCRIPTORS:
            data = cast(data, POINTER(retro_input_descriptor))

            # print(value)
            input: retro_input_descriptor
            for input in foreach(data, lambda v: v.description):
                # print(input.description)
                ...

            logging.debug("SET_INPUT_DESCRIPTORS")

            return True

        elif cmd == RETRO_ENVIRONMENT.GET_VARIABLE:
            data = cast(data, POINTER(retro_variable)).contents

            data.value = self.variables[data.key]["value"]

            logging.debug(f"GET_VARIABLE: key={data.key}")

            return True

        elif cmd == RETRO_ENVIRONMENT.SET_VARIABLES:
            data = cast(data, POINTER(retro_variable))

            # variables = {}

            for var in foreach(data, lambda v: v.key and v.value):
                # variables[var.key] = RetroOption(var.value)
                desc, rest = var.value.split(b"; ")
                valid = tuple(rest.split(b"|"))
                data = valid[0]

                self.variables[var.key] = {"value": data, "valid": valid, "desc": desc}

            # print(self.variables)

            logging.debug(f"SET_VARIABLES")

            return True

        elif cmd == RETRO_ENVIRONMENT.GET_VARIABLE_UPDATE:
            data = cast(data, POINTER(c_bool)).contents.value

            logging.debug(f"GET_VARIABLE_UPDATE: {data}")

            return False

        elif cmd == RETRO_ENVIRONMENT.GET_CAMERA_INTERFACE:
            return False

            data = cast(data, POINTER(retro_camera_callback)).contents

            self.__cam = lambda *args: print("cam:", args)

            data.caps = 0  # raw buffer
            data.width = 100
            data.height = 100
            data.start = retro_camera_start_t(self.__cam)
            data.stop = retro_camera_stop_t(self.__cam)
            data.frame_raw_framebuffer = retro_camera_frame_raw_framebuffer_t(
                self.__cam
            )
            data.frame_opengl_texture = None
            data.initialized = retro_camera_lifetime_status_t(self.__cam)
            data.deinitialized = retro_camera_lifetime_status_t(self.__cam)

            logging.debug("GET_CAMERA_INTERFACE")

            return True

        elif cmd == RETRO_ENVIRONMENT.GET_LOG_INTERFACE:
            return False

            data = cast(data, POINTER(retro_log_callback)).contents

            self.__log = lambda *args: print("log:", args)

            data.log = retro_log_printf_t(self.__log)

            logging.debug("GET_LOG_INTERFACE")

            return True

        elif cmd == RETRO_ENVIRONMENT.SET_MEMORY_MAPS:
            # data = cast(data, POINTER(retro_memory_map)).contents
            # print(data.num_descriptors)

            logging.debug("SET_MEMORY_MAPS")

            return True

        elif cmd == RETRO_ENVIRONMENT.SET_SUPPORT_ACHIEVEMENTS:
            data = cast(data, POINTER(c_bool)).contents.value
            logging.info(f"SET_SUPPORT_ACHIEVEMENTS: {data}")
            return True

        elif cmd == RETRO_ENVIRONMENT.GET_INPUT_BITMASKS:
            if data:
                data = cast(data, POINTER(c_bool)).contents.value
                ...
                return True

            logging.debug(f"GET_INPUT_BITMASKS: {data}")
            return False

        elif cmd == RETRO_ENVIRONMENT.GET_CORE_OPTIONS_VERSION:
            data = cast(data, POINTER(c_uint)).contents.value

            logging.info(f"GET_CORE_OPTIONS_VERSION: {data}")

            return True  # accept Options Version

        elif cmd == RETRO_ENVIRONMENT.SET_AUDIO_BUFFER_STATUS_CALLBACK:
            return False

            if data:
                data = cast(data, POINTER(retro_audio_buffer_status_callback)).contents

                self.__audio_status = lambda *args: print("audio status:", args)

                data.callback = retro_audio_buffer_status_callback_t(
                    self.__audio_status
                )

            logging.debug("SET_AUDIO_BUFFER_STATUS_CALLBACK")

            return True

        elif cmd == RETRO_ENVIRONMENT.SET_MINIMUM_AUDIO_LATENCY:
            data = cast(data, POINTER(c_uint)).contents.value

            logging.debug(f"SET_MINIMUM_AUDIO_LATENCY: {data}")

            return True

        else:
            logging.warning(f"{cmd} (not implemeted)")

        return True

    def video_refresh(
        self, data: c_void_p, width: int, height: int, pitch: int
    ) -> None:
        """A new video frame is available

        Args:
            data (c_void_p): framebuffer (must be cast into correct format)
            width (int): width of frame
            height (int): height of frame
            pitch (int): pitch of frame line
        """
        logging.debug("Callback: video_refresh")

        _ = buffer_to_frame(
            data, (width, height, pitch), self.pixel_format, numpy=False
        )

    def audio_sample(self, left: int, right: int) -> None:
        """New audio frame is available

        Args:
            left (int): left audio channel
            right (int): rigth audio channel
        """
        logging.debug("Callback: audio_sample")

    def audio_sample_batch(self, data: POINTER(c_int16), frames: int) -> int:
        """New audio frames are available

        Args:
            data (POINTER(c_uint16)): alternating left-right audio channels
            frames (int): number of audio frames

        Returns:
            int: ?
        """
        logging.debug("Callback: audio_sample_batch")

        return 0

    def input_poll(self) -> None:
        """Read frontend input"""
        logging.debug("Callback: input_poll")

    def input_state(self, port: int, device: int, index: int, id: int) -> int:
        """Pass values of `input_poll` to core

        Args:
            port (int): Player
            device (int): Device identifier (`RETRO_DEVICE`)
            index (int): Only used for analog device
            id (int): Action ID

        Returns:
            int: Value of input action
        """
        logging.debug("Callback: input_state")

        return 0

    # endregion
