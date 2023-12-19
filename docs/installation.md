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
pip install retropy[dev]    # retropy + numpy + black + mkdocs
```

## Releases

Download wanted version from [Releases](https://github.com/29th-Day/retropy/releases "GitHub Releases"). Extract to local or path-accessable folder.

## Nightly Version

1. Clone current version from repo
```
git clone https://github.com/29th-Day/retropy.git
```

2. Move `src/retropy` to local or path-accessable folder

[^1]: `ModuleNotFoundError` will be raised if unavailable feature is called
