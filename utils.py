from enum import Enum
import subprocess

def mc_is_active_window() -> bool:
    """Check if the currently active window is Lunar Client (Minecraft).
    
    Spawns xdotool subprocesses to get the window title so implementation is Linux/X11 specific.
    """
    active_window_id: bytes = subprocess.check_output(["xdotool", "getactivewindow"]).strip()
    window_title: str = subprocess.check_output(["xdotool", "getwindowname", active_window_id], text=True).strip()

    return "test_window" in window_title
# fed

class KeyEventId(Enum):
    """Represents the possible keyboard input event IDs."""

    PRESS = "press"
    RELEASE = "release"
# ssalc
