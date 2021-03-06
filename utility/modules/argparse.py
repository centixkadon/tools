#!/usr/bin/env python3

import os
import shutil

import argparse

from utility.color import color

os.environ.update(zip(("COLUMNS", "LINES"), (str(x) for x in shutil.get_terminal_size())))

def add():
  print("add")

def mul():
  print("mul")

def main():
  parser = argparse.ArgumentParser(description=color.red("Python module argparse test description."), epilog=color.green("Python module argparse test epilog."))
  parser.add_argument("-V", "--version", help="Version", action="version", version="%(prog)s 0.1")
  parser.add_argument("-v", "--verbose", help="Verbose", action="count", default=0)

  parser.add_argument("--foo", help="Test int", type=int, default=42)

  parser.add_argument("--cpu", help="Use cpu", action="store_const", dest="device", const=1)
  parser.add_argument("--gpu", help="Use gpu", action="store_const", dest="device", const=2)

  parser.add_argument("--number", help="Numbers to calculate", action="append", dest="numbers", type=int, choices=range(3, 6), metavar="NUMBERS")

  parser.add_argument("--one", help="Number 1 to calculate", action="append_const", dest="numbers", const=1)
  parser.add_argument("--two", help="Number 2 to calculate", action="append_const", dest="numbers", const=2)

  group = parser.add_mutually_exclusive_group()
  group.add_argument("-t", "--true", help="True", action="store_true")
  group.add_argument("-f", "--false", help="False", action="store_false")

  subparsers = parser.add_subparsers(title="commands", description="description", help="help", metavar="COMMAND")
  parserAdd = subparsers.add_parser("add", help="Add x and y")
  parserAdd.add_argument("x", type=int, help="Add x")
  parserAdd.add_argument("y", type=int, help="Add y")
  parserAdd.set_defaults(func=add)

  parserMul = subparsers.add_parser("mul", help="Multiply x and y")
  parserMul.add_argument("x", type=int, help="Multiply x")
  parserMul.add_argument("y", type=int, help="Multiply y")
  parserAdd.set_defaults(func=mul)

  args = parser.parse_args()
  print(args)

if __name__ == "__main__":
  main()
