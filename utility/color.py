#!/usr/bin/env python3

"""Print colored text

Colors and formatting
  Formatting
    "^[[${CODE}m"  ("^[" is "\e" or "\\033")
     0  Reset all
     1  Bold
     2  Dim
     4  Underlined
     5  Blink
     7  Reverse
     8  Hidden
    2*  Reset
  8/16 Colors
     "^[[3${CODE}m"   Foreground (Dark)
     "^[[9${CODE}m"   Foreground
     "^[[4${CODE}m"   Background (Dark)
    "^[[10${CODE}m"   Background
     0  Black
     1  Red
     2  Green
     3  Yellow
     4  Blue
     5  Magenta
     6  Cyan
     7  White
     9  Default
  88/256 Colors
    "^[[38;5;${CODE}m" Foreground
    "^[[48;5;${CODE}m" Background
      0 <= CODE <  16:  CODE=8/16 Colors
     16 <= CODE < 232:  CODE=$((${RED} * 36 + ${GREEN} * 6 + ${BLUE} + 16))
    232 <= CODE < 256:  CODE=$((${GREY} + 232))
"""

import os
import platform

__author__ = "centixkadon"
__version__ = [0, 2, 0]

if platform.system() == "Windows":
  os.system("color")

class color:
  _colors = dict(zip(["black", "red", "green", "yellow", "blue", "magenta", "cyan", "white"], range(8)))

  def __init__(self, bold=True, underlined=False, fg=None, bg=None):
    self._bold, self._underlined, self._fg, self._bg = bold, underlined, fg, bg

  def __getattr__(self, c):
    if c.lower() == "default":
      return __class__()

    if c.lower() == "bold":
      return __class__(not self._bold, self._underlined, self._fg, self._bg)
    if c == "b":
      return __class__(False, self._underlined, self._fg, self._bg)
    if c == "B":
      return __class__(True, self._underlined, self._fg, self._bg)

    if c.lower() == "underlined":
      return __class__(self._bold, not self._underlined, self._fg, self._bg)
    if c == "u":
      return __class__(self._bold, False, self._fg, self._bg)
    if c == "U":
      return __class__(self._bold, True, self._fg, self._bg)

    if c.lower() in self._colors:
      return __class__(self._bold, **dict({"fg": self._fg, "bg": self._bg}, **{"fg" if c == c.lower() else "bg": self._colors[c.lower()]}))

    if c.lower() == "gray":
      def gray(i):
        if 1 <= i <= 24:
          return __class__(self._bold, **dict({"fg": self._fg, "bg": self._bg}, **{"fg" if c == c.lower() else "bg": i + 231}))
        raise KeyError("gray should be in [1, 24]")
      return gray

    if c.lower() == "rgb":
      def rgb(r, g, b):
        if 0 <= r < 6 and 0 <= g < 6 and 0 <= b < 6:
          return __class__(self._bold, **dict({"fg": self._fg, "bg": self._bg}, **{"fg" if c == c.lower() else "bg": r * 36 + g * 6 + b + 16}))
        raise KeyError("rgb should be in [0, 6)")
      return rgb
    raise KeyError("color is not correct")

  __getitem__ = __getattr__

  def __call__(self, s):
    fg = "" if self._fg is None else f";{self._fg + 30}" if self._fg < 8 else f";{self._fg + 82}" if self._fg < 16 else f";38;5;{self._fg:>03}"
    bg = "" if self._bg is None else f";{self._bg + 40}" if self._bg < 8 else f";{self._bg + 92}" if self._bg < 16 else f";48;5;{self._bg:>03}"
    return "" if s == "" else f"\033[{'1' if self._bold else '0'}{fg}{bg}m{s}\033[0m"

color = color()


def main():
  print(f'{"System colors":^152}')
  print(f'+{"":-<56}+     +{"":-<56}+     +{"":-<24}+')
  print("|", end="")
  for c in color._colors:
    print(color[c](f'{c:^7}'), end="")
  print("|     |", end="")
  for c in color._colors:
    print(color[c].bold(f'{c:^7}'), end="")
  print("|     |", end="")
  for c in color._colors:
    print(color[c.upper()](" . "), end="")
  print("|")

  print("|", end="")
  for c in color._colors:
    print(color[c].White(f'{c:^7}'), end="")
  print("|     |", end="")
  for c in color._colors:
    print(color[c].White.bold(f'{c:^7}'), end="")
  print("|     |", end="")
  for c in color._colors:
    print(color.black[c.upper()](" . "), end="")
  print("|")

  print(f'+{"--bold":-<56}+     +{"--regular":-<56}+     +{"--background":-<24}+')
  print()
  print()


  print(f'{"Gray colors":^152}')
  gray = "-" + "-".join([str(i) for i in range(1, 10)]) + "--" + "--".join([str(i) for i in range(11, 25, 2)])
  print(f'+{gray}--+ +{gray}--+ +{gray}--+')
  print("|", end="")
  for i in range(1, 25):
    print(color.gray(i)("##"), end="")
  print(f'| |', end="")
  for i in range(1, 25):
    print(color.gray(i).bold("##"), end="")
  print(f'| |', end="")
  for i in range(1, 25):
    print(color.white.Gray(i)("  "), end="")
  print("|")

  gray = "--".join([f'{i}' for i in range(10, 25, 2)])
  print(f'+--bold{"-" * 12}{gray}+ +--regular{"-" * 9}{gray}+ +--background{"-" * 6}{gray}+')
  print()
  print()


  print(f'{"RGB colors":^152}')
  print("GB012345+", end="")
  for r in range(1, 6):
    print(f'-R{r}----+', end="")
  print("  +", end="")
  for r in range(6):
    print("-------+", end="")
  print("  +", end="")
  for r in range(6):
    print("-------+", end="")
  print()

  for g in range(6):
    print(f'{g}', end="")
    for r in range(6):
      print(" ", end="")
      for b in range(6):
        print(color.rgb(r, g, b)("#"), end="")
      print("|", end="")
    print("  ", end="")
    for r in range(6):
      print("| ", end="")
      for b in range(6):
        print(color.rgb(r, g, b).bold("#"), end="")
    print("|  ", end="")
    for r in range(6):
      print("| ", end="")
      for b in range(6):
        print(color.Rgb(r, g, b)(" "), end="")
    print("|")

  print(f'+--bold-+', end="")
  for r in range(1, 6):
    print("-------+", end="")
  print(f'  +--regular------+', end="")
  for r in range(2, 6):
    print("-------+", end="")
  print(f'  +--background---+', end="")
  for r in range(2, 6):
    print("-------+", end="")
  print()
  print()


if __name__ == "__main__":
  main()
