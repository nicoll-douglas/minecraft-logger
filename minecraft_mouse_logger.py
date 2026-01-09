from minecraft_event_logger import MinecraftEventLogger
from utils import MouseEventId, translate_global_pos_to_primary_monitor_pos, current_timestamp
import logging
import json

class MinecraftMouseLogger(MinecraftEventLogger):
    """Represents a mouse logger that logs mouse events in a Minecraft window to a file."""

    def __init__(self):
        super().__init__(["mouse_x", "mouse_y", "event_id", "timestamp"], "mouselog") # CSV log file header and filename prefix
    # fed

    def log(self, raw_mouse_x: int, raw_mouse_y: int, event_id: MouseEventId) -> None:
        """Log a mouse input event as a row to the current CSV file.

        Arguments
        ---------
        raw_mouse_x
            The raw x coordinate of the mouse input event.

        raw_mouse_y
            The raw y coordinate of the mouse input event.

        event_id
            The ID of a mouse event type.
        """
        if self._writer is None: return

        result: None | tuple[int, int] = translate_global_pos_to_primary_monitor_pos(raw_mouse_x, raw_mouse_y)

        if result is None: return # not on primary monitor so ignore

        data: dict[str, str | int] = {
            "mouse_x": result[0],
            "mouse_y": result[1],
            "event_id": event_id.value,
            "timestamp": current_timestamp()
        }

        self._writer.writerow(data)
        logging.info(json.dumps(data))
    # fed
# ssalc
