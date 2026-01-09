import config, logging, json
import csv_logger_controller as controller
from event_ids import KeyEventId, MouseEventId
from pynput import keyboard
from typing import Literal
from utils import translate_monitor_pos, current_timestamp, mc_is_active_window
from csv_logger import CsvLogger
from threading import Lock, Event

_STOP_KEY: keyboard.KeyCode = config.LOGGER_CONTROLS["STOP"]
_EXIT_KEY: keyboard.KeyCode = config.LOGGER_CONTROLS["EXIT"]
_PAUSE_KEY: keyboard.KeyCode = config.LOGGER_CONTROLS["PAUSE"]
_EVENT_LOCK: Lock = Lock()
_MOUSE_LISTENER_EXIT_EVENT: Event = Event()
_KEYLOGGER: CsvLogger = CsvLogger(["key_id", "event_id", "timestamp"], "keylog")
_MOUSELOGGER: CsvLogger = CsvLogger(["mouse_x", "mouse_y", "event_id", "timestamp"], "mouselog")

def handle_key_press(key: keyboard.Key | keyboard.KeyCode | None) -> Literal[False] | None:
    """Handle a key press event received by a pynput keyboard listener.

    Depending on the given key, the keylogger state and currently active window, can pause, resume, stop or start loggers, or log the key event to the keylogger's file.

    Arguments
    ---------
    key
        The key associated with the key press event.

    Returns
    -------
    `False` if the user pressed the exit key (stop listening to key events) otherwise `None`.
    """
    with _EVENT_LOCK:
        # handle user wants to exit
        if key == _EXIT_KEY:
            _KEYLOGGER.stop()
            _MOUSELOGGER.stop()
            _MOUSE_LISTENER_EXIT_EVENT.set()
            logging.info("Stopped listening for keyboard input")

            return False # return False to signal to pynput keyboard listener to stop
        # fi

        # pause the logger if Minecraft is not focused
        if (not mc_is_active_window()) and controller.INSTANCE.can_pause():
            _KEYLOGGER.pause()
            _MOUSELOGGER.pause()
            controller.INSTANCE.pause()

        # handle user wants to stop current loggers or start new loggers
        elif key == _STOP_KEY:
            if controller.INSTANCE.can_start():
                _KEYLOGGER.start()
                _MOUSELOGGER.start()
                controller.INSTANCE.start()

            elif controller.INSTANCE.can_stop():
                _KEYLOGGER.stop()
                _MOUSELOGGER.stop()
                controller.INSTANCE.stop()
            # fi

        # handle user wants to pause or resume current loggers
        elif key == _PAUSE_KEY:
            if controller.INSTANCE.can_resume():
                _KEYLOGGER.resume()
                _MOUSELOGGER.resume()
                controller.INSTANCE.resume()

            elif controller.INSTANCE.can_pause():
                _KEYLOGGER.pause()
                _MOUSELOGGER.pause()
                controller.INSTANCE.pause()
            # fi

        # handle logging of key press event
        elif controller.INSTANCE.can_log() and key in config.KEY_IDS:
            key_id: str = config.KEY_IDS[key]
            
            if controller.INSTANCE.is_pressed(key_id): return None

            data: dict[str, str] = {
                "key_id": key_id,
                "event_id": KeyEventId.PRESS.value,
                "timestamp": current_timestamp()
            }

            controller.INSTANCE.was_pressed(key_id)
            _KEYLOGGER.log(data)
            logging.info(json.dumps(data))
        # fi
    # htiw

    return None
# fed

def handle_key_release(key: keyboard.Key | keyboard.KeyCode | None) -> None:
    """Handle a key release event received by a pynput keyboard listener.

    If Minecraft is not the currently focused window, will pause the mouse and key loggers.

    Arguments
    ---------
    key
        The key associated with the keyboard event.
    """
    with _EVENT_LOCK:
        # pause the logger if Minecraft is not focused
        if (not mc_is_active_window()) and controller.INSTANCE.can_pause():
            _KEYLOGGER.pause()
            _MOUSELOGGER.pause()
            controller.INSTANCE.pause()

        # handle logging of key release event
        elif controller.INSTANCE.can_log() and key in config.KEY_IDS:
            key_id: str = config.KEY_IDS[key]

            if not controller.INSTANCE.is_pressed(key_id): return

            data: dict[str, str] = {
                "key_id": key_id,
                "event_id": KeyEventId.RELEASE.value,
                "timestamp": current_timestamp()
            }

            controller.INSTANCE.was_released(key_id)
            _KEYLOGGER.log(data)
            logging.info(json.dumps(data))
        # fi
    # htiw
# fed

def handle_mouse_move(mouse_x: int, mouse_y: int) -> None | Literal[False]:
    """Handle a mouse move event received by a pynput mouse listener.

    If Minecraft is not the currently focused window, will pause the mouse and key loggers.

    Arguments
    ---------
    mouse_x
        The absolute x coordinate/position of the mouse pointer after the mouse move event.

    mouse_y
        The absolute y coordinate/position of the mouse pointer after the mouse move event.
    """    
    with _EVENT_LOCK:
        if _MOUSE_LISTENER_EXIT_EVENT.is_set():
            logging.info("Stopped listening for mouse input")

            return False # return False to signal to pynput mouse listener to stop
        # fi

        # pause the logger if Minecraft is not focused
        if (not mc_is_active_window()) and controller.INSTANCE.can_pause():
            _KEYLOGGER.pause()
            _MOUSELOGGER.pause()
            controller.INSTANCE.pause()

        # handle logging of the mouse move event
        elif controller.INSTANCE.can_log():
            pos: None | tuple[int, int] = translate_monitor_pos(mouse_x, mouse_y)

            if pos is None: return None # not on primary monitor so ignore

            data: dict[str, str | int] = {
                "mouse_x": pos[0],
                "mouse_y": pos[1],
                "event_id": MouseEventId.MOVE.value,
                "timestamp": current_timestamp()
            }

            _MOUSELOGGER.log(data)
            logging.info(json.dumps(data))
        # fi

        return None
    # htiw
# fed

