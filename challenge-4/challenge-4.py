#! /usr/bin/env python

import sys

class DNAState:
  string = ""

  def __init__(self, line):
    self.string = line[:-1]

  def __sub__(self, other):
    """
    The difference between 2 DNA states is
    defined as the number of different letters
    in the same position between them.
    """
    counter = 0
    for i in range(len(self.string)):
      if self.string[i] != other.string[i]:
        counter = counter + 1
    return counter

  def canAccess(self, other):
    """
    Another DNA state is accessible if we
    only need to change 1 letter.
    """
    if self - other == 1:
      return True
    return False

  def __eq__(self, other):
    return self.string == other.string

class DNASolver:
  """
  DNASolver solves the problem by running a backtracking
  algorithm after obtaining all the data available. The
  backtracking scheme is OK to solve this problem, although
  maybe there are better algorithms for it.

  The good thing about running backtracking is that you have the
  list of permitted states, and that makes it more efficient because
  you only need to make recursive calls to the accessible states
  in the permitted list, thus reducing a lot the branching factor of
  the backtracking tree.
  """
  initial_state = 0
  final_state = 0
  permitted = []
  min_path = 9999
  global_solution = []
  def __init__(self, state1, state2):
    self.initial_state = state1
    self.final_state = state2

  def readPermittedStates(self):
    line = sys.stdin.readline()
    while line:
      new_state = DNAState(line)
      self.permitted.append(new_state)
      line = sys.stdin.readline()

  def backtrack(self, cur_state, steps, possible_states, solution):
    # if DNA state is final, save min steps and solution if proceeds
    if (cur_state - self.final_state == 0):
      if self.min_path > steps:
        self.min_path = steps
        self.global_solution = solution
      return
    prev_state = cur_state
    for st in possible_states:
      if st.canAccess(cur_state):
        # replicate objects and modify them
        new_possible = possible_states
        new_possible.remove(st)
        new_solution = solution
        new_solution.append(st)
        # assign values
        cur_state = st
        steps = steps + 1
        self.backtrack(cur_state, steps, new_possible, solution)
        # restore values for next iteration
        steps = steps - 1
        cur_state = prev_state
      
  def solve(self):
    self.permitted.remove(initial_state)
    # Initial call for backtracking
    self.backtrack(self.initial_state, 0, self.permitted, [self.initial_state])
    return self.global_solution

line = sys.stdin.readline()
initial_state = DNAState(line)
line = sys.stdin.readline()
final_state = DNAState(line)
solver = DNASolver(initial_state, final_state)
solver.readPermittedStates()
solution = solver.solve()
solution_string = [x.string for x in solution]
print("->".join(solution_string))
