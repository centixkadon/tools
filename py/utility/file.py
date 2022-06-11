
import os

from py.utility import *



def read(filename: str, encoding: Optional[str] = "utf-8", newline: Optional[str] = "\n"):
  try:
    with open(filename, "r", encoding=encoding, newline=newline) as f:
      return f.read()
  except FileNotFoundError:
    pass
  return None

def readb(filename: str):
  try:
    with open(filename, "rb") as f:
      return f.read()
  except FileNotFoundError:
    pass
  return None



def write(s: str, filename: str, encoding: Optional[str] = "utf-8", newline: Optional[str] = "\n"):
  os.makedirs(os.path.dirname(filename), exist_ok=True)

  while True:
    try:
      with open(filename, "w", encoding=encoding, newline=newline) as f:
        f.write(s)
        break
    except KeyboardInterrupt:
      print("writing to file, please wait")

def writeb(b: bytes, filename: str):
  os.makedirs(os.path.dirname(filename), exist_ok=True)

  while True:
    try:
      with open(filename, "wb") as f:
        f.write(b)
        break
    except KeyboardInterrupt:
      print("writing to file, please wait")
