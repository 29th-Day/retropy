class InputDevice:
    state: dict[str, int | float]

    def __init__(self):
        self.reset()

    def __getitem__(self, key: str):
        return self.state[key]

    def __setitem__(self, key: str, value: int | float):
        self.state[key] = value

    def reset(self):
        ...

    def get_state(self, device: int, index: int, id: int) -> int:
        ...
