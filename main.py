from threading import Lock, Event
import config
from minecraft_key_logger import MinecraftKeyLogger
from minecraft_mouse_logger import MinecraftMouseLogger
import logger_controller as logc
from utils import mc_is_active_window, KeyEventId, MouseEventId
from pynput import keyboard, mouse
from typing import Literal
import logging

logging.basicConfig(level=logging.INFO)

event_lock: Lock = Lock()
keylogger: MinecraftKeyLogger = MinecraftKeyLogger()
mouselogger: MinecraftMouseLogger = MinecraftMouseLogger()
mouse_listener_exit_event: Event = Event()

def handle_key_press(key: keyboard.Key | keyboard.KeyCode | None) -> Literal[False] | None:
    """Handle a key press event received by a pynput keyboard listener.

    Depending on the given key, keylogger state and currently active window, can pause, resume, stop or start the keylogger, or log the key event to a file.

    Arguments
    ---------
    key
        The key associated with the keyboard event.

    Returns
    -------
    `False` if the user pressed the exit key (stop listening to key events) otherwise `None`.
    """
    with event_lock:
        if key == config.LOGGER_CONTROLS["EXIT"]:
            keylogger.stop()
            mouselogger.stop()
            mouse_listener_exit_event.set()
            logging.info("Stopped listening for keyboard input")

            return False # return False to signal to pynput keyboard listener to stop
        # fi

        if (not mc_is_active_window()) and logc.INSTANCE.can_pause():
            logc.INSTANCE.pause()
            keylogger.pause()
            mouselogger.pause()
        elif key == config.LOGGER_CONTROLS["STOP"]:
            if logc.INSTANCE.can_start():
                logc.INSTANCE.start()
                keylogger.start()
                mouselogger.start()
            elif logc.INSTANCE.can_stop():
                logc.INSTANCE.stop()
                keylogger.stop()
                mouselogger.stop()
            # fi
        elif key == config.LOGGER_CONTROLS["PAUSE"]:
            if logc.INSTANCE.can_resume():
                logc.INSTANCE.resume()
                keylogger.resume()
                mouselogger.resume()
            elif logc.INSTANCE.can_pause():
                logc.INSTANCE.pause()
                keylogger.pause()
                mouselogger.pause()
            # fi
        elif logc.INSTANCE.can_log() and key in config.KEY_IDS:
            key_id: str = config.KEY_IDS[key]

            if logc.INSTANCE.is_pressed(key_id): return None

            logc.INSTANCE.was_pressed(key_id)
            keylogger.log(config.KEY_IDS[key], KeyEventId.PRESS)
        # fi
    # htiw

    return None
# fed

def handle_key_release(key: keyboard.Key | keyboard.KeyCode | None) -> None:
    """Handle a key release event received by a pynput keyboard listener.

    If Minecraft is not the currently focused window, will pause the keylogger. 

    Arguments
    ---------
    key
        The key associated with the keyboard event.
    """
    with event_lock:
        if (not mc_is_active_window()) and logc.INSTANCE.can_pause():
            logc.INSTANCE.pause()
            keylogger.pause()
            mouselogger.pause()

            return
        # fi

        if logc.INSTANCE.can_log() and key in config.KEY_IDS:
            key_id: str = config.KEY_IDS[key]

            if not logc.INSTANCE.is_pressed(key_id): return

            logc.INSTANCE.was_released(key_id)
            keylogger.log(config.KEY_IDS[key], KeyEventId.RELEASE)
        # fi
    # htiw
# fed

def handle_mouse_move(mouse_x: int, mouse_y: int) -> None | Literal[False]:
    """Handle a mouse move event received by a pynput mouse listener.

    If Minecraft is not the currently focused window, will pause the keylogger. 

    Arguments
    ---------
    mouse_x
        The absolute x coordinate/position of the mouse pointer after the mouse move event.

    mouse_y
        The absolute y coordinate/position of the mouse pointer after the mouse move event.
    """    
    with event_lock:
        if mouse_listener_exit_event.is_set():
            logging.info("Stopped listening for mouse input")

            return False # return False to signal to pynput mouse listener to stop
        # fi

        if (not mc_is_active_window()) and logc.INSTANCE.can_pause():
            logc.INSTANCE.pause()
            keylogger.pause()
            mouselogger.pause()

            return None
        # fi

        if logc.INSTANCE.can_log():
            mouselogger.log(mouse_x, mouse_y, MouseEventId.MOVE)
        # fi

        return None
    # htiw
# fed

def main() -> None:
    """Start the pynput keyboard and mouse listener with event handlers in parallel."""
    kb_listener: keyboard.Listener = keyboard.Listener(
        on_press=handle_key_press,
        on_release=handle_key_release
    )
    mouse_listener: mouse.Listener = mouse.Listener(on_move=handle_mouse_move)

    logging.info("Listening for keyboard input...")
    logging.info("Listening for mouse input...")

    kb_listener.start()
    mouse_listener.start()
    kb_listener.join()
    mouse_listener.join()
# fed

main()
