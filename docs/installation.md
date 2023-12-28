# Installation

## pip

```
pip install retropy
```

By default, retropy does not have any external dependencies. However, some additional features are accessable if other packages are available[^1].

``` bash
pip install retropy[numpy]  # retropy + numpy
pip install retropy[gym]    # retropy + numpy + gymnasium
pip install retropy[pygame] # retropy + numpy + pygame
pip install retropy[pyglet] # retropy + numpy + pyglet
pip install retropy[dev]    # retropy + dev dependencies
```

## Releases

Every release is archived and can be downloaded from [Releases](https://github.com/29th-Day/retropy/releases "GitHub Releases").

## Nightly Version

The current development version can be download via
```
git clone https://github.com/29th-Day/retropy.git
```

[^1]: `ModuleNotFoundError` will be raised if unavailable feature is called
