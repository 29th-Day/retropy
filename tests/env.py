__core = "C:/Users/Gerald/AppData/Local/RetroArch/cores/"

__game = "C:/Users/Gerald/AppData/Local/RetroArch/roms/"

SYSTEMS = {
    "GBA": (__core + "mgba_libretro.dll", __game + "Tetris.gb"),
    "N64": (__core + "parallel_n64_libretro.dll", __game + "Super Mario 64.n64"),
}

__all__ = ["SYSTEMS"]
