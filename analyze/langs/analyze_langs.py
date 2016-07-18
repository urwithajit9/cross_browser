#!/usr/bin/env python

from PIL import Image, ImageChops
import os
from sets import Set
import pdb, traceback, sys

def main():
  img_root = '.'
  uids = Set()
  for f in os.listdir(img_root):
    if f.find("lang.png") != -1:
      num = int(f.split("_")[0])
      uids.add(num)


  for uid in uids:
    analyzer = LangAnalyzer(img_root, uid)
    print analyzer.anaylze()
    return

def isBoxes(img):
  xCountDict = {}
  cols, rows = img.size
  pixels = img.load()
  for j in range(rows):
    xCount = 0
    for i in range(cols):
      if pixels[i, j] is 1:
        xCount += 1

    if not xCountDict.has_key(xCount):
      xCountDict.update({xCount: 1})

  numXCounts = len(xCountDict)

  yCountDict = {}
  for i in range(cols):
    yCount = 0
    for j in range(rows):
      if pixels[i, j] is 1:
        yCount += 1

    if not yCountDict.has_key(yCount):
      yCountDict.update({yCount: 1})

  numYCounts = len(yCountDict)

  return numXCounts <=5 and numYCounts <= 5

class LangAnalyzer:
  def __init__(self, img_root, uid):
    self.img_root = img_root
    self.uid = uid

  def anaylze(self):
    results = Set()
    for index in range(36):
      img = Image.open("{}/{}_{}_lang.png".format(self.img_root, self.uid, index))
      binary = Image.new('1', img.size)
      bPix = binary.load()
      pix = img.load()
      cols, rows = img.size
      for j in range(rows):
        for i in range(cols):
          R, G, B = pix[i, j]
          L = R * 299/1000.0 + G * 587/1000.0 + B * 114/1000.0
          if L < 255/2.0:
            bPix[i, j] = 1
          else:
            bPix[i, j] = 0

      if isBoxes(binary):
        results.add(index)

    return results

if __name__ == '__main__':
  main()