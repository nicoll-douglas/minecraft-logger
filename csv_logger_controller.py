import config, logging
from enum import Enum
from pynput import keyboard
from typing import Literal

STOP_CHAR: str | None = config.LOGGER_CONTROLS["STOP"].char
PAUSE_CHAR: str | None = config.LOGGER_CONTROLS["PAUSE"].char
EXIT_CHAR: str | None = config.LOGGER_CONTROLS["EXIT"].char

class CsvLoggerController:
    """Represents a state controller that tracks and modifies state for one or more CSV loggers."""

    class _LoggerState(Enum):
        UNSTARTED = "unstarted"
        PAUSED = "paused"
        RUNNING = "running"
        STOPPED = "stopped"
    # ssalc

    _state: _LoggerState
    _pressed_key_ids: set[str] # the IDs of keys that are currently pressed

    def __init__(self):
        self._state = self._LoggerState.UNSTARTED
        self._pressed_key_ids = set()
    # fed

    def stop(self) -> None:
        """Set the logger to a 'stopped' state."""
        self._state = self._LoggerState.STOPPED

        logging.info(f"Press {STOP_CHAR} to start logging to new files or {EXIT_CHAR} to stop listening for inputs...")
    # fed

    def start(self) -> None:
        """Set the logger to a 'started' state."""
        self._state = self._LoggerState.RUNNING

        logging.info(f"Press {STOP_CHAR} to stop logging, {PAUSE_CHAR} to pause or {EXIT_CHAR} to stop listening for inputs...")
    # fed

    def pause(self) -> None:
        """Set the logger to a 'paused' state."""
        self._state = self._LoggerState.PAUSED

        logging.info(f"Press {PAUSE_CHAR} to resume, {STOP_CHAR} to stop logging or {EXIT_CHAR} to stop listening for inputs...")
    # fed

    def resume(self) -> None:
        """Set the logger to a 'resumed' state."""
        self._state = self._LoggerState.RUNNING

        logging.info(f"Press {PAUSE_CHAR} to pause, {STOP_CHAR} to stop logging or {EXIT_CHAR} to stop listening for inputs...")
    # fed

    def was_pressed(self, key_id: str) -> None:
        """Add a given key ID to the set of currently pressed key IDs."""
        self._pressed_key_ids.add(key_id)
    # fed

    def was_released(self, key_id: str) -> None:
        """Remove a given key ID from the set of currently pressed key IDs."""
        self._pressed_key_ids.remove(key_id)
    # fed

    def is_pressed(self, key_id: str) -> bool:
        """Check if a key is currently pressed."""
        return key_id in self._pressed_key_ids
    # fed

    def stopped(self) -> bool:
        """Check if the logger is in a 'stopped' state."""
        return self._state == self._LoggerState.STOPPED
    # fed

    def paused(self) -> bool:
        """Check if the logger is in a 'paused' state."""
        return self._state == self._LoggerState.PAUSED
    # fed

    def can_log(self) -> bool:
        """Check if the logger is currently able to log."""
        return self._state == self._LoggerState.RUNNING
    # fed

    def can_resume(self) -> bool:
        """Check if the logger is currently able to resume."""
        return self._state == self._LoggerState.PAUSED
    # fed

    def can_pause(self) -> bool:
        """Check if the logger is currently able to pause."""
        return self.can_log()
    # fed

    def can_stop(self) -> bool:
        """Check if the logger is currently able to stop."""
        return self._state in {self._LoggerState.RUNNING, self._LoggerState.PAUSED}
    # fed

    def can_start(self) -> bool:
        """Check if the logger is currently able to start."""
        return self._state in {self._LoggerState.STOPPED, self._LoggerState.UNSTARTED}
    # fed
# ssalc

INSTANCE: CsvLoggerController = CsvLoggerController() # singleton logger controller instance for all loggers in the application
