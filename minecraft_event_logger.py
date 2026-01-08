import csv
from datetime import datetime
from pathlib import Path
from typing import TextIO, Literal
import logger_controller as logc

class MinecraftEventLogger:
    """Represents a logger that logs events in a Minecraft window to a file."""
    _log_fields: list[str] # the header of the CSV log file
    _log_file: Path | None # the path to the current log file
    _text_stream: TextIO | None # a text stream to the current log file
    _writer: csv.DictWriter | None # a csv writer tied to the current text stream

    def __init__(self, log_fields: list[str]):
        self._log_fields = log_fields
        self._log_file = None
        self._text_stream = None
        self._writer = None
    # fed
 
    def pause(self) -> None:
        """Pause logging to the current file.

        Will close the text stream and set the paused flag, or do nothing if the keylogger is already paused or stopped. Logging to the current file can be resumed with the `resume` method.
        """
        if self._text_stream is None: return

        self._text_stream.close()

        self._text_stream = None
        self._writer = None
    # fed

    def resume(self) -> None:
        """Resume logging to the current file.

        Will open a new text stream and a new CSV writer as well as set the paused flag. Does nothing if the keylogger is stopped or is not paused.
        """
        if self._log_file is None: return

        text_stream: TextIO = self._open_log_stream(self._log_file, "a")
        self._text_stream = text_stream # store new text stream

        writer: csv.DictWriter = self._create_csv_writer(text_stream)
        self._writer = writer # store new writer
    # fed

    def stop(self) -> None:
        """Stop logging to the current file.

        Will close the current text stream and destroy references to the current file (sets the 'flag'). Does nothing if the keylogger is already stopped.
        """
        if self._text_stream is None: return
        
        self._text_stream.close()

        self._log_file = None
        self._text_stream = None
        self._writer = None
    # fed

    def start(self) -> None:
        """Start logging to a new file.

        Will stop and clean up keylogging state to any current file, then, create a new file and open a text stream and CSV writer to it.
        """
        log_file: Path = self._create_log_file_path()
        self._log_file = log_file

        text_stream: TextIO = self._open_log_stream(log_file, "w")
        self._text_stream = text_stream # store text stream to close in future

        writer: csv.DictWriter = self._create_csv_writer(text_stream)
        self._writer = writer # store writer for future writes

        writer.writeheader()
    # fed

    def timestamp(self) -> str:
        return datetime.now().isoformat() 
    # fed

    def log_file(self) -> Path | None:
        return self._log_file
    # fed

    def _open_log_stream(self, file_path: Path, mode: Literal["w", "a"]) -> TextIO:
        """Open and return a write/append text stream to a log file."""
        return file_path.open(mode, newline="", encoding="ascii")
    # fed

    def _create_log_file_path(self) -> Path:
        """Create and return a path to a new, timestamped log file in the current working directory."""
        timestamp: str = datetime.now().strftime("%Y%m%d_%H%M%S")

        return Path.cwd() / f"keylog_{timestamp}.csv"
    # fed

    def _create_csv_writer(self, text_stream: TextIO) -> csv.DictWriter:
        """Create and return a new CSV writer tied to the given text stream.

        Arguments
        ---------
        text_stream
            An open text stream to a log file.

        Returns
        -------
        The CSV writer.
        """
        return csv.DictWriter(text_stream, fieldnames=self._log_fields)
    # fed
# ssalc
