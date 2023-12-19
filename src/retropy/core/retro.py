# retropy/core/retro.py

"""
Provide basic python wrapper for dll Cores.
"""

from ctypes import *

import logging
from pathlib import Path
from typing import Callable, Sequence

from . import callbacks as cb
from .renderer.framebuffer import PixelFormat
from .os.localization import Region
from .os.system import SystemInfo, SystemAvInfo
from .game import GameInfo
from .environment import EnvironmentCommand, CoreVariable
from .device import InputDescriptor
from .device.controller import ControllerInfo
from .performance import perf
from .log import LogCallback, log_printf_t
from .options import (
    OptionsDisplay,
    UpdateOptionsDisplayCallback,
    core_options_update_display_callback_t,
)


from ..utils.savestate import Savestate
from ..utils.video import buffer_to_frame, Frame
from ..utils.input import InputDevice, GamePad
from ..utils.exceptions import InvalidRomError, SavestateError
from ..utils.ptr_array import foreach

logging.basicConfig(level=logging.WARNING, format="%(levelname)-7s - %(message)s")


class RetroPy:
    """Python(ic) frontend for libretro"""

    pixel_format: PixelFormat
    core_variables: dict[bytes, dict[str, bytes | Sequence[bytes]]] = {}
    # frontend_options: dict[str, Any] = {}
    controllers: list[InputDevice] = []
    last_frame: Frame = None
    loaded: bool = False

    # region magic methods / (de)init

    def __init__(self, path: str, numpy: bool = True) -> None:
        """Loads needed DLL and initializes the libretro core

        Args:
            path (str): Path to valid ROM file
        """
        self.path = Path(path)
        self.numpy = numpy

        # Load core dll
        self.core = cdll.LoadLibrary(self.path)

        logging.info(f"Loading core: '{str(self.path)}'")

        # Create handle for environment commands
        self.env_cmd: dict[int | EnvironmentCommand, Callable[[c_void_p], bool]] = {
            EnvironmentCommand.SET_ROTATION: self.env_SET_ROTATION,
            EnvironmentCommand.GET_OVERSCAN: self.env_GET_OVERSCAN,
            EnvironmentCommand.GET_CAN_DUPE: self.env_GET_CAN_DUPE,
            EnvironmentCommand.SET_MESSAGE: self.env_SET_MESSAGE,
            EnvironmentCommand.SHUTDOWN: self.env_SHUTDOWN,
            EnvironmentCommand.SET_PERFORMANCE_LEVEL: self.env_SET_PERFORMANCE_LEVEL,
            EnvironmentCommand.GET_SYSTEM_DIRECTORY: self.env_GET_SYSTEM_DIRECTORY,
            EnvironmentCommand.SET_PIXEL_FORMAT: self.env_SET_PIXEL_FORMAT,
            EnvironmentCommand.SET_INPUT_DESCRIPTORS: self.env_SET_INPUT_DESCRIPTORS,
            EnvironmentCommand.SET_KEYBOARD_CALLBACK: self.env_SET_KEYBOARD_CALLBACK,
            EnvironmentCommand.SET_DISK_CONTROL_INTERFACE: self.env_SET_DISK_CONTROL_INTERFACE,
            EnvironmentCommand.SET_HW_RENDER: self.env_SET_HW_RENDER,
            EnvironmentCommand.GET_VARIABLE: self.env_GET_VARIABLE,
            EnvironmentCommand.SET_VARIABLES: self.env_SET_VARIABLES,
            EnvironmentCommand.GET_VARIABLE_UPDATE: self.env_GET_VARIABLE_UPDATE,
            EnvironmentCommand.SET_SUPPORT_NO_GAME: self.env_SET_SUPPORT_NO_GAME,
            EnvironmentCommand.GET_LIBRETRO_PATH: self.env_GET_LIBRETRO_PATH,
            EnvironmentCommand.SET_FRAME_TIME_CALLBACK: self.env_SET_FRAME_TIME_CALLBACK,
            EnvironmentCommand.SET_AUDIO_CALLBACK: self.env_SET_AUDIO_CALLBACK,
            EnvironmentCommand.GET_RUMBLE_INTERFACE: self.env_GET_RUMBLE_INTERFACE,
            EnvironmentCommand.GET_INPUT_DEVICE_CAPABILITIES: self.env_GET_INPUT_DEVICE_CAPABILITIES,
            EnvironmentCommand.GET_SENSOR_INTERFACE: self.env_GET_SENSOR_INTERFACE,
            EnvironmentCommand.GET_CAMERA_INTERFACE: self.env_GET_CAMERA_INTERFACE,
            EnvironmentCommand.GET_LOG_INTERFACE: self.env_GET_LOG_INTERFACE,
            EnvironmentCommand.GET_PERF_INTERFACE: self.env_GET_PERF_INTERFACE,
            EnvironmentCommand.GET_LOCATION_INTERFACE: self.env_GET_LOCATION_INTERFACE,
            EnvironmentCommand.GET_CORE_ASSETS_DIRECTORY: self.env_GET_CORE_ASSETS_DIRECTORY,
            EnvironmentCommand.GET_SAVE_DIRECTORY: self.env_GET_SAVE_DIRECTORY,
            EnvironmentCommand.SET_SYSTEM_AV_INFO: self.env_SET_SYSTEM_AV_INFO,
            EnvironmentCommand.SET_PROC_ADDRESS_CALLBACK: self.env_SET_PROC_ADDRESS_CALLBACK,
            EnvironmentCommand.SET_SUBSYSTEM_INFO: self.env_SET_SUBSYSTEM_INFO,
            EnvironmentCommand.SET_CONTROLLER_INFO: self.env_SET_CONTROLLER_INFO,
            EnvironmentCommand.SET_MEMORY_MAPS: self.env_SET_MEMORY_MAPS,
            EnvironmentCommand.SET_GEOMETRY: self.env_SET_GEOMETRY,
            EnvironmentCommand.GET_USERNAME: self.env_GET_USERNAME,
            EnvironmentCommand.GET_LANGUAGE: self.env_GET_LANGUAGE,
            EnvironmentCommand.GET_CURRENT_SOFTWARE_FRAMEBUFFER: self.env_GET_CURRENT_SOFTWARE_FRAMEBUFFER,
            EnvironmentCommand.GET_HW_RENDER_INTERFACE: self.env_GET_HW_RENDER_INTERFACE,
            EnvironmentCommand.SET_SUPPORT_ACHIEVEMENTS: self.env_SET_SUPPORT_ACHIEVEMENTS,
            EnvironmentCommand.SET_HW_RENDER_CONTEXT_NEGOTIATION_INTERFACE: self.env_SET_HW_RENDER_CONTEXT_NEGOTIATION_INTERFACE,
            EnvironmentCommand.SET_SERIALIZATION_QUIRKS: self.env_SET_SERIALIZATION_QUIRKS,
            EnvironmentCommand.SET_HW_SHARED_CONTEXT: self.env_SET_HW_SHARED_CONTEXT,
            EnvironmentCommand.GET_VFS_INTERFACE: self.env_GET_VFS_INTERFACE,
            EnvironmentCommand.GET_LED_INTERFACE: self.env_GET_LED_INTERFACE,
            EnvironmentCommand.GET_AUDIO_VIDEO_ENABLE: self.env_GET_AUDIO_VIDEO_ENABLE,
            EnvironmentCommand.GET_MIDI_INTERFACE: self.env_GET_MIDI_INTERFACE,
            EnvironmentCommand.GET_FASTFORWARDING: self.env_GET_FASTFORWARDING,
            EnvironmentCommand.GET_TARGET_REFRESH_RATE: self.env_GET_TARGET_REFRESH_RATE,
            EnvironmentCommand.GET_INPUT_BITMASKS: self.env_GET_INPUT_BITMASKS,
            EnvironmentCommand.GET_CORE_OPTIONS_VERSION: self.env_GET_CORE_OPTIONS_VERSION,
            EnvironmentCommand.SET_CORE_OPTIONS: self.env_SET_CORE_OPTIONS,
            EnvironmentCommand.SET_CORE_OPTIONS_INTL: self.env_SET_CORE_OPTIONS_INTL,
            EnvironmentCommand.SET_CORE_OPTIONS_DISPLAY: self.env_SET_CORE_OPTIONS_DISPLAY,
            EnvironmentCommand.GET_PREFERRED_HW_RENDER: self.env_GET_PREFERRED_HW_RENDER,
            EnvironmentCommand.GET_DISK_CONTROL_INTERFACE_VERSION: self.env_GET_DISK_CONTROL_INTERFACE_VERSION,
            EnvironmentCommand.SET_DISK_CONTROL_EXT_INTERFACE: self.env_SET_DISK_CONTROL_EXT_INTERFACE,
            EnvironmentCommand.GET_MESSAGE_INTERFACE_VERSION: self.env_GET_MESSAGE_INTERFACE_VERSION,
            EnvironmentCommand.SET_MESSAGE_EXT: self.env_SET_MESSAGE_EXT,
            EnvironmentCommand.GET_INPUT_MAX_USERS: self.env_GET_INPUT_MAX_USERS,
            EnvironmentCommand.SET_AUDIO_BUFFER_STATUS_CALLBACK: self.env_SET_AUDIO_BUFFER_STATUS_CALLBACK,
            EnvironmentCommand.SET_MINIMUM_AUDIO_LATENCY: self.env_SET_MINIMUM_AUDIO_LATENCY,
            EnvironmentCommand.SET_FASTFORWARDING_OVERRIDE: self.env_SET_FASTFORWARDING_OVERRIDE,
            EnvironmentCommand.SET_CONTENT_INFO_OVERRIDE: self.env_SET_CONTENT_INFO_OVERRIDE,
            EnvironmentCommand.GET_GAME_INFO_EXT: self.env_GET_GAME_INFO_EXT,
            EnvironmentCommand.SET_CORE_OPTIONS_V2: self.env_SET_CORE_OPTIONS_V2,
            EnvironmentCommand.SET_CORE_OPTIONS_V2_INTL: self.env_SET_CORE_OPTIONS_V2_INTL,
            EnvironmentCommand.SET_CORE_OPTIONS_UPDATE_DISPLAY_CALLBACK: self.env_SET_CORE_OPTIONS_UPDATE_DISPLAY_CALLBACK,
            EnvironmentCommand.SET_VARIABLE: self.env_SET_VARIABLE,
            EnvironmentCommand.GET_THROTTLE_STATE: self.env_GET_THROTTLE_STATE,
            EnvironmentCommand.GET_SAVESTATE_CONTEXT: self.env_GET_SAVESTATE_CONTEXT,
            EnvironmentCommand.GET_HW_RENDER_CONTEXT_NEGOTIATION_INTERFACE_SUPPORT: self.env_GET_HW_RENDER_CONTEXT_NEGOTIATION_INTERFACE_SUPPORT,
            EnvironmentCommand.GET_JIT_CAPABLE: self.env_GET_JIT_CAPABLE,
            EnvironmentCommand.GET_MICROPHONE_INTERFACE: self.env_GET_MICROPHONE_INTERFACE,
            EnvironmentCommand.GET_DEVICE_POWER: self.env_GET_DEVICE_POWER,
            EnvironmentCommand.SET_NETPACKET_INTERFACE: self.env_SET_NETPACKET_INTERFACE,
        }
        """Handles all libretro environment commands.
        
        Can be overwritten or expanded by sub class.
        """

        # Create callback objects (and keep them in scope)
        self.__cb_env = cb.environment_t(self.environment)
        self.__cb_video = cb.video_refresh_t(self.video_refresh)
        self.__cb_audio = cb.audio_sample_t(self.audio_sample)
        self.__cb_audio_batch = cb.audio_sample_batch_t(self.audio_sample_batch)
        self.__cb_input_poll = cb.input_poll_t(self.input_poll)
        self.__cb_input_state = cb.input_state_t(self.input_state)

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

    # endregion

    # region Core properties

    def version(self) -> int:
        """Retrieve API version

        Returns:
            int: version
        """
        return self.core.retro_api_version()

    def region(self) -> Region:
        """Retrieve cores regional code

        Returns:
            Region: region
        """
        return Region(self.core.retro_get_region())

    def system_info(self) -> SystemInfo:
        """Retrieve cores system information

        Returns:
            SystemInfo: core information
        """
        info = SystemInfo()
        self.core.retro_get_system_info(byref(info))
        return info

    def system_av_info(self) -> SystemAvInfo:
        """Retrieve cores system information specific for a game

        Returns:
            SystemAvInfo: core information
        """
        info = SystemAvInfo()
        self.core.retro_get_system_av_info(byref(info))
        return info

    # endregion

    # region Functions

    # region Not implement. Most likely useless

    # def set_player_controller(self, player: int, device: Device):
    #     """Sets the input device of a player. All player devices default to Device.JOYPAD.

    #     Args:
    #         player (int): player id
    #         device (Device): set as input device
    #     """
    #     self.core.retro_set_controller_port_device(player, device)
    #     logging.debug("Set player controller type")

    # endregion

    def load(self, path: str):
        """Load a game from ROM

        Args:
            path (str): Parh to ROM

        Raises:
            FileNotFoundError: rom file does not exist
            InvalidRomError: rom file cannot be processed
        """

        if self.loaded:
            logging.debug("Game already loaded")

        romPath = Path(path).resolve()
        if not romPath.is_file():
            raise FileNotFoundError(f"`path` ({romPath}) is not a file")

        game = GameInfo(
            path=str(romPath).encode("utf-8"), data=None, size=0, meta=b"metadata"
        )

        self.loaded = bool(self.core.retro_load_game(byref(game)))

        if not self.loaded:
            raise InvalidRomError(
                f"file '{game.path.decode('utf-8')}' cannot be loaded"
            )

        logging.info("Game loaded")

    def unload(self):
        """Unload current game

        Must be called before loading another game
        """
        self.core.retro_unload_game()
        self.loaded = False

        logging.info("Game unloaded")

    def frame_advance(self):
        """
        Run core for a single video frame
        """
        self.core.retro_run()
        return self.last_frame

    def reset(self):
        """
        Reset current game to intial state
        """
        self.core.retro_reset()
        logging.info("Game reset")

    def save_state(self) -> Savestate:
        """Save current core state

        Raises:
            SavestateError: Creating savestate failed

        Returns:
            Savestate: Savestate data
        """

        size = self.core.retro_serialize_size()
        save = Savestate(size)

        if not bool(self.core.retro_serialize(save.data, save.size)):
            raise SavestateError("Creating savestate failed")

        logging.info(f"State saved")

        return save

    def load_state(self, savestate: Savestate):
        """Load previously saved core state

        Args:
            savestate (Savestate): state to load

        Raises:
            SavestateError: Loading savestate failed
        """

        if not bool(self.core.retro_unserialize(savestate.data, savestate.size)):
            raise SavestateError("Loading savestate failed")

        logging.info(f"State loaded")

    # endregion

    # region Callbacks

    def environment(self, cmd: int, data) -> bool:
        """Handle diverse tasks

        Args:
            cmd (int): Command identifier (`RETRO_ENVIRONMENT`)
            data (c_void_p): Must be cast to correct type

        `data` has no type so it automatically recieves type when cast

        Returns:
            bool: Meaning depending on command. Return `False` to **commonly** mean a command is not supported / indicate success of action.
        """

        func = self.env_cmd.get(cmd, None)

        if func:
            return func(data)

        logging.warning(
            f"Unknown Command - cmd={cmd} (0x{cmd:X}): Consider reading the documentation / source code of the current core to support custom environment commands"
        )

        return False

    def video_refresh(self, data, width: int, height: int, pitch: int) -> None:
        """A new video frame is available

        Args:
            data (c_void_p): framebuffer (must be cast into correct format)
            width (int): width of frame
            height (int): height of frame
            pitch (int): pitch of frame line
        """
        logging.debug("Callback: video_refresh")

        # Data may be NULL if GET_CAN_DUPE returns true (libretro.h: 4381)
        if not data:
            return

        self.last_frame = buffer_to_frame(
            data, (height, width, pitch), self.pixel_format, numpy=self.numpy
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
            device (int): Device identifier (`Device`)
            index (int): Only used for analog device
            id (int): Action ID

        Returns:
            int: Value of input action
        """

        value = self.controllers[port].get_state(device, index, id)

        logging.debug("Callback: input_state")
        return value

    # endregion

    # region environment commands

    def env_UNKNOWN(self, cmd: int):
        logging.debug("SET_ROTATION (not implemented)")
        return False

    def env_SET_ROTATION(self, data) -> bool:
        logging.debug("GET_OVERSCAN (not implemented)")
        return False

    def env_GET_OVERSCAN(self, data) -> bool:
        logging.debug("GET_CAN_DUPE (not implemented)")
        return False

    def env_GET_CAN_DUPE(self, data) -> bool:
        logging.debug("SET_MESSAGE (not implemented)")
        return False

    def env_SET_MESSAGE(self, data) -> bool:
        logging.debug("SHUTDOWN (not implemented)")
        return False

    def env_SHUTDOWN(self, data) -> bool:
        logging.debug("SHUTDOWN (not implemented)")
        return False

    def env_SET_PERFORMANCE_LEVEL(self, data) -> bool:
        logging.debug("SET_PERFORMANCE_LEVEL (not implemented)")
        return False

    def env_GET_SYSTEM_DIRECTORY(self, data) -> bool:
        data = cast(data, POINTER(c_char_p)).contents

        system_directory = Path("C:/Users/Gerald/core").absolute()

        data = c_char_p(str(system_directory).encode("utf-8"))

        logging.info(f"GET_SYSTEM_DIRECTORY: {system_directory}")
        return False

    def env_SET_PIXEL_FORMAT(self, data) -> bool:
        data = cast(data, POINTER(c_int32)).contents.value

        format = PixelFormat(data)
        self.pixel_format = format

        logging.info(f"SET_PIXEL_FORMAT: {format}")
        return False

    def env_SET_INPUT_DESCRIPTORS(self, data) -> bool:
        data = cast(data, POINTER(InputDescriptor))

        # Add a controller for each player

        # input: InputDescriptor
        for input in foreach(data, lambda v: v.description):
            # print(
            #     input.port,
            #     Device(input.device),
            #     input.index,
            #     input.id,
            #     input.description,
            # )
            if input.port >= len(self.controllers):
                self.controllers.append(GamePad())

        logging.debug("SET_INPUT_DESCRIPTORS")
        return False

    def env_SET_KEYBOARD_CALLBACK(self, data) -> bool:
        logging.debug("SET_KEYBOARD_CALLBACK (not implemented)")
        return False

    def env_SET_DISK_CONTROL_INTERFACE(self, data) -> bool:
        logging.debug("SET_DISK_CONTROL_INTERFACE (not implemented)")
        return False

    def env_SET_HW_RENDER(self, data) -> bool:
        # No hardware acceleration (for now?)

        # data = cast(data, POINTER(HWRenderCallback)).contents
        # print(HwContextType(data.context_type))

        logging.debug("SET_HW_RENDER (not implemented)")
        return False

    def env_GET_VARIABLE(self, data) -> bool:
        data = cast(data, POINTER(CoreVariable)).contents

        data.value = self.core_variables[data.key]["value"]

        logging.debug(f"GET_VARIABLE: key={data.key}")
        return False

    def env_SET_VARIABLES(self, data) -> bool:
        data = cast(data, POINTER(CoreVariable))

        # variables = {}

        for var in foreach(data, lambda v: v.key and v.value):
            # variables[var.key] = RetroOption(var.value)
            desc, rest = var.value.split(b"; ")
            valid = tuple(rest.split(b"|"))
            data = valid[0]

            self.core_variables[var.key] = {
                "value": data,
                "valid": valid,
                "desc": desc,
            }

        # print(self.variables)

        logging.debug(f"SET_VARIABLES")

        return True

    def env_GET_VARIABLE_UPDATE(self, data) -> bool:
        data = cast(data, POINTER(c_bool)).contents.value

        logging.debug(f"GET_VARIABLE_UPDATE: {data}")
        return False

    def env_SET_SUPPORT_NO_GAME(self, data) -> bool:
        logging.debug("SET_SUPPORT_NO_GAME (not implemented)")
        return False

    def env_GET_LIBRETRO_PATH(self, data) -> bool:
        logging.debug("GET_LIBRETRO_PATH (not implemented)")
        return False

    def env_SET_FRAME_TIME_CALLBACK(self, data) -> bool:
        logging.debug("SET_FRAME_TIME_CALLBACK (not implemented)")
        return False

    def env_SET_AUDIO_CALLBACK(self, data) -> bool:
        logging.debug("SET_AUDIO_CALLBACK (not implemented)")
        return False

    def env_GET_RUMBLE_INTERFACE(self, data) -> bool:
        # data = cast(data, POINTER(RumbleInterface)).contents
        # self.__rumble = set_rumble_state_t(lambda *args: print("rumble:", *args))
        # data.set_rumble_state = self.__rumble

        logging.debug("GET_RUMBLE_INTERFACE")
        return False

    def env_GET_INPUT_DEVICE_CAPABILITIES(self, data) -> bool:
        logging.debug("GET_INPUT_DEVICE_CAPABILITIES (not implemented)")
        return False

    def env_GET_SENSOR_INTERFACE(self, data) -> bool:
        logging.debug("GET_SENSOR_INTERFACE (not implemented)")
        return False

    def env_GET_CAMERA_INTERFACE(self, data) -> bool:
        logging.debug("GET_CAMERA_INTERFACE (not implemented)")
        return False

        data = cast(data, POINTER(CameraCallback)).contents

        self.__cam = lambda *args: print("cam:", args)

        data.caps = 0  # raw buffer
        data.width = 100
        data.height = 100
        data.start = retro_camera_start_t(self.__cam)
        data.stop = retro_camera_stop_t(self.__cam)
        data.frame_raw_framebuffer = retro_camera_frame_raw_framebuffer_t(self.__cam)
        data.frame_opengl_texture = None
        data.initialized = retro_camera_lifetime_status_t(self.__cam)
        data.deinitialized = retro_camera_lifetime_status_t(self.__cam)

        logging.debug("GET_CAMERA_INTERFACE")

        return True

    def env_GET_LOG_INTERFACE(self, data) -> bool:
        # ctypes does not support variadic functions

        data = cast(data, POINTER(LogCallback)).contents
        self.__log = log_printf_t(lambda *args: print("LOG:", *args))
        data.log = self.__log

        logging.debug("GET_LOG_INTERFACE")

        return False

    def env_GET_PERF_INTERFACE(self, data) -> bool:
        data = cast(data, POINTER(perf.PerfCallback)).contents

        self.__perf1 = perf.perf_get_time_usec_t(
            lambda *args: print("get_time_usec:", *args)
        )
        self.__perf2 = perf.get_cpu_features_t(
            lambda *args: print("cpu_features:", *args)
        )
        self.__perf3 = perf.perf_get_counter_t(
            lambda *args: print("get_counter:", *args)
        )

        # self.__perf_counter = perf.PerfCounter()

        self.__perf4 = perf.perf_register_t(lambda *args: print("register:", *args))
        self.__perf5 = perf.perf_start_t(lambda *args: print("start:", *args))
        self.__perf6 = perf.perf_stop_t(lambda *args: print("stop:", *args))
        self.__perf7 = perf.perf_log_t(lambda: print("performance log"))

        data.get_time_usec = self.__perf1
        data.get_cpu_features = self.__perf2
        data.get_perf_counter = self.__perf3
        data.perf_register = self.__perf4
        data.perf_start = self.__perf5
        data.perf_stop = self.__perf6
        data.perf_log = self.__perf7

        self.perf_interface = data

        logging.debug("GET_PERF_INTERFACE")
        return True

    def env_GET_LOCATION_INTERFACE(self, data) -> bool:
        logging.debug("GET_LOCATION_INTERFACE (not implemented)")
        return False

    def env_GET_CORE_ASSETS_DIRECTORY(self, data) -> bool:
        logging.debug("GET_CORE_ASSETS_DIRECTORY (not implemented)")
        return False

    def env_GET_SAVE_DIRECTORY(self, data) -> bool:
        logging.debug("GET_SAVE_DIRECTORY (not implemented)")
        return False

    def env_SET_SYSTEM_AV_INFO(self, data) -> bool:
        logging.debug("SET_SYSTEM_AV_INFO (not implemented)")
        return False

    def env_SET_PROC_ADDRESS_CALLBACK(self, data) -> bool:
        logging.debug("SET_PROC_ADDRESS_CALLBACK (not implemented)")
        return False

    def env_SET_SUBSYSTEM_INFO(self, data) -> bool:
        logging.debug("SET_SUBSYSTEM_INFO (not implemented)")
        return False

    def env_SET_CONTROLLER_INFO(self, data) -> bool:
        data = cast(data, POINTER(ControllerInfo)).contents

        accepted_controller = []

        for i in range(data.num_types):
            info = data.types[i]
            accepted_controller.append((info.id, info.desc))

        # print(accepted_controller)

        logging.debug("SET_CONTROLLER_INFO")

        return True

    def env_SET_MEMORY_MAPS(self, data) -> bool:
        logging.debug("SET_MEMORY_MAPS (not implemented)")
        return False

    def env_SET_GEOMETRY(self, data) -> bool:
        logging.debug("SET_GEOMETRY (not implemented)")
        return False

    def env_GET_USERNAME(self, data) -> bool:
        logging.debug("GET_USERNAME (not implemented)")
        return False

    def env_GET_LANGUAGE(self, data) -> bool:
        logging.debug("GET_LANGUAGE (not implemented)")
        return False

    def env_GET_CURRENT_SOFTWARE_FRAMEBUFFER(self, data) -> bool:
        logging.debug("GET_CURRENT_SOFTWARE_FRAMEBUFFER (not implemented)")
        return False

    def env_GET_HW_RENDER_INTERFACE(self, data) -> bool:
        logging.debug("GET_HW_RENDER_INTERFACE (not implemented)")
        return False

    def env_SET_SUPPORT_ACHIEVEMENTS(self, data) -> bool:
        data = cast(data, POINTER(c_bool)).contents.value
        logging.info(f"SET_SUPPORT_ACHIEVEMENTS: {data}")
        return True

    def env_SET_HW_RENDER_CONTEXT_NEGOTIATION_INTERFACE(self, data) -> bool:
        logging.debug("SET_HW_RENDER_CONTEXT_NEGOTIATION_INTERFACE (not implemented)")
        return False

    def env_SET_SERIALIZATION_QUIRKS(self, data) -> bool:
        logging.debug("SET_SERIALIZATION_QUIRKS (not implemented)")
        return False

    def env_SET_HW_SHARED_CONTEXT(self, data) -> bool:
        logging.debug("SET_HW_SHARED_CONTEXT (not implemented)")
        return False

    def env_GET_VFS_INTERFACE(self, data) -> bool:
        logging.debug("GET_VFS_INTERFACE (not implemented)")
        return False

    def env_GET_LED_INTERFACE(self, data) -> bool:
        logging.debug("GET_LED_INTERFACE (not implemented)")
        return False

    def env_GET_AUDIO_VIDEO_ENABLE(self, data) -> bool:
        logging.debug("GET_AUDIO_VIDEO_ENABLE (not implemented)")
        return False

    def env_GET_MIDI_INTERFACE(self, data) -> bool:
        logging.debug("GET_MIDI_INTERFACE (not implemented)")
        return False

    def env_GET_FASTFORWARDING(self, data) -> bool:
        logging.debug("GET_FASTFORWARDING (not implemented)")
        return False

    def env_GET_TARGET_REFRESH_RATE(self, data) -> bool:
        logging.debug("GET_TARGET_REFRESH_RATE (not implemented)")
        return False

    def env_GET_INPUT_BITMASKS(self, data) -> bool:
        if data:
            data = cast(data, POINTER(c_bool)).contents.value
            ...
            # return True

        logging.debug(f"GET_INPUT_BITMASKS: {data}")
        return False

    def env_GET_CORE_OPTIONS_VERSION(self, data) -> bool:
        data = cast(data, POINTER(c_uint)).contents.value

        logging.info(f"GET_CORE_OPTIONS_VERSION: {data}")
        return False

    def env_SET_CORE_OPTIONS(self, data) -> bool:
        logging.debug("SET_CORE_OPTIONS (not implemented)")
        return False

    def env_SET_CORE_OPTIONS_INTL(self, data) -> bool:
        logging.debug("SET_CORE_OPTIONS_INTL (not implemented)")
        return False

    def env_SET_CORE_OPTIONS_DISPLAY(self, data) -> bool:
        data = cast(data, POINTER(OptionsDisplay)).contents

        logging.debug(
            f"SET_CORE_OPTIONS_DISPLAY {f'({data.key})' if data.visible else " "}"
        )
        return False

    def env_GET_PREFERRED_HW_RENDER(self, data) -> bool:
        logging.debug("GET_PREFERRED_HW_RENDER (not implemented)")
        return False

    def env_GET_DISK_CONTROL_INTERFACE_VERSION(self, data) -> bool:
        logging.debug("GET_DISK_CONTROL_INTERFACE_VERSION (not implemented)")
        return False

    def env_SET_DISK_CONTROL_EXT_INTERFACE(self, data) -> bool:
        logging.debug("SET_DISK_CONTROL_EXT_INTERFACE (not implemented)")
        return False

    def env_GET_MESSAGE_INTERFACE_VERSION(self, data) -> bool:
        logging.debug("GET_MESSAGE_INTERFACE_VERSION (not implemented)")
        return False

    def env_SET_MESSAGE_EXT(self, data) -> bool:
        logging.debug("SET_MESSAGE_EXT (not implemented)")
        return False

    def env_GET_INPUT_MAX_USERS(self, data) -> bool:
        logging.debug("GET_INPUT_MAX_USERS (not implemented)")
        return False

    def env_SET_AUDIO_BUFFER_STATUS_CALLBACK(self, data) -> bool:
        logging.debug("SET_AUDIO_BUFFER_STATUS_CALLBACK")
        return False

        if data:
            data = cast(data, POINTER(AudioBufferStatusCallback)).contents

            self.__audio_status = lambda *args: print("audio status:", args)

            data.callback = retro_audio_buffer_status_callback_t(self.__audio_status)

        logging.debug("SET_AUDIO_BUFFER_STATUS_CALLBACK")

        return True

    def env_SET_MINIMUM_AUDIO_LATENCY(self, data) -> bool:
        data = cast(data, POINTER(c_uint)).contents.value

        # self.frontend_options["min_audio_latency"] = data

        logging.debug(f"SET_MINIMUM_AUDIO_LATENCY: {data}")
        return True

    def env_SET_FASTFORWARDING_OVERRIDE(self, data) -> bool:
        logging.debug("SET_FASTFORWARDING_OVERRIDE (not implemented)")
        return False

    def env_SET_CONTENT_INFO_OVERRIDE(self, data) -> bool:
        logging.debug("SET_CONTENT_INFO_OVERRIDE (not implemented)")
        return False

    def env_GET_GAME_INFO_EXT(self, data) -> bool:
        logging.debug("GET_GAME_INFO_EXT (not implemented)")
        return False

    def env_SET_CORE_OPTIONS_V2(self, data) -> bool:
        logging.debug("SET_CORE_OPTIONS_V2 (not implemented)")
        return False

    def env_SET_CORE_OPTIONS_V2_INTL(self, data) -> bool:
        logging.debug("SET_CORE_OPTIONS_V2_INTL (not implemented)")
        return False

    def env_SET_CORE_OPTIONS_UPDATE_DISPLAY_CALLBACK(self, data) -> bool:
        data = cast(data, POINTER(UpdateOptionsDisplayCallback)).contents

        self.__options_update_display = core_options_update_display_callback_t(
            lambda: True
        )

        data.callback = self.__options_update_display

        logging.debug("SET_CORE_OPTIONS_UPDATE_DISPLAY_CALLBACK")
        return True

    def env_SET_VARIABLE(self, data) -> bool:
        logging.debug("SET_VARIABLE (not implemented)")
        return False

    def env_GET_THROTTLE_STATE(self, data) -> bool:
        logging.debug("GET_THROTTLE_STATE (not implemented)")
        return False

    def env_GET_SAVESTATE_CONTEXT(self, data) -> bool:
        logging.debug("GET_SAVESTATE_CONTEXT (not implemented)")
        return False

    def env_GET_HW_RENDER_CONTEXT_NEGOTIATION_INTERFACE_SUPPORT(self, data) -> bool:
        logging.debug(
            "GET_HW_RENDER_CONTEXT_NEGOTIATION_INTERFACE_SUPPORT (not implemented)"
        )
        return False

    def env_GET_JIT_CAPABLE(self, data) -> bool:
        logging.debug("GET_JIT_CAPABLE (not implemented)")
        return False

    def env_GET_MICROPHONE_INTERFACE(self, data) -> bool:
        logging.debug("GET_MICROPHONE_INTERFACE (not implemented)")
        return False

    def env_GET_DEVICE_POWER(self, data) -> bool:
        logging.debug("GET_DEVICE_POWER (not implemented)")
        return False

    def env_SET_NETPACKET_INTERFACE(self, data) -> bool:
        logging.debug("SET_NETPACKET_INTERFACE (not implemented)")
        return False

    # endregion
