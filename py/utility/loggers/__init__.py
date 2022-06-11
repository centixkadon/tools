
import logging
from logging import CRITICAL, ERROR, WARNING, INFO, DEBUG

from py.utility import color

level_colors = {
  CRITICAL  : color.magenta,
  ERROR     : color.red,
  WARNING   : color.yellow,
  INFO      : color.green,
  DEBUG     : color.white,
}

level_names = {
  CRITICAL  : "CRITI",
  ERROR     : "ERROR",
  WARNING   : "WARN",
  INFO      : "INFO",
  DEBUG     : "DEBUG",
}

def levelname(level):
  return level_colors.get(level, color)(level_names.get(level, "NOTSET"))

CRITICAL_NAME  = levelname(CRITICAL)
ERROR_NAME     = levelname(ERROR)
WARNING_NAME   = levelname(WARNING)
INFO_NAME      = levelname(INFO)
DEBUG_NAME     = levelname(DEBUG)

class LogRecord(logging.LogRecord):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.msecs_int = int(self.msecs)
    self.levelname = level_colors.get(self.levelno, color)(f"{level_names.get(self.levelno, ''):>5}")

def config(filter_names):
  handlers = []
  for filter_name in filter_names:
    handler = logging.StreamHandler()
    handler.addFilter(logging.Filter(filter_name))
    handlers.append(handler)

  logging.basicConfig(
    format="[{asctime}.{msecs_int:03}][{levelname}][{name}][{filename:16.16}{lineno:>4}]: {msg}",
    datefmt="%Y-%m-%d %H:%M:%S",
    style="{",
    handlers=handlers)
  logging.setLogRecordFactory(LogRecord)

def get(name):
  return logging.getLogger(name)

def main():
  logger = get(__name__)
  logger.info("help2")