
import shutil

from py.utility import *

def main():
  shutil.rmtree("test/file", ignore_errors=True)

  a = file.read("test/file/a")
  print(f"read a {a!r}")

  file.write("test b\ntest 中文 b", "test/file/b", newline="\r\n")
  b = file.read("test/file/b")
  print(f"write b {b!r}")

  file.write(["test c", "test 中文 c"], "test/file/c")
  c = file.read("test/file/c")
  print(f"write c {c!r}")



if __name__ == "__main__":
  main()
