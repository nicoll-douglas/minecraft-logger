from enum import Enum

class KeyEventId(Enum):
    """Represents the possible keyboard input event IDs."""

    PRESS = "press"
    RELEASE = "release"
# ssalc

class MouseEventId(Enum):
    """Represents the possible mouse input event IDs."""

    MOVE = "move"
    CLICK = "click"
    SCROLL = "scroll"
# ssalc
