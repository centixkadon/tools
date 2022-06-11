
import logging

from py.utility import *



class LogRecord(logging.LogRecord):

  _level_styles = {
    logging.CRITICAL: ("CRITI", style.magenta),
    logging.ERROR: ("ERROR", style.red),
    logging.WARNING: ("WARN", style.yellow),
    logging.INFO: ("INFO", style.green),
    logging.DEBUG: ("DEBUG", style.white),
  }
  levelname_len = max(len(n) for n, _ in _level_styles.values())

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    self.msecs_int = int(self.msecs)
    levelname, levelname_style = self._level_styles[self.levelno]
    self.levelname = levelname_style(f"{levelname:>{self.levelname_len}}")



def basicConfig(level: int | str):
  format = "[{asctime}.{msecs_int:03}][{levelname}][{filename:36.36}{lineno:>4}]: {msg}"
  logging.basicConfig(level=level, format=format, datefmt="%Y-%m-%d %H:%M:%S", style="{")
  logging.setLogRecordFactory(LogRecord)
