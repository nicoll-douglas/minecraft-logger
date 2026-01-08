from threading import Lock
import config
from minecraft_key_logger import MinecraftKeyLogger
import logger_controller as logc
from utils import mc_is_active_window, KeyEventId
from pynput import keyboard
from typing import Literal
import logging

logging.basicConfig(level=logging.INFO)

event_lock: Lock = Lock()
keylogger: MinecraftKeyLogger = MinecraftKeyLogger()

def handle_key_press(key: keyboard.Key | keyboard.KeyCode | None) -> Literal[False] | None:
    """Handle a key press event received by pynput.

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
        get_log_filename = lambda: "" if keylogger.log_file() is None else keylogger.log_file().name

        if key == config.LOGGER_CONTROLS["EXIT"]:
            log_filename = get_log_filename() 

            if log_filename:
                logging.info("Stopped logging to " +  get_log_filename())

            keylogger.stop()

            return False # return False to signal to pynput keyboard listener to stop
        # fi

        if (not mc_is_active_window()) and logc.INSTANCE.can_pause():
            logging.info("Paused logging to " + get_log_filename())
            logc.INSTANCE.pause()
            keylogger.pause()
        elif key == config.LOGGER_CONTROLS["STOP"]:
            if logc.INSTANCE.can_start():
                logc.INSTANCE.start()
                keylogger.start()
                logging.info("Started logging to " + get_log_filename())
            elif logc.INSTANCE.can_stop():
                logging.info("Stopped logging to " + get_log_filename())
                logc.INSTANCE.stop()
                keylogger.stop()
            # fi
        elif key == config.LOGGER_CONTROLS["PAUSE"]:
            if logc.INSTANCE.can_resume():
                logging.info("Resumed logging to " + get_log_filename())
                logc.INSTANCE.resume()
                keylogger.resume()
            elif logc.INSTANCE.can_pause():
                logging.info("Paused logging to " + get_log_filename())
                logc.INSTANCE.pause()
                keylogger.pause()
            # fi
        elif logc.INSTANCE.can_log() and key in config.KEY_IDS:
            key_id: str = config.KEY_IDS[key]

            if logc.INSTANCE.is_pressed(key_id): return None

            logc.INSTANCE.was_pressed(key_id)
            keylogger.log(config.KEY_IDS[key], KeyEventId.PRESS)
        # fi

        return None
    # htiw
# fed

def handle_key_release(key: keyboard.Key | keyboard.KeyCode | None) -> None:
    """Handle a key release event received by pynput.

    If Minecraft is not the currently focused window, will pause the keylogger. 
    """
    with event_lock:
        if (not mc_is_active_window()) and logc.INSTANCE.can_pause():
            logc.INSTANCE.pause()
            keylogger.pause()

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

def main() -> None:
    """Start the pynput keyboard event listener with the keylogger event handlers in the current thread."""
    with keyboard.Listener(
        on_press=handle_key_press,
        on_release=handle_key_release
    ) as listener:
        logging.info("Listening for keyboard input...")
        listener.join()
    # htiw

    logging.info("Stopped listening for keyboard input")
# fed

main()
