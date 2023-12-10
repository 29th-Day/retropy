from __future__ import annotations

from ctypes import *
from ctypes import _Pointer

import logging
from pathlib import Path
from typing import Any, TypeVar, Callable, Sequence

from . import callbacks as cb
from .renderer.framebuffer import PixelFormat
from .os.localization import Region
from .os.system import SystemInfo, SystemAvInfo
from .game import GameInfo
from .environment import EnvironmentCommand, CoreVariable
from .device import InputDescriptor, Device
from .device.controller import ControllerInfo
from .performance import perf


from ..utils.savestate import Savestate
from ..utils.video import buffer_to_frame, Frame
from ..utils.input import Gamepad
from ..utils.exceptions import InvalidRomError, SavestateError

T = TypeVar('T')

logging.basicConfig(level=logging.WARNING, format="%(levelname)-7s - %(message)s")


class RetroPy:
    """Python(ic) frontend for libretro"""

    pixel_format: PixelFormat
    core_variables: dict[bytes, dict[str, bytes | Sequence[bytes]]] = {}
    frontend_options: dict[str, Any] = {}
    controllers: list[Gamepad] = []
    last_frame: Frame = None
    loaded: bool = False

    def __init__(self, path: str, numpy: bool = True) -> None:
        """Loads needed DLL and initializes the libretro core

        Args:
            path (str): Path to valid ROM file
        """
        self.path = path
        self.numpy = numpy

        # Load core dll
        self.core = cdll.LoadLibrary(self.path)

        logging.debug(f"Loading core: '{path}'")

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

    # region Properties

    def version(self) -> int:
        """Retrieve API version

        Returns:
            int: version
        """
        return self.core.retro_api_version()

    def region(self) -> Region:
        """Retrieve cores regional code

        Returns:
            RETRO_REGION: region
        """
        return Region(self.core.retro_get_region())

    def system_info(self) -> SystemInfo:
        """Retrieve cores system information

        Returns:
            retro_system_info: core information (static w.r.t. core)
        """
        info = SystemInfo()
        self.core.retro_get_system_info(byref(info))
        return info

    def system_av_info(self) -> SystemAvInfo:
        """Retrieve cores system information specific for a game

        Returns:
            retro_system_av_info: core information (dynamic w.r.t. game)
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
            return False

        romPath = Path(path).resolve()
        if not romPath.is_file():
            raise FileNotFoundError(f"`path` ({romPath}) is not a file")

        game = GameInfo(
            path=str(romPath).encode("utf-8"), data=None, size=0, meta=b"metadata"
        )

        self.loaded = bool(self.core.retro_load_game(byref(game)))

        if not self.loaded:
            raise InvalidRomError(f"file '{game}' cannot be loaded")

        logging.debug("Game loaded")

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
        return self.last_frame

    def reset(self):
        """
        Reset current game to intial state
        """
        self.core.retro_reset()
        logging.debug("Game reset")

    def save_state(self) -> Savestate:
        """Save current core state

        Raises:
            SavestateError: State could not be created

        Returns:
            Savestate: Savestate data
        """

        size = self.core.retro_serialize_size()
        save = Savestate(size)


        if not bool(self.core.retro_serialize(save.data, save.size)):
            raise SavestateError("Savestate creation failed")

        logging.debug(f"State saved")
        
        return save

    def load_state(self, savestate: Savestate):
        """Load previously saved core state

        Args:
            savestate (Savestate): state to load

        Raises:
            SavestateError: State could not be loaded
        """

        if not bool(self.core.retro_unserialize(savestate.data, savestate.size)):
            raise SavestateError("Savestate loading failed")

        logging.debug(f"State loaded")

    # endregion

    # region Callbacks

    def environment(self, cmd: int, data) -> bool:
        """Handle diverse tasks

        Args:
            cmd (int): Command identifier (`RETRO_ENVIRONMENT`)
            data (c_void_p): Must be cast to correct type

        `data` has no type so it automatically recieves type when cast

        Returns:
            bool: Meaning depending on command. Return `False` to **commonly** mean a command is not supported.
        """
        cmd = EnvironmentCommand(cmd)

        def foreach(array: _Pointer[T], cond: Callable[[T], bool]):
            i = 0
            v: T = array[i]
            while cond(v):
                yield v
                i += 1
                v = array[i]

        if cmd == EnvironmentCommand.UNKNOWN:
            logging.warning(f"{cmd.name}: cmd={cmd} (0x{cmd:X}): Consider reading the documentation / source code of the current core to support custom environment commands")

        # All are just here for easier navigation during development.
        # Some may never be used/not supported at all, so they get removed later on.

        elif cmd == EnvironmentCommand.SET_ROTATION:
            logging.debug("SET_ROTATION (not implemented)")
            return False
        
        elif cmd == EnvironmentCommand.GET_OVERSCAN:
            logging.debug("GET_OVERSCAN (not implemented)")
            return False
        
        elif cmd == EnvironmentCommand.GET_CAN_DUPE:
            logging.debug("GET_CAN_DUPE (not implemented)")
            return False
        
        elif cmd == EnvironmentCommand.SET_MESSAGE:
            logging.debug("SET_MESSAGE (not implemented)")
            return False
        
        elif cmd == EnvironmentCommand.SHUTDOWN:
            logging.debug("SHUTDOWN (not implemented)")
            return False
        
        elif cmd == EnvironmentCommand.SET_PERFORMANCE_LEVEL:
            logging.debug("SET_PERFORMANCE_LEVEL (not implemented)")
            return False

        elif cmd == EnvironmentCommand.GET_SYSTEM_DIRECTORY:
            data = cast(data, POINTER(c_char_p)).contents

            system_directory = Path("./core_dir/").absolute()

            data = c_char_p(str(system_directory).encode("utf-8"))

            logging.info(f"GET_SYSTEM_DIRECTORY: {system_directory}")

            return True

        elif cmd == EnvironmentCommand.SET_PIXEL_FORMAT:
            data = cast(data, POINTER(c_int32)).contents.value

            format = PixelFormat(data)
            self.pixel_format = format

            logging.info(f"SET_PIXEL_FORMAT: {format}")

            return True

        elif cmd == EnvironmentCommand.SET_INPUT_DESCRIPTORS:
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
                    self.controllers.append(Gamepad())
            
            logging.debug("SET_INPUT_DESCRIPTORS")

            return True

        elif cmd == EnvironmentCommand.SET_KEYBOARD_CALLBACK:
            logging.debug("SET_KEYBOARD_CALLBACK (not implemented)")
            return False
        
        elif cmd == EnvironmentCommand.SET_DISK_CONTROL_INTERFACE:
            logging.debug("SET_DISK_CONTROL_INTERFACE (not implemented)")
            return False

        elif cmd == EnvironmentCommand.SET_HW_RENDER:
            # No hardware acceleration (for now?)
            
            # data = cast(data, POINTER(HWRenderCallback)).contents
            # print(HwContextType(data.context_type))
            
            logging.debug("SET_HW_RENDER (not implemented)")
            
            return False

        elif cmd == EnvironmentCommand.GET_VARIABLE:
            data = cast(data, POINTER(CoreVariable)).contents

            data.value = self.core_variables[data.key]["value"]

            logging.debug(f"GET_VARIABLE: key={data.key}")

            return True

        elif cmd == EnvironmentCommand.SET_VARIABLES:
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

        elif cmd == EnvironmentCommand.GET_VARIABLE_UPDATE:
            data = cast(data, POINTER(c_bool)).contents.value

            logging.debug(f"GET_VARIABLE_UPDATE: {data}")

            return False

        elif cmd == EnvironmentCommand.SET_SUPPORT_NO_GAME:
            logging.debug("SET_SUPPORT_NO_GAME (not implemented)")
            return False
        
        elif cmd == EnvironmentCommand.GET_LIBRETRO_PATH:
            logging.debug("GET_LIBRETRO_PATH (not implemented)")
            return False
        
        elif cmd == EnvironmentCommand.SET_FRAME_TIME_CALLBACK:
            logging.debug("SET_FRAME_TIME_CALLBACK (not implemented)")
            return False
        
        elif cmd == EnvironmentCommand.SET_AUDIO_CALLBACK:
            logging.debug("SET_AUDIO_CALLBACK (not implemented)")
            return False
        
        elif cmd == EnvironmentCommand.GET_RUMBLE_INTERFACE:
            # data = cast(data, POINTER(RumbleInterface)).contents
            # self.__rumble = set_rumble_state_t(lambda *args: print("rumble:", *args))
            # data.set_rumble_state = self.__rumble
            
            logging.debug("GET_RUMBLE_INTERFACE")
            return False

        elif cmd == EnvironmentCommand.GET_INPUT_DEVICE_CAPABILITIES:
            logging.debug("GET_INPUT_DEVICE_CAPABILITIES (not implemented)")
            return False
        
        elif cmd == EnvironmentCommand.GET_SENSOR_INTERFACE:
            logging.debug("GET_SENSOR_INTERFACE (not implemented)")
            return False
        
        elif cmd == EnvironmentCommand.GET_CAMERA_INTERFACE:
            logging.debug("GET_CAMERA_INTERFACE (not implemented)")
            return False

            data = cast(data, POINTER(CameraCallback)).contents

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

        elif cmd == EnvironmentCommand.GET_LOG_INTERFACE:
            # ctypes does not support variadic functions

            # data = cast(data, POINTER(LogCallback)).contents
            # self.__log = log_printf_t(lambda *args: print("LOG:", *args))
            # data.log = self.__log

            logging.debug("GET_LOG_INTERFACE")

            return False

        elif cmd == EnvironmentCommand.GET_PERF_INTERFACE:
            data = cast(data, POINTER(perf.PerfCallback)).contents
            
            self.__perf1 = perf.perf_get_time_usec_t(lambda *args: print("get_time_usec:", *args))
            self.__perf2 = perf.get_cpu_features_t(lambda *args: print("cpu_features:", *args))
            self.__perf3 = perf.perf_get_counter_t(lambda *args: print("get_counter:", *args))
            
            # self.__perf_counter = perf.PerfCounter()
            
            self.__perf4 = perf.perf_register_t(lambda *args: print("register:", *args))
            self.__perf5 = perf.perf_start_t(lambda *args: print("start:", *args))
            self.__perf6 = perf.perf_stop_t(lambda *args: print("stop:", *args))
            self.__perf7 = perf.perf_log_t(lambda *args: print("log:", *args))
            
            data.get_time_usec = self.__perf1
            data.get_cpu_features = self.__perf2
            data.get_perf_counter = self.__perf3
            data.perf_register = self.__perf4
            data.perf_start = self.__perf5
            data.perf_stop = self.__perf6
            data.perf_log = self.__perf7
            
            logging.debug("GET_PERF_INTERFACE")
            return True
        
        elif cmd == EnvironmentCommand.GET_LOCATION_INTERFACE:
            logging.debug("GET_LOCATION_INTERFACE (not implemented)")
            return False
        
        elif cmd == EnvironmentCommand.GET_CORE_ASSETS_DIRECTORY:
            logging.debug("GET_CORE_ASSETS_DIRECTORY (not implemented)")
            return False
        
        elif cmd == EnvironmentCommand.GET_SAVE_DIRECTORY:
            logging.debug("GET_SAVE_DIRECTORY (not implemented)")
            return False
        
        elif cmd == EnvironmentCommand.SET_SYSTEM_AV_INFO:
            logging.debug("SET_SYSTEM_AV_INFO (not implemented)")
            return False
        
        elif cmd == EnvironmentCommand.SET_PROC_ADDRESS_CALLBACK:
            logging.debug("SET_PROC_ADDRESS_CALLBACK (not implemented)")
            return False
        
        elif cmd == EnvironmentCommand.SET_SUBSYSTEM_INFO:
            logging.debug("SET_SUBSYSTEM_INFO (not implemented)")
            return False

        elif cmd == EnvironmentCommand.SET_CONTROLLER_INFO:
            data = cast(data, POINTER(ControllerInfo)).contents
            
            accepted_controller = []
            
            for i in range(data.num_types):
                info = data.types[i]
                accepted_controller.append((info.id, info.desc))
            
            # print(accepted_controller)
            
            logging.debug("SET_CONTROLLER_INFO")
            
            return True

        elif cmd == EnvironmentCommand.SET_MEMORY_MAPS:
            # data = cast(data, POINTER(retro_memory_map)).contents
            # print(data.num_descriptors)

            logging.debug("SET_MEMORY_MAPS (not implemented)")

            return False

        elif cmd == EnvironmentCommand.SET_GEOMETRY:
            logging.debug("SET_GEOMETRY (not implemented)")
            return False
        
        elif cmd == EnvironmentCommand.GET_USERNAME:
            logging.debug("GET_USERNAME (not implemented)")
            return False
        
        elif cmd == EnvironmentCommand.GET_LANGUAGE:
            logging.debug("GET_LANGUAGE (not implemented)")
            return False
        
        elif cmd == EnvironmentCommand.GET_CURRENT_SOFTWARE_FRAMEBUFFER:
            logging.debug("GET_CURRENT_SOFTWARE_FRAMEBUFFER (not implemented)")
            return False
        
        elif cmd == EnvironmentCommand.GET_HW_RENDER_INTERFACE:
            logging.debug("GET_HW_RENDER_INTERFACE (not implemented)")
            return False

        elif cmd == EnvironmentCommand.SET_SUPPORT_ACHIEVEMENTS:
            data = cast(data, POINTER(c_bool)).contents.value
            logging.info(f"SET_SUPPORT_ACHIEVEMENTS: {data}")
            return True

        elif cmd == EnvironmentCommand.SET_HW_RENDER_CONTEXT_NEGOTIATION_INTERFACE:
            logging.debug("SET_HW_RENDER_CONTEXT_NEGOTIATION_INTERFACE (not implemented)")
            return False
        
        elif cmd == EnvironmentCommand.SET_SERIALIZATION_QUIRKS:
            logging.debug("SET_SERIALIZATION_QUIRKS (not implemented)")
            return False
        
        elif cmd == EnvironmentCommand.SET_HW_SHARED_CONTEXT:
            logging.debug("SET_HW_SHARED_CONTEXT (not implemented)")
            return False
        
        elif cmd == EnvironmentCommand.GET_VFS_INTERFACE:
            logging.debug("GET_VFS_INTERFACE (not implemented)")
            return False
        
        elif cmd == EnvironmentCommand.GET_LED_INTERFACE:
            logging.debug("GET_LED_INTERFACE (not implemented)")
            return False
        
        elif cmd == EnvironmentCommand.GET_AUDIO_VIDEO_ENABLE:
            logging.debug("GET_AUDIO_VIDEO_ENABLE (not implemented)")
            return False
        
        elif cmd == EnvironmentCommand.GET_MIDI_INTERFACE:
            logging.debug("GET_MIDI_INTERFACE (not implemented)")
            return False
        
        elif cmd == EnvironmentCommand.GET_FASTFORWARDING:
            logging.debug("GET_FASTFORWARDING (not implemented)")
            return False
        
        elif cmd == EnvironmentCommand.GET_TARGET_REFRESH_RATE:
            logging.debug("GET_TARGET_REFRESH_RATE (not implemented)")
            return False

        elif cmd == EnvironmentCommand.GET_INPUT_BITMASKS:
            if data:
                data = cast(data, POINTER(c_bool)).contents.value
                ...
                # return True

            logging.debug(f"GET_INPUT_BITMASKS: {data}")
            return False

        elif cmd == EnvironmentCommand.GET_CORE_OPTIONS_VERSION:
            data = cast(data, POINTER(c_uint)).contents.value

            logging.info(f"GET_CORE_OPTIONS_VERSION: {data}")

            return True  # accept Options Version

        elif cmd == EnvironmentCommand.SET_CORE_OPTIONS:
            logging.debug("SET_CORE_OPTIONS (not implemented)")
            return False
        
        elif cmd == EnvironmentCommand.SET_CORE_OPTIONS_INTL:
            logging.debug("SET_CORE_OPTIONS_INTL (not implemented)")
            return False
        
        elif cmd == EnvironmentCommand.SET_CORE_OPTIONS_DISPLAY:
            logging.debug("SET_CORE_OPTIONS_DISPLAY (not implemented)")
            return False
        
        elif cmd == EnvironmentCommand.GET_PREFERRED_HW_RENDER:
            logging.debug("GET_PREFERRED_HW_RENDER (not implemented)")
            return False
        
        elif cmd == EnvironmentCommand.GET_DISK_CONTROL_INTERFACE_VERSION:
            logging.debug("GET_DISK_CONTROL_INTERFACE_VERSION (not implemented)")
            return False
        
        elif cmd == EnvironmentCommand.SET_DISK_CONTROL_EXT_INTERFACE:
            logging.debug("SET_DISK_CONTROL_EXT_INTERFACE (not implemented)")
            return False
        
        elif cmd == EnvironmentCommand.GET_MESSAGE_INTERFACE_VERSION:
            logging.debug("GET_MESSAGE_INTERFACE_VERSION (not implemented)")
            return False
        
        elif cmd == EnvironmentCommand.SET_MESSAGE_EXT:
            logging.debug("SET_MESSAGE_EXT (not implemented)")
            return False
        
        elif cmd == EnvironmentCommand.GET_INPUT_MAX_USERS:
            logging.debug("GET_INPUT_MAX_USERS (not implemented)")
            return False

        elif cmd == EnvironmentCommand.SET_AUDIO_BUFFER_STATUS_CALLBACK:
            logging.debug("SET_AUDIO_BUFFER_STATUS_CALLBACK")
            return False

            if data:
                data = cast(data, POINTER(AudioBufferStatusCallback)).contents

                self.__audio_status = lambda *args: print("audio status:", args)

                data.callback = retro_audio_buffer_status_callback_t(
                    self.__audio_status
                )

            logging.debug("SET_AUDIO_BUFFER_STATUS_CALLBACK")

            return True

        elif cmd == EnvironmentCommand.SET_MINIMUM_AUDIO_LATENCY:
            data = cast(data, POINTER(c_uint)).contents.value

            self.frontend_options["min_audio_latency"] = data

            logging.debug(f"SET_MINIMUM_AUDIO_LATENCY: {data}")
            return True

        elif cmd == EnvironmentCommand.SET_FASTFORWARDING_OVERRIDE:
            logging.debug("SET_FASTFORWARDING_OVERRIDE (not implemented)")
            return False
        
        elif cmd == EnvironmentCommand.SET_CONTENT_INFO_OVERRIDE:
            logging.debug("SET_CONTENT_INFO_OVERRIDE (not implemented)")
            return False
        
        elif cmd == EnvironmentCommand.GET_GAME_INFO_EXT:
            logging.debug("GET_GAME_INFO_EXT (not implemented)")
            return False
        
        elif cmd == EnvironmentCommand.SET_CORE_OPTIONS_V2:
            logging.debug("SET_CORE_OPTIONS_V2 (not implemented)")
            return False
        
        elif cmd == EnvironmentCommand.SET_CORE_OPTIONS_V2_INTL:
            logging.debug("SET_CORE_OPTIONS_V2_INTL (not implemented)")
            return False
        
        elif cmd == EnvironmentCommand.SET_CORE_OPTIONS_UPDATE_DISPLAY_CALLBACK:
            logging.debug("SET_CORE_OPTIONS_UPDATE_DISPLAY_CALLBACK (not implemented)")
            return False
        
        elif cmd == EnvironmentCommand.SET_VARIABLE:
            logging.debug("SET_VARIABLE (not implemented)")
            return False
        
        elif cmd == EnvironmentCommand.GET_THROTTLE_STATE:
            logging.debug("GET_THROTTLE_STATE (not implemented)")
            return False
        
        elif cmd == EnvironmentCommand.GET_SAVESTATE_CONTEXT:
            logging.debug("GET_SAVESTATE_CONTEXT (not implemented)")
            return False
        
        elif cmd == EnvironmentCommand.GET_HW_RENDER_CONTEXT_NEGOTIATION_INTERFACE_SUPPORT:
            logging.debug("GET_HW_RENDER_CONTEXT_NEGOTIATION_INTERFACE_SUPPORT (not implemented)")
            return False
        
        elif cmd == EnvironmentCommand.GET_JIT_CAPABLE:
            logging.debug("GET_JIT_CAPABLE (not implemented)")
            return False
        
        elif cmd == EnvironmentCommand.GET_MICROPHONE_INTERFACE:
            logging.debug("GET_MICROPHONE_INTERFACE (not implemented)")
            return False
        
        elif cmd == EnvironmentCommand.GET_DEVICE_POWER:
            logging.debug("GET_DEVICE_POWER (not implemented)")
            return False
        
        elif cmd == EnvironmentCommand.SET_NETPACKET_INTERFACE:
            logging.debug("SET_NETPACKET_INTERFACE (not implemented)")
            return False

        else:
            logging.warning(f"{cmd} (not implemeted)")

        return False

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
            device (int): Device identifier (`RETRO_DEVICE`)
            index (int): Only used for analog device
            id (int): Action ID

        Returns:
            int: Value of input action
        """

        value = self.controllers[port].get_state(Device(device), index, id)

        logging.debug("Callback: input_state")
        return value

    # endregion
