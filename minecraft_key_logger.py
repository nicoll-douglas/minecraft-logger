from minecraft_event_logger import MinecraftEventLogger
from enum import Enum
from utils import KeyEventId
import logging
import json

class MinecraftKeyLogger(MinecraftEventLogger):
    """Represents a keylogger that logs key events in a Minecraft window to a file."""
    def __init__(self):
        super().__init__(["key_id", "event_id", "timestamp"])
    # fed

    def log(self, key_id: str, event_id: KeyEventId) -> None:
        """Log a key event as a row to the current CSV file.

        Does nothing if the keylogger is stopped or paused.

        Arguments
        ---------
        key_id
            A string ID representation of the key.

        event_id
            The ID of a key event type.
        """
        if self._writer is None: return None

        timestamp: str = self.timestamp()

        data: dict[str, str] = {
            "key_id": key_id,
            "event_id": event_id.value,
            "timestamp": timestamp
        }

        self._writer.writerow(data)

        logging.info(json.dumps(data))
    # fed
# ssalc
