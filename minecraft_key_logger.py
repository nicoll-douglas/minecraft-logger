from minecraft_event_logger import MinecraftEventLogger
from enum import Enum
from utils import KeyEventId, current_timestamp
import logging
import json

class MinecraftKeyLogger(MinecraftEventLogger):
    """Represents a keylogger that logs key events in a Minecraft window to a file."""

    def __init__(self):
        super().__init__(["key_id", "event_id", "timestamp"], "keylog") # CSV log file header and filename prefix
    # fed

    def log(self, key_id: str, event_id: KeyEventId) -> None:
        """Log a keyboard input event as a row to the current CSV file.

        Arguments
        ---------
        key_id
            The text ID associated with a key.

        event_id
            The ID of a key event type.
        """
        if self._writer is None: return

        data: dict[str, str] = {
            "key_id": key_id,
            "event_id": event_id.value,
            "timestamp": current_timestamp()
        }

        self._writer.writerow(data)
        logging.info(json.dumps(data))
    # fed
# ssalc
