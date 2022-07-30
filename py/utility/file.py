
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



def encode(s: bytes | str, encoding: Optional[str] = "utf-8", newline: Optional[str] = "\n"):
  if isinstance(s, bytes):
    return s

  if newline is not None and newline != "":
    s = s.replace("\n", newline)
  return s.encode() if encoding is None else s.encode(encoding=encoding)

def write(lines: bytes | str | Iterable[bytes] | Iterable[str], filename: str, encoding: Optional[str] = "utf-8", newline: Optional[str] = "\n"):
  if isinstance(lines, bytes):
    lines = [lines]
  elif isinstance(lines, str):
    lines = [lines]

  lines = [line if isinstance(line, bytes) else encode(line, encoding=encoding, newline=newline) for line in lines]
  b = (b"" if newline is None else encode(newline, encoding=encoding)).join(lines)

  os.makedirs(os.path.dirname(filename), exist_ok=True)

  while True:
    try:
      with open(filename, "wb") as f:
        f.write(b)
        break
    except KeyboardInterrupt:
      print("writing to file, please wait")
