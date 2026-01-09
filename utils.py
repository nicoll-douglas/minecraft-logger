import subprocess, screeninfo
from enum import Enum
from datetime import datetime

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

def translate_monitor_pos(x: int, y: int) -> None | tuple[int, int]:
    """Translate the global position of the mouse pointer across monitors to local coordinates on the primary monitor.

    The translated coordinates should be in the range 0 <= x < 1920 and 0 <= y < 1080.
    """
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
