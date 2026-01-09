from pynput.keyboard import KeyCode, Key

# configuration that maps keys to text IDs
# uppercase key codes are mapped to the IDs of lower case equivalents because we want to count caps lock or shifted alphanumeric input as just the lowercase
KEY_IDS: dict[KeyCode | Key, str] = {
    KeyCode.from_char("w"): "w",
    KeyCode.from_char("a"): "a",
    KeyCode.from_char("s"): "s",
    KeyCode.from_char("d"): "d",
    KeyCode.from_char("W"): "w",
    KeyCode.from_char("A"): "a",
    KeyCode.from_char("S"): "s",
    KeyCode.from_char("D"): "d",
    Key.space: "space",
    Key.shift: "shift",
    Key.ctrl: "ctrl"
}

# configuration for controls that manage the logger
LOGGER_CONTROLS: dict[str, KeyCode] = {
    "PAUSE": KeyCode.from_char("p"), # key that pauses the logger
    "STOP": KeyCode.from_char("o"), # key that stops the logger
    "EXIT": KeyCode.from_char("i") # key that stops pynput from listening to keyboard input
}
