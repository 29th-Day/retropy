# How-to Guides

## Libretro API

The most important reference is the [`libretro.h`](https://github.com/libretro/libretro-common/blob/master/include/libretro.h) file. It contains all information about the workings and expectations of the API.It can be found on the official repository of libretro and open-source cores.

When ported into the Python wrapper, every objects name can deviate from the C name, but the original name should be preserved in the objects docstring.

## Custom frontend

Custom frontends can be created by inhereting the `RetroPy` class.
