#! /usr/bin/env python

import sys,math

def hypothenuse(side1, side2):
  """
  The algorithm the man behind the door
  uses is the same used to compute the
  hypothenuse for a triangle with catheti
  x and y :)
  """
  hyp = math.sqrt(side1 * side1 + side2 * side2)
  return round(hyp, 2)

line = sys.stdin.readline()
num_cases = int(line)

for i in range(num_cases):
  line = sys.stdin.readline()
  nums = [int(x) for x in line.split()]
  result = hypothenuse(nums[0], nums[1])
  if int(result) == result:
    print(int(result))
  else:
    print("{0:.2f}".format(result))
