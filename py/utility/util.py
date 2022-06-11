
import builtins

from py.utility import *

def is_empty(s: AnyStr) -> bool:
  return len(s) == 0

def is_not_empty(s: AnyStr) -> bool:
  return not is_empty(s)

def wrap(s: Optional[str], wrap_with: str):
  if s is None or is_empty(wrap_with):
    return s

  return f"{wrap_with}{s}{wrap_with}"

def wrap_if_missing(s: Optional[str], wrap_with: str):
  if s is None or is_empty(wrap_with):
    return s

  wrap_start = "" if s.startswith(wrap_with) else wrap_with
  wrap_end = "" if s.endswith(wrap_with) else wrap_with

  return f"{wrap_start}{s}{wrap_end}"

def hex(number: int, upper: bool = False, width: Optional[int] = None):
  s = builtins.hex(number).removeprefix("0x")
  if upper:
    s = s.upper()
  if width is not None:
    s = s.zfill(width)
  return s



def nvl(value: Optional[T], default_value: T) -> T:
  return value if value is not None else default_value

def coalesce(*values: Optional[T]) -> Optional[T]:
  for value in values:
    if value is not None:
      return value

def str_nvl(value: Optional[AnyStr], default_value: AnyStr) -> AnyStr:
  return value if value is not None and is_not_empty(value) else default_value

def str_coalesce(*values: Optional[AnyStr]) -> Optional[AnyStr]:
  for value in values:
    if value is not None and is_not_empty(value):
      return value
