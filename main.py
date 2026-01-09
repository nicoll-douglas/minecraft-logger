import config, logging, json
import csv_logger_controller as controller
from event_ids import KeyEventId, MouseEventId
from pynput import keyboard, mouse
from typing import Literal
from utils import translate_monitor_pos, current_timestamp, mc_is_active_window
from csv_logger import CsvLogger
from threading import Lock, Event

logging.basicConfig(level=logging.INFO)

STOP_KEY: keyboard.KeyCode = config.LOGGER_CONTROLS["STOP"]
EXIT_KEY: keyboard.KeyCode = config.LOGGER_CONTROLS["EXIT"]
PAUSE_KEY: keyboard.KeyCode = config.LOGGER_CONTROLS["PAUSE"]
EVENT_LOCK: Lock = Lock()
MOUSE_LISTENER_EXIT_EVENT: Event = Event()
KEYLOGGER: CsvLogger = CsvLogger(["key_id", "event_id", "timestamp"], "keylog")
MOUSELOGGER: CsvLogger = CsvLogger(["mouse_x", "mouse_y", "event_id", "timestamp"], "mouselog")

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
    with EVENT_LOCK:
        # handle user wants to exit
        if key == EXIT_KEY:
            KEYLOGGER.stop()
            MOUSELOGGER.stop()
            MOUSE_LISTENER_EXIT_EVENT.set()
            logging.info("Stopped listening for keyboard input")

            return False # return False to signal to pynput keyboard listener to stop
        # fi

        # pause the logger if Minecraft is not focused
        if (not mc_is_active_window()) and controller.INSTANCE.can_pause():
            KEYLOGGER.pause()
            MOUSELOGGER.pause()
            controller.INSTANCE.pause()

        # handle user wants to stop current loggers or start new loggers
        elif key == STOP_KEY:
            if controller.INSTANCE.can_start():
                KEYLOGGER.start()
                MOUSELOGGER.start()
                controller.INSTANCE.start()

            elif controller.INSTANCE.can_stop():
                KEYLOGGER.stop()
                MOUSELOGGER.stop()
                controller.INSTANCE.stop()
            # fi

        # handle user wants to pause or resume current loggers
        elif key == PAUSE_KEY:
            if controller.INSTANCE.can_resume():
                KEYLOGGER.resume()
                MOUSELOGGER.resume()
                controller.INSTANCE.resume()

            elif controller.INSTANCE.can_pause():
                KEYLOGGER.pause()
                MOUSELOGGER.pause()
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
            KEYLOGGER.log(data)
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
    with EVENT_LOCK:
        # pause the logger if Minecraft is not focused
        if (not mc_is_active_window()) and controller.INSTANCE.can_pause():
            KEYLOGGER.pause()
            MOUSELOGGER.pause()
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
            KEYLOGGER.log(data)
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
    with EVENT_LOCK:
        if MOUSE_LISTENER_EXIT_EVENT.is_set():
            logging.info("Stopped listening for mouse input")

            return False # return False to signal to pynput mouse listener to stop
        # fi

        # pause the logger if Minecraft is not focused
        if (not mc_is_active_window()) and controller.INSTANCE.can_pause():
            KEYLOGGER.pause()
            MOUSELOGGER.pause()
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

            MOUSELOGGER.log(data)
            logging.info(json.dumps(data))
        # fi

        return None
    # htiw
# fed

def main() -> None:
    """Start the pynput keyboard and mouse listeners with event handlers in parallel."""
    kb_listener: keyboard.Listener = keyboard.Listener(
        on_press=handle_key_press,
        on_release=handle_key_release
    )
    mouse_listener: mouse.Listener = mouse.Listener(on_move=handle_mouse_move)

    logging.info("Listening for keyboard input...")
    logging.info("Listening for mouse input...")
    logging.info(f"Logging is currently unstarted, press {STOP_KEY.char} to start logging or {EXIT_KEY.char} to stop listening for inputs...")

    kb_listener.start()
    mouse_listener.start()

    kb_listener.join()
    mouse_listener.join()

    logging.info("Exiting...")
# fed

main()
