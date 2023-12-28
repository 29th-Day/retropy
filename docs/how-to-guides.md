# How-to Guides

## Libretro API

The most important reference is the [`libretro.h`](https://github.com/libretro/libretro-common/blob/master/include/libretro.h) header file. It contains all information about the workings and expectations of the API. It can be found on the official repository of libretro and open-source cores.

A basic understanding of C (and ctypes) is likely sufficient.

When ported into the Python wrapper, every objects name likely deviate from the C name, but the original name should be preserved in the objects docstring.

## Custom frontend

Custom frontends can be created by two ways

### Encapsulating the `RetroPy` class

The simple way.

It involves create additional abstraction on top of the class. The implementations are left as is and only additional functionality is added.

This should be done when no changes to the existing implementation are necessary.

### Inheriting the `RetroPy` class.

The complex way.

It involves modifying existing behavior of the implementations. Especially useful if cores have features beyond the standard API. 
