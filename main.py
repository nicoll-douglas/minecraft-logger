import config, logging
from pynput import keyboard, mouse
from event_handlers import handle_key_press, handle_key_release, handle_mouse_move

STOP_CHAR: str | None = config.LOGGER_CONTROLS["STOP"].char
EXIT_CHAR: str | None = config.LOGGER_CONTROLS["EXIT"].char

logging.basicConfig(level=logging.INFO)

def main() -> None:
    """Start the pynput keyboard and mouse listeners with event handlers in parallel."""
    kb_listener: keyboard.Listener = keyboard.Listener(
        on_press=handle_key_press,
        on_release=handle_key_release
    )
    mouse_listener: mouse.Listener = mouse.Listener(on_move=handle_mouse_move)

    logging.info("Listening for keyboard input...")
    logging.info("Listening for mouse input...")
    logging.info(f"Logging is currently unstarted, press {STOP_CHAR} to start logging or {EXIT_CHAR} to stop listening for inputs...")

    kb_listener.start()
    mouse_listener.start()

    kb_listener.join()
    mouse_listener.join()

    logging.info("Exiting...")
# fed

main()
