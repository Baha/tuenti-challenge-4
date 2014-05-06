#! /usr/bin/env python

import sys

class Generation:
  matrix = []
  max_x = 7
  max_y = 7
  def __init__(self, lines=None):
    if lines == None:
      self.matrix = [['-' for j in range(8)] for i in range(8)]
    else:
      self.matrix = [[x for x in line] for line in lines]

  def isAlive(self,x,y):
    if x >= 0 and y >= 0 and x <= self.max_x and y <= self.max_y:
      return self.matrix[x][y] == 'X'
    return False
  
  def isDead(self, x, y):
    return not isAlive(x, y)

  def aliveNeighbors(self, x, y):
    count = 0
    count = count + self.isAlive(x-1, y-1)
    count = count + self.isAlive(x, y-1)
    count = count + self.isAlive(x+1, y-1)
    count = count + self.isAlive(x-1, y)
    count = count + self.isAlive(x+1, y)
    count = count + self.isAlive(x-1, y+1)
    count = count + self.isAlive(x, y+1)
    count = count + self.isAlive(x+1, y+1)
    return count

  def nextGen(self):
    """
    This is the algorithm used to create the
    next generation. You can read the details at:
    http://en.wikipedia.org/wiki/Conway's_Game_of_Life
    """
    next_gen = Generation()

    for x in range(8):
      for y in range(8):
        n = self.aliveNeighbors(x,y)
        #print x, y, n
        if n < 2 or n > 3:
          next_gen.matrix[x][y] = '-'
        if n == 3 and self.matrix[x][y] == '-':
          next_gen.matrix[x][y] = 'X'
        if (n == 2 or n == 3) and self.matrix[x][y] == 'X':
          next_gen.matrix[x][y] = 'X'
    return next_gen

  def __str__(self):
    return ''.join([''.join(x) + '\n' for x in self.matrix])

  def __eq__(self, other):
    return self.matrix == other.matrix

lines = sys.stdin.readlines()
lines = [x[:-1] for x in lines]
# Generation 0
cur_gen = Generation(lines)
gen_list = []
gen_list.append(cur_gen)
# Create next generations
for i in range(1,100):
  # print(cur_gen)
  cur_gen = cur_gen.nextGen()
  gen_list.append(cur_gen)

# Check the first generation equal to a previous generation
for i in range(100):
  for j in range(i+1, 100):
    if gen_list[i] == gen_list[j]:
      print i, (j - i)
      sys.exit(0)
sys.stdout.write(str(gen))
