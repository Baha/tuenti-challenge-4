#! /usr/bin/env python

import sys

LEFT       = 0
RIGHT      = 1
UP         = 2
DOWN       = 3
HORIZONTAL = 0
VERTICAL   = 1

class SymbolManager:
  """
  This class serves as a token
  producer of symbols for CircuitBuilder.
  """
  symbol_list = []

  def __init__(self, line):
    self.symbol_list = line[:-1]

  def generate(self):
    for sym in self.symbol_list:
      yield sym

class CircuitBuilder:
  direction   = RIGHT
  orientation = HORIZONTAL
  cur_x = -1
  cur_y = 0
  max_right = -9999
  max_left = 9999
  max_up = -9999
  max_down = 9999
  symbols = []

  def __init__(self, gen):
    self.symbols = gen

  def computeBounds(self):
    """
    This first function computes the bounding box
    of the track. This way it is easier to deal
    with parts of the track to go to the left or
    up the starting point.
    """
    for sym in self.symbols.generate():
      if self.orientation == HORIZONTAL:
        if self.direction == RIGHT:
          self.cur_x = self.cur_x + 1
        else:
          self.cur_x = self.cur_x - 1
      else:
        if self.direction == UP:
          self.cur_y = self.cur_y + 1
        else:
          self.cur_y = self.cur_y - 1
      self.max_right = max(self.max_right, self.cur_x)
      self.max_left  = min(self.max_left, self.cur_x)
      self.max_up    = max(self.max_up, self.cur_y)
      self.max_down  = min(self.max_down, self.cur_y)

      if sym == '/':
        if self.orientation == HORIZONTAL:
          self.orientation = VERTICAL
          if self.direction == RIGHT:
            self.direction = UP
          else:
            self.direction = DOWN
        else:
          self.orientation = HORIZONTAL
          if self.direction == UP:
            self.direction = RIGHT
          else:
            self.direction = LEFT
          
      if sym == '\\':
        if self.orientation == HORIZONTAL:
          self.orientation = VERTICAL
          if self.direction == RIGHT:
            self.direction = DOWN
          else:
            self.direction = UP
        else:
          self.orientation = HORIZONTAL
          if self.direction == UP:
            self.direction = LEFT
          else:
            self.direction = RIGHT

  def asciiRepr(self):
    """
    This second method returns the final result.
    It creates a matrix of spaces (with the minimum
    length required) and makes a second pass, correctly
    setting the symbols on the list.
    """
    self.direction = RIGHT
    self.orientation = HORIZONTAL
    width = self.max_right - self.max_left + 1
    height = self.max_up - self.max_down + 1
    x = -self.max_left - 1
    y = self.max_up
    matrix = [([' ' for j in range(width)] + ['\n']) for i in range(height)]
    for sym in self.symbols.generate():
      if self.orientation == HORIZONTAL:
        if self.direction == RIGHT:
          x = x + 1
        else:
          x = x - 1
      else:
        if self.direction == UP:
          y = y - 1
        else:
          y = y + 1

      if sym == '-' and self.orientation == VERTICAL:
        matrix[y][x] = '|'
      else:
        matrix[y][x] = sym

      if sym == '/':
        if self.orientation == HORIZONTAL:
          self.orientation = VERTICAL
          if self.direction == RIGHT:
            self.direction = UP
          else:
            self.direction = DOWN
        else:
          self.orientation = HORIZONTAL
          if self.direction == UP:
            self.direction = RIGHT
          else:
            self.direction = LEFT
          
      if sym == '\\':
        if self.orientation == HORIZONTAL:
          self.orientation = VERTICAL
          if self.direction == RIGHT:
            self.direction = DOWN
          else:
            self.direction = UP
        else:
          self.orientation = HORIZONTAL
          if self.direction == UP:
            self.direction = LEFT
          else:
            self.direction = RIGHT
    return matrix

line = sys.stdin.readline()
manager = SymbolManager(line)
circuit = CircuitBuilder(manager)
circuit.computeBounds()
ascii_matrix = circuit.asciiRepr()
sys.stdout.write(''.join([''.join(x) for x in ascii_matrix]))
