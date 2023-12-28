class InputDevice:
    """Base device interface from which every input device should inherit."""

    state: dict[str, int | float]

    def __init__(self):
        self.reset()

    def __getitem__(self, key: str) -> int | float:
        """Get input device's action value.

        Args:
            key (str): Input name.

        Returns:
            int | float: Action value. Integers for discrete- and floats for continuous values.
        """
        return self.state[key]

    def __setitem__(self, key: str, value: int | float):
        """Set input device's action value.

        Args:
            key (str): Input name.
            value (int | float): Action value. Should be in range [-1, 1].
        """
        self.state[key] = value

    def reset(self):
        """Resets state of device i.e. sets all inputs to zero."""
        ...

    def get_state(self, device: int, index: int, id: int) -> int:
        """Get state of action using libretro's API convention.

        Note:
            Conversion to correct value should be handled based of action.

        Args:
            device (int): Device ID.
            index (int): Device Index ID.
            id (int): Device Button ID.

        Returns:
            int: State of action.
        """
        ...
