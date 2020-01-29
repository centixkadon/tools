#!/usr/bin/env python3

import os
import shutil

import logging as _logging
from logging import *

from utility.color import color

def getLevelName(level):
  return _logging.getLevelName(level).replace(" ", "")


def addLevelNames():
  os.environ["COLUMNS"], os.environ["LINES"] = (str(x) for x in shutil.get_terminal_size())

  for no, c in [(_logging.CRITICAL, color.magenta), (_logging.ERROR, color.red), (_logging.WARNING, color.yellow), (_logging.INFO, color.green), (_logging.DEBUG, color.white)]:
    _logging.addLevelName(no, c(f"{_logging.getLevelName(no):>8}"))


def setLevel(level):
  _logging.basicConfig(level=level, format="%(asctime)s.%(msecs)03d %(levelname)s %(filename)s:%(lineno)3s - %(msg)s", datefmt="%Y-%m-%d %H:%M:%S")
  # _logging.basicConfig(level=level, format="{asctime}.{msecs:03.0f} {levelname} {filename}:{lineno:3} - {msg}", datefmt="%Y-%m-%d %H:%M:%S", style="{")



def main():
  addLevelNames()
  setLevel(logging.NOTSET)

  _logging.debug("Debug")
  _logging.info("Info")
  _logging.warning("Warning")
  _logging.error("Error")
  _logging.critical("Critical")

if __name__ == "__main__":
  main()
