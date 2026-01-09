import csv, logging 
from datetime import datetime
from pathlib import Path
from typing import TextIO, Literal, Any, Mapping

class CsvLogger:
    """Represents a logger that will log given events to a CSV file."""

    _file_prefix: str # the prefix before the timestamp in the log filename
    _log_fields: list[str] # the header of the CSV log file / fields that are logged
    _log_file: Path | None # the path to the current log file
    _text_stream: TextIO | None # a text stream to the current log file
    _writer: csv.DictWriter | None # a csv writer tied to the current text stream

    def __init__(self, log_fields: list[str], file_prefix: str):
        self._file_prefix = file_prefix
        self._log_fields = log_fields
        self._log_file = None
        self._text_stream = None
        self._writer = None
    # fed
 
    def pause(self) -> None:
        """Close the current text stream to pause logging to the current file."""
        if self._text_stream is not None:
            self._text_stream.close()
        # fi

        self._text_stream = None
        self._writer = None

        if self._log_file is None: return

        logging.info(f"Paused logging to {self._log_file.name}")
    # fed

    def resume(self) -> None:
        """Reopen a text stream and CSV writer to resume logging to the current file."""
        if self._log_file is None: return

        text_stream: TextIO = self._open_log_stream(self._log_file, "a")
        self._text_stream = text_stream # store new text stream

        writer: csv.DictWriter = self._create_csv_writer(text_stream)
        self._writer = writer # store new writer

        logging.info(f"Resumed logging to {self._log_file.name}")
    # fed

    def stop(self) -> None:
        """Abandon the current file and close the current text stream to stop logging to the file."""
        if self._text_stream is not None:
            self._text_stream.close()
        # fi

        self._text_stream = None
        self._writer = None

        if self._log_file is None: return

        logging.info(f"Stopped logging to {self._log_file.name}")

        self._log_file = None
    # fed

    def start(self) -> None:
        """Create a new CSV file with a header, open a new text stream to it, and open a CSV writer to start logging to the file."""
        if self._text_stream is not None:
            self._text_stream.close()
        # fi

        log_file: Path = self._create_log_file_path()
        self._log_file = log_file

        text_stream: TextIO = self._open_log_stream(log_file, "w")
        self._text_stream = text_stream # store text stream to close in future

        writer: csv.DictWriter = self._create_csv_writer(text_stream)
        self._writer = writer # store writer for future writes

        writer.writeheader()

        logging.info(f"Started logging to {self._log_file.name}")
    # fed

    def log(self, data: Mapping[str, Any]) -> None:
        """Log the given data to the current CSV file and stdout."""
        if self._writer is None: return

        self._writer.writerow(data)
    # fed

    def _open_log_stream(self, file_path: Path, mode: Literal["w", "a"]) -> TextIO:
        """Open and return a write or append text stream to a log file."""
        return file_path.open(mode, newline="", encoding="ascii")
    # fed

    def _create_log_file_path(self) -> Path:
        """Create and return a path to a new, timestamped log file in the current working directory."""
        timestamp: str = datetime.now().strftime("%Y%m%d_%H%M%S")

        return Path.cwd() / f"{self._file_prefix}_{timestamp}.csv"
    # fed

    def _create_csv_writer(self, text_stream: TextIO) -> csv.DictWriter:
        """Create and return a new CSV writer tied to the given text stream."""
        return csv.DictWriter(text_stream, fieldnames=self._log_fields)
    # fed
# ssalc
