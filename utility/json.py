#!/usr/bin/env python3

import json as _json
from json import *

class json:
  def __init__(self, obj=None, *, filename=None, encoding="utf-8", ensure_ascii=False, separators=(",", ":"), **kwargs):
    self._obj = obj

    self._filename = filename
    self._dump_kwargs = kwargs
    self._dump_kwargs.update({
      "ensure_ascii": False,
      "separators": (",", ":"),
    })

    if obj:
      if self._filename:
        with open(self._filename, "w", encoding=encoding) as f:
          _json.dump(self._obj, f, **self._dump_kwargs)

    elif filename:
      with open(filename, "r", encoding=encoding) as f:
        self._obj = _json.load(f)


  def __getitem__(self, key):
    if self._obj:
      if isinstance(self._obj, list):
        try:
          return __class__(self._obj[int(key)])
        except (ValueError, IndexError):
          pass

      elif isinstance(self._obj, dict):
        return __class__(self._obj.get(str(key)))

    return __class__(None)

  def __setitem__(self, key, value):
    if self._obj:
      if isinstance(self._obj, list):
        try:
          self._obj[int(key)] = value
        except (ValueError, IndexError):
          pass

      elif isinstance(self._obj, dict):
        self._obj[str(key)] = value

  __getattr__ = __getitem__

  def __setattr__(self, name, value):
    if name[0] == "_":
      super().__setattr__(name, value)
    else:
      self[name] = value

  def __call__(self):
    return self._obj

  def __bool__(self):
    return bool(self._obj)

  def __int__(self):
    return int(self._obj)

  def __float__(self):
    return float(self._obj)

  def __repr__(self):
    return f"json({str(self._obj)})"

  def __iter__(self):
    if isinstance(self._obj, dict):
      return iter(self._obj.items())
    return iter(self._obj)


if __name__ == "__main__":
  j = json({
    "a": 1,
    "b": [1, 2],
  })

  for x in j.b:
    print(x)

  for k, v in j:
    print(k, v)

  j.a = 2
  print(j)
