from ctypes import *

from ._structs import *
from ._enums import *
from ._typedefs import *

from ._config import LibRetroOption
from ._exceptions import NoGameLoaded, GameAlreadyLoaded
from ._utils import Savestate, PlayerInput

class RetroPy:
    game_loaded: bool = False
    color_format: RETRO_COLOR_FORMAT = RETRO_COLOR_FORMAT.FORMAT_0RGB1555
    player_inputs: list[PlayerInput] = [PlayerInput()]

    def __init__(self, dll_path: str, options: LibRetroOption = None):
        self.path = dll_path
        self.options = options
        self.core = cdll.LoadLibrary(self.path)

        # weird wrapping is needed to deal with the self argument by python (which ctypes cannot handle)
        # callbacks get stored in the class to keep them in memory (https://docs.python.org/3/library/ctypes.html#ctypes-callback-functions)
        self.__cb_env = retro_environment_t(lambda *args: self.cb_environment(*args))
        self.__cb_video = retro_video_refresh_t(lambda *args: self.cb_video_refresh(*args))
        self.__cb_audio = retro_audio_sample_t(lambda *args: self.cb_audio_sample(*args))
        self.__cb_audio_batch = retro_audio_sample_batch_t(lambda *args: self.cb_audio_sample_batch(*args))
        self.__cb_input_poll = retro_input_poll_t(lambda: self.cb_input_poll())
        self.__cb_input_state = retro_input_state_t(lambda *args: self.cb_input_state(*args))

        # register the callbacks
        self.core.retro_set_environment(self.__cb_env)
        self.core.retro_set_video_refresh(self.__cb_video)
        self.core.retro_set_audio_sample(self.__cb_audio)
        self.core.retro_set_audio_sample_batch(self.__cb_audio_batch)
        self.core.retro_set_input_poll(self.__cb_input_poll)
        self.core.retro_set_input_state(self.__cb_input_state)
        # init core
        self.core.retro_init()

    def __del__(self):
        if self.game_loaded:
            self.unload_game()
        self.core.retro_deinit()

    # region setup functionality

    def api_version(self) -> int:
        """
        Get the LibRetro API version used by the core.
        
        Returns:
            int: API version
        """   
        return self.core.retro_api_version()

    def get_region(self) -> RETRO_REGION:
        """Get the region the core is based on.

        Returns:
            RETRO_REGION: Region of the core
        """
        return RETRO_REGION(self.core.retro_get_region())

    def get_system_info(self) -> retro_system_info:
        """Get general core system information.

        Returns:
            retro_system_info: Information about the core (static with core)
        """
        info = retro_system_info()
        self.core.retro_get_system_info(byref(info))
        return info

    def get_system_av_info(self) -> retro_system_av_info:
        """Get (game) system specific information from the core.

        Raises:
            exceptions.NoGameLoaded: No game was loaded prior to calling this function

        Returns:
            retro_system_av_info: Information about the core (dynamic with game)
        """
        if not self.game_loaded:
            raise NoGameLoaded("A game has to loaded before this function can be called")

        info = retro_system_av_info()
        self.core.retro_get_system_av_info(byref(info))
        return info

    def set_controller(self, port: int = 0, device: RETRO_DEVICE = RETRO_DEVICE.JOYPAD):
        """Sets the device used for a specifc port (player).

        By default, RETRO_DEVICE.JOYPAD is assumed for all ports.

        Args:
            port (int, optional): Which port / player to set the device for. Defaults to 0.
            device (RETRO_DEVICE, optional): Which device to set. Defaults to RETRO_DEVICE.JOYPAD.
        """
        self.core.retro_set_controller_port_device(c_uint32(port), c_uint32(device))

    # endregion

    # region main functionality

    def load_game(self, game: retro_game_info = None, path: str = None) -> bool:
        """Loads a game from the specified parameter.

        Note: `game` has priority over `path`

        Args:
            game (retro_game_info, optional): Information about the game
            path (str, optional): Path to the game

        Raises:
            ValueError: One of the arguments must be set.
            GameAlreadyLoaded: A game is already loaded. Unload before loading another game.

        Returns:
            bool: Wether the loading was success or not.
        """
        if self.game_loaded:
            raise GameAlreadyLoaded("A game is already loaded. Unload current game using `unload_game()` before loading a new one")

        if game is None:
            if path is None:
                raise ValueError("One of the arguments must be set.")
            else:
                game = retro_game_info(path=path.encode("utf-8"))

        success = bool(self.core.retro_load_game(byref(game)))
        if success:
            self.game_loaded = True
        return success

    # def load_game_special(self, game_type: c_uint32, game: POINTER(retro_game_info), num_info: c_size_t) -> bool:
    #     return self.core.retro_load_game_special(game_type, game, num_info)

    def reset(self):
        """Resets the current game to its initial state.
        """
        self.core.retro_reset()

    def run(self):
        """Run the game for one video frame.

        Note: Use the callback functions to access video frames and handle input.
        """
        if not self.game_loaded:
            raise NoGameLoaded("A game must be loaded before calling `run()`")

        self.core.retro_run()

    def serialize(self):
        """Saves the current (memory) state as a savestate.

        Returns:
            Savestate: A savestate / snapshot of the current state.
        """
        savestate = Savestate(size=self.core.retro_serialize_size())
        success = bool(self.core.retro_serialize(savestate.data, savestate.size))

        if success:
            return savestate
        return None

    def unserialize(self, savestate: Savestate):
        """Restores the state of the given savestate.

        Args:
            savestate (Savestate): The state to restore.

        Returns:
            bool: Wether the restoration was success or not.
        """
        return bool(self.core.retro_unserialize(savestate.data, savestate.size))

    def unload_game(self):
        """Unloads the current loaded game.

        Note: Must be used before another game is loaded.
        """
        self.core.retro_unload_game()
        self.game_loaded = False

    # endregion

    # region memory (manipulation)

    def cheat_reset(self):
        self.core.retro_cheat_reset()

    def cheat_set(self, index: c_uint32, enabled: c_bool, code: c_char_p):
        self.core.retro_cheat_set(index, enabled, code)

    def get_memory_data(self, id: c_uint32) -> c_void_p:
        return self.core.retro_get_memory_data(id)

    def get_memory_size(self, id: c_uint32) -> int:
        return self.core.retro_get_memory_size(id)

    # endregion

    # region callbacks

    def cb_environment(self, cmd: c_uint32, data: c_void_p) -> c_bool:
        """Handles uncommon tasks which would be difficult to handle otherwise in an portable way.

        *This is a callback for the core. This should NEVER be called by the frontend.*

        This may be the most complicated function in the whole wrapper. Look at the official `libretro.h`
        for more information: https://github.com/libretro/libretro-common/blob/master/include/libretro.h

        Args:
            cmd (c_uint32): The action to perform (cast into `RETRO_ENVIRONMENT` for easier handling)
            data (c_void_p): A void pointer containing the data of the action (has to be casted according to `libretro.h`)

        Returns:
            c_bool: Meaning depending on the given `cmd`
        """
        # print("set_environment")

        cmd = RETRO_ENVIRONMENT(cmd)

        # GET: get from frontend (set pointer) / SET: set in frontend (read pointer)

        if cmd == 0:
            pass
        
        # https://github.com/mgba-emu/mgba/blob/master/src/platform/libretro/libretro.h#L545
        elif cmd == RETRO_ENVIRONMENT.GET_SYSTEM_DIRECTORY:
            path = cast(data, POINTER(c_char_p))
            # TODO: change default behavior
            path_dir = (__file__[:__file__.rfind("\\") + 1]).encode("utf-8")
            path.contents = c_char_p(path_dir)
            # print(path.contents.value)
            return True

        # https://github.com/mgba-emu/mgba/blob/master/src/platform/libretro/libretro.h#L559
        elif cmd == RETRO_ENVIRONMENT.SET_PIXEL_FORMAT:
            format = cast(data, POINTER(c_int)).contents.value
            self.color_format = RETRO_COLOR_FORMAT(format)
            return True
        
        # https://github.com/mgba-emu/mgba/blob/master/src/platform/libretro/libretro.h#L570
        elif cmd == RETRO_ENVIRONMENT.SET_INPUT_DESCRIPTORS:
            array = cast(data, POINTER(retro_input_descriptor))

            inputs = []
            for i in range(30):
                var: retro_input_descriptor = array[i]
                if var.description is None:
                    break
                inputs.append(array[i])
            
            # for d in inputs:
                # print(d.description)

            return False

        # https://github.com/mgba-emu/mgba/blob/master/src/platform/libretro/libretro.h#L602
        elif cmd == RETRO_ENVIRONMENT.GET_VARIABLE:
            var = cast(data, POINTER(retro_variable))
            key: str = var.contents.key.decode("utf-8")

            # print(key, var.contents.value)
            value: str = self.options[key]
            if value is None:
                return False
            
            var.contents.value = c_char_p(value.encode("utf-8"))
            # print(var.contents.key, var.contents.value)
            return True

        # https://github.com/mgba-emu/mgba/blob/master/src/platform/libretro/libretro.h#L610
        elif cmd == RETRO_ENVIRONMENT.SET_VARIABLES:
            array = cast(data, POINTER(retro_variable))
            
            # this is hacky, range() is used as a kind of safeguard
            variables = {}
            for i in range(30):
                var: retro_variable = array[i]
                if var.key is None and var.value is None:
                    break
                variables[var.key.decode("utf-8")] = var.value.decode("utf-8")

            # print(variables)
            return True

        # https://github.com/mgba-emu/mgba/blob/master/src/platform/libretro/libretro.h#L648
        elif cmd == RETRO_ENVIRONMENT.GET_VARIABLE_UPDATE:
            updated = cast(data, POINTER(c_bool))
            # TODO: somethings wong here
            updated.contents = c_bool(True)
            # print("updated:", updated.contents.value)
            return True

        # https://github.com/mgba-emu/mgba/blob/master/src/platform/libretro/libretro.h#L738
        elif cmd == RETRO_ENVIRONMENT.GET_CAMERA_INTERFACE:
            # interface = cast(data, POINTER(retro_camera_callback))

            # if not interface.contents is None:
            #     interface = interface.contents
            #     interface.start = None
            #     interface.stop = None
            #     interface.frame_raw_framebuffer = None
            #     interface.frame_opengl_texture = None
            #     interface.initialized = None
            #     interface.deinitialized = None
            return False

        # https://github.com/mgba-emu/mgba/blob/master/src/platform/libretro/libretro.h#L763
        elif cmd == RETRO_ENVIRONMENT.GET_LOG_INTERFACE:
            # callback = cast(data, POINTER(retro_log_callback))

            # if not callback.contents is None:
            #     callback = callback.contents
            #     callback.log = None
            return False

        # https://github.com/mgba-emu/mgba/blob/master/src/platform/libretro/libretro.h#L913
        elif cmd == RETRO_ENVIRONMENT.SET_MEMORY_MAPS:
            memory_map = cast(data, POINTER(retro_memory_map)).contents

            # print(memory_map.num_descriptors)
            # print(memory_map.descriptors)
            return False

        # https://github.com/mgba-emu/mgba/blob/master/src/platform/libretro/libretro.h#L1000
        elif cmd == RETRO_ENVIRONMENT.SET_SUPPORT_ACHIEVEMENTS:
            supported = cast(data, POINTER(c_bool)).contents.value
            # print("achievements supported:", supported)
            return False

        # https://github.com/mgba-emu/mgba/blob/master/src/platform/libretro/libretro.h#L1105
        elif cmd == RETRO_ENVIRONMENT.GET_INPUT_BITMASKS:
            # if data is not None:
            #     supports_input_bitmask = cast(data, POINTER(c_bool)).contents

            #     print("support input bitmask:", supports_input_bitmask)

            return False # disable bitmask (for now?)

        # https://github.com/mgba-emu/mgba/blob/master/src/platform/libretro/libretro.h#L1117
        elif cmd == RETRO_ENVIRONMENT.GET_CORE_OPTIONS_VERSION:
            version = cast(data, POINTER(c_uint32)).contents.value
            if version == 0:
                # ...
                return False
            elif version >= 1:
                # ...
                return True
            elif version >= 2:
                # ...
                return True

        # https://github.com/mgba-emu/mgba/blob/master/src/platform/libretro/libretro.h#L1350
        elif cmd == RETRO_ENVIRONMENT.SET_AUDIO_BUFFER_STATUS_CALLBACK:
            # callback = cast(data, POINTER(retro_audio_buffer_status_callback))
            
            # callback.contents = retro_audio_buffer_status_callback()

            # if not callback is None:
            #     callback = callback.contents
            #     callback.callback = None
            return False

        # https://github.com/mgba-emu/mgba/blob/master/src/platform/libretro/libretro.h#L1359
        elif cmd == RETRO_ENVIRONMENT.SET_MINIMUM_AUDIO_LATENCY:
            # minimun_latency = cast(data, POINTER(c_uint32)).contents
            # update frontend latency
            # print("minmun latency:", minimun_latency)
            return False

        else:
            print(cmd)
            print(f"UNKNOWN COMMAND")

        return False

    def cb_video_refresh(self, data: c_void_p, width: c_uint32, height: c_uint32, pitch: c_size_t):
        """Render a frame onto the frontend.

        *This is a callback for the core. This should NEVER be called by the frontend.*

        The format of the pixels is according to TODO: ...

        Args:
            data (c_void_p): Frame in 1D form. Has to be cast into correct type and form.
            width (c_uint32): Width of the frame to render.
            height (c_uint32): Height of the frame to render.
            pitch (c_size_t): Length in bytes between two lines in buffer (width * bytes per pixel)
        """
        pass

    def cb_audio_sample(self, left: int, right: int):
        """Renders a single audio frame of left and right channel.

        *This is a callback for the core. This should NEVER be called by the frontend.
        Either `cb_audio_sample()` or `cb_audio_sample_batch()` is ever called.*

        Format is 16bit native endian.
        
        Args:
            left (int): _description_
            right (int): _description_
        """
        pass

    def cb_audio_sample_batch(self, data: POINTER(c_int16), frames: c_size_t) -> c_size_t:
        """Renders multiple audio frames in one go.

        *This is a callback for the core. This should NEVER be called by the frontend.
        Either `cb_audio_sample()` or `cb_audio_sample_batch()` is ever called.*

        Args:
            data (POINTER(c_int16)): Sample of left and right channels interleaved ([l, r, l, r, ...])
            frames (c_size_t): Number of frames the audio batch is for (data is double the length of `frames`)

        Returns:
            c_size_t: TODO: ????
        """
        return 0

    def cb_input_poll(self):
        """Reads in the input from the frontend.

        This function is used to not need to read input every single frame.

        *This is a callback for the core. This should NEVER be called by the frontend.*
        """
        pass

    def cb_input_state(self, port: c_uint32, device: c_uint32, index: c_uint32, id: c_uint32) -> c_int16:
        """Sets the read-in input for the selected port / player.

        Args:
            port (c_uint32): Port / player identifier.
            device (c_uint32): Device identifier. Use `RETRO_DEVICE` for better handling.
            index (c_uint32 / RETRO_INPUT): Index identifier (only used with RETRO_DEVICE.ANALOG controller).
            id (c_uint32): ID of a action. Use `RETRO_INPUT` for better handling.

        Returns:
            int: Value of the input action.
        """
        playerInput: PlayerInput = self.player_inputs[int(port)]
        # print(RETRO_INPUT_JOYPAD(id), value)
        if RETRO_DEVICE(device) == playerInput.device:
            return playerInput.actions.get(id, 0)
        return 0

    # endregion
