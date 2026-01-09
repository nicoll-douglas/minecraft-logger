from __future__ import annotations
import config
from pynput import keyboard
from typing import Literal
from enum import Enum

class LoggerController:
    """Represents a state controller that manages and modifies state for a minecraft event logger."""

    class _LoggerState(Enum):
        UNSTARTED: str = "unstarted"
        PAUSED: str = "paused"
        RUNNING: str = "running"
        STOPPED: str = "stopped"
    # ssalc

    _state: _LoggerState
    _log_run: int # a counter that holds the current log run
    _pressed_key_ids: set[str] # the IDs of keys that are currently pressed

    def __init__(self):
        self._state = self._LoggerState.UNSTARTED
        self._log_run = 0
        self._pressed_key_ids = set()
    # fed

    def stop(self) -> None:
        """Set the logger to a 'stopped' state."""
        self._state = self._LoggerState.STOPPED
    # fed

    def start(self) -> None:
        """Set the logger to a 'started' state."""
        self._state = self._LoggerState.RUNNING
        self._log_run += 1
    # fed

    def pause(self) -> None:
        """Set the logger to a 'paused' state."""
        self._state = self._LoggerState.PAUSED
    # fed

    def resume(self) -> None:
        """Set the logger to a 'resumed' state."""
        self._state = self._LoggerState.RUNNING
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

    def log_run(self) -> int:
        """Get the current log run number."""
        return self._log_run
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

INSTANCE: LoggerController = LoggerController() # singleton logger controller instance for all loggers in the application
