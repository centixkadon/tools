
from py.utility import color

def main():
  print(f'{"System colors":^152}')
  print(f'+{"":-<56}+ +{"":-<56}+ +{"":-<24}+')
  print("|", end="")
  for c in color._foreground_colors:
    print(color[c](f'{c:^7}'), end="")
  print("| |", end="")
  for c in color._foreground_colors:
    print(color[c].bold(f'{c:^7}'), end="")
  print("| |", end="")
  for c in color._background_colors:
    print(color[c](" . "), end="")
  print("|")

  print("|", end="")
  for c in color._foreground_colors:
    print(color[c].bg_white(f'{c:^7}'), end="")
  print("| |", end="")
  for c in color._foreground_colors:
    print(color[c].bg_white.bold(f'{c:^7}'), end="")
  print("| |", end="")
  for c in color._background_colors:
    print(color.black[c](" . "), end="")
  print("|")

  print(f'+{"--bold":-<56}+ +{"--regular":-<56}+ +{"--background":-<24}+')
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
    print(color.white.bg_gray(i)("  "), end="")
  print("|")

  gray = "--".join([f'{i}' for i in range(10, 25, 2)])
  print(f'+--bold{"-" * 12}{gray}+ +--regular{"-" * 9}{gray}+ +--background{"-" * 6}{gray}+')
  print()
  print()


  print(f'{"RGB colors":^152}')
  print("GB012345+", end="")
  for r in range(1, 6):
    print(f'-R{r}----+', end="")
  for _ in range(2):
    print(" +" + "-------+" * 6, end="")
  print()

  for g in range(6):
    print(f'{g}', end="")
    for r in range(6):
      print(" ", end="")
      for b in range(6):
        print(color.rgb(r, g, b)("#"), end="")
      print("|", end="")
    print(" ", end="")
    for r in range(6):
      print("| ", end="")
      for b in range(6):
        print(color.rgb(r, g, b).bold("#"), end="")
    print("| ", end="")
    for r in range(6):
      print("| ", end="")
      for b in range(6):
        print(color.bg_rgb(r, g, b)(" "), end="")
    print("|")

  for i in ["+--bold-+-------+", " +--regular------+", " +--background---+"]:
    print(i + "-------+" * 4, end="")
  print()
  print()

if __name__ == "__main__":
  main()
