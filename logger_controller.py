import config
from pynput import keyboard
from typing import Literal

class LoggerController:
    _paused: bool
    _stopped: bool
    _log_run: int
    _pressed_key_ids: set[str]

    def __init__(self):
        self._paused = True
        self._stopped = True
        self._log_run = 0
        self._pressed_key_ids = set()
    # fed

    def stop(self) -> None:
        self._stopped = True
    # fed

    def start(self) -> None:
        self._stopped = False
        self._paused = False
        self._log_run += 1
    # fed

    def pause(self) -> None:
        self._paused = True
    # fed

    def resume(self) -> None:
        self._paused = False
    # fed

    def was_pressed(self, key_id: str) -> None:
        self._pressed_key_ids.add(key_id)
    # fed

    def was_released(self, key_id: str) -> None:
        self._pressed_key_ids.remove(key_id)
    # fed

    def is_pressed(self, key_id: str) -> bool:
        return key_id in self._pressed_key_ids
    # fed

    def stopped(self) -> bool:
        return self._stopped
    # fed

    def paused(self) -> bool:
        return self._paused
    # fed

    def log_run(self) -> int:
        return self._log_run
    # fed

    def can_log(self) -> bool:
        return not (self._paused or self._stopped)
    # fed

    def can_resume(self) -> bool:
        return self._paused and not self._stopped
    # fed

    def can_pause(self) -> bool:
        return self.can_log()
    # fed

    def can_stop(self) -> bool:
        return not self._stopped
    # fed

    def can_start(self) -> bool:
        return self._stopped
    # fed
# ssalc

INSTANCE: LoggerController = LoggerController()
