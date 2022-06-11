
import logging

from py.utility import log

from py.utility import color
from py.utility import loggers

def f(func):
  def ff(*args, **kwargs):
    print("ff", args, kwargs)
    return func(*args, kwargs=kwargs, **kwargs)
  return ff

class test:
  @f
  def __init__(self, *, kwargs, **_):
    print("__init__", kwargs)
    self.run(**kwargs)

    self.run2(kwargs=kwargs)

  @f
  def run(self, *, a, kwargs, **_):
    print("run", kwargs, a)

  def run2(self, kwargs, **_):
    print("run2", kwargs)

  @property
  def a(self):
    return 1

def main():
  # log.addLevelNames()
  # log.basicConfig(level=logging.NOTSET)

  # logging.debug("Debug")
  # logging.info("Info")
  # logging.warning("Warning")
  # logging.error("Error", exc_info=RuntimeError("hhh"))
  # logging.critical("Critical")

  # print(__name__)
  # logger = logging.getLogger(__name__)
  # logger.setLevel(logging.DEBUG)
  # handler = logging.StreamHandler()
  # logger.addHandler(handler)
  # fmt = "[{asctime}.{msecs_int:03}][{levelname:>{levelname_len}}][{filename:36.36}{lineno:>4}]: {msg}"
  # datefmt = "%Y-%m-%d %H:%M:%S"
  # style = "{"
  # handler.setFormatter(logging.Formatter(fmt, datefmt, style))

  kwargs = {
    "a": 1,
  }
  test(**kwargs)



def func(*args, a, **kwargs):
  print("func", kwargs)

if __name__ == "__main__":
  func(1, a="1")
  main()

  loggers.config([__name__, "py", "root"])
  logger = loggers.get(__name__)
  logger.info("name1before")
  logger.setLevel(logging.INFO)
  logger.info("name1")

  loggers.main()

  try:
    def func2():
      raise RuntimeError("hhh")
    func2()
  except RuntimeError as e:
    logging.warning("name3", exc_info=e)
