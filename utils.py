from enum import Enum
import subprocess
from datetime import datetime
import screeninfo

def mc_is_active_window() -> bool:
    """Check if the currently active window is Lunar Client (Minecraft).
    
    Spawns xdotool subprocesses to get the window title so implementation is Linux/X11 specific.
    """
    active_window_id: bytes = subprocess.check_output(["xdotool", "getactivewindow"]).strip()
    window_title: str = subprocess.check_output(["xdotool", "getwindowname", active_window_id], text=True).strip()

    return "test_window" in window_title
# fed

def current_timestamp() -> str:
    """Get the current timestamp."""
    return datetime.now().isoformat()
# fed

def translate_global_pos_to_primary_monitor_pos(x: int, y: int) -> None | tuple[int, int]:
    """Translate the global position of the mouse pointer to local coordinates on the primary monitor."""
    monitors: list[screeninfo.common.Monitor] = screeninfo.get_monitors()
    monitor: screeninfo.common.Monitor = monitors[1] # primary monitor, implementation dependent

    x_is_on_monitor: bool = monitor.x <= x < monitor.x + monitor.width
    y_is_on_monitor: bool = monitor.y <= y < monitor.y + monitor.height

    if x_is_on_monitor and y_is_on_monitor:
        return x - monitor.x, y - monitor.y
    # fi
    
    # is on another monitor
    return None
# fi

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
