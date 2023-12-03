import re

class LibRetroOption():
    options: dict

    def __init__(self, path: str = None) -> None:
        self.path = path
        self.options = {}
        if path:
            self.load(path)

    def save(self, path: str):
        with open(path, "wt", encoding="utf-8") as f:
            for key, value in self.options.items():
                f.write(f"{key} = \"{value}\"")

    def load(self, path: str):
        pattern = r'(\w+)\s*=\s*"(\w+)"'
        with open(path, "r", encoding="utf-8") as f:
            for line in f.readlines():
                match = re.search(pattern, line)
                if match:
                    self.options[match.group(1)] = match.group(2)

    def __getitem__(self, __key):
        return self.options.get(__key, None)

class PyGameOption(LibRetroOption):
    fps: int
    scaling: float

    def __init__(self, fps: int = 60, scaling: float = 1.0, path: str = None) -> None:
        super().__init__(path)
        self.fps = fps
        self.scaling = scaling

if __name__ == "__main__":
    options = LibRetroOption("C:/Users/Gerald/AppData/Local/RetroArch/config/mGBA/mGBA.opt")

    print(options["mgba_use_bios"])