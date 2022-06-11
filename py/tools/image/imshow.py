
import sys

import bisect

import cv2

from py.utility import color

def main():
  print(color.Rgb(0, 0, 0).rgb(5, 5, 5)("⠁⠂⠄⠈⠐⠠⡀⢀⣿"))
  return

  if len(sys.argv) > 2:
    _, image_filename, mask_filename, *_ = sys.argv
    print("image", image_filename)
    print("mask", mask_filename)

    mask = cv2.imread(mask_filename, cv2.IMREAD_GRAYSCALE)
    return

    img = cv2.imread(image_filename)
    height, width, *_ = img.shape

    w = 10
    factor = 9 * w / width
    img = cv2.resize(img, None, None, factor, factor)
    height, width, *_ = img.shape

    c = ["00", "5f", "87", "af", "d7", "ff"]
    c = [int(x, 16) for x in c]
    c = [(i + j) / 2 for i, j in zip(c, c[1:] + [c[-1] + 1])]
    for i in range(0, height - 19, 19):
      for j in range(0, width, 9):
        b, g, r, *_ = cv2.sumElems(img[i:i+19, j:j+9] / (19 * 9))
        r = bisect.bisect_left(c, r)
        g = bisect.bisect_left(c, g)
        b = bisect.bisect_left(c, b)
        print(color.Rgb(r, g, b)(" "), end="")
      print()

    print(height, width)

if __name__ == "__main__":
  main()
