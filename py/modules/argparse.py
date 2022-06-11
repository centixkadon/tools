
import argparse
import logging

from py.utility import color, log



def func(*args, x, y, **kwargs):
  logging.info(f"args {args}")
  logging.info(f"kwargs {kwargs}")
  logging.info(x)
  logging.info(y)



def main():
  log.addLevelNames()

  parser = argparse.ArgumentParser(description=color.red("Python module argparse description."), epilog=color.green("Python module argparse epilog."), add_help=False)
  parser.add_argument("-h", "--help", help="show this help message and exit", action="help")
  parser.add_argument("-V", "--version", action="version", version="%(prog)s 0.1")
  parser.add_argument("-v", "--verbose", help=f"set log level to {logging.getLevelName(20)} or {logging.getLevelName(10)} (default {logging.getLevelName(30)})", action="count", default=0)
  parser.add_argument("-q", "--quiet", help=f"set log level to {logging.getLevelName(40)} or {logging.getLevelName(50)} (default {logging.getLevelName(30)})", action="count", default=0)

  parser.add_argument("-t", "--text", help="text")
  parser.add_argument("-b", "--bool", help="true", action="store_true")

  parser.add_argument("x", help="this is x")
  parser.add_argument("y", help="this is y")

  args = parser.parse_args()
  args.level = max(0, logging.WARN - (args.verbose - args.quiet) * 10)
  log.basicConfig(level=args.level)
  logging.info(f"set log level to {logging.getLevelName(args.level)}")
  logging.info(args)

  func(**vars(args))

if __name__ == "__main__":
  main()
