from pynput.keyboard import KeyCode, Key

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

LOGGER_CONTROLS: dict[str, KeyCode] = {
    "PAUSE": KeyCode.from_char("p"),
    "STOP": KeyCode.from_char("o"),
    "EXIT": KeyCode.from_char("i")
}
