#! /usr/bin/env python

import sys

class GraphDict:
  edges = {}
  visited = {}

  def __init__(self, graph=None):
    if graph:
      self.edges = dict(graph.edges)

  def addEdge(self, vert1, vert2):
    if vert1 in self.edges:
      self.edges[vert1].append(vert2)
    else:
      self.edges[vert1] = [vert2]
  
  def clearVisited(self):
    for vert in self.edges:
      self.visited[vert] = False

  def relatedVerts(self, vert1, vert2):
    if not vert1 in self.edges or not vert2 in self.edges:
      return False
    self.clearVisited()
    queue = [vert1]
    self.visited[vert1] = True

    while len(queue) > 0:
      cur_vert = queue[0]
      queue.remove(cur_vert)
      if cur_vert == vert2:
        return True

      for vert in self.edges[cur_vert]:
        if not self.visited[vert]:
          queue.append(vert)
          self.visited[vert] = True
    return False

terro_A = int(sys.stdin.readline())
terro_B = int(sys.stdin.readline())

graph = GraphDict()
i = 0

call_list = []
calls_file = open("phone_call.log");
calls_line = calls_file.readline()
while calls_line:
  calls = [int(x) for x in calls_line.split()]
  call_list.append([calls[0], calls[1]])
  calls_line = calls_file.readline()

while i < 1000000:
  prev_graph = GraphDict(graph)
  for j in range(10000):
    calls[0], calls[1] = call_list[i + j]
    graph.addEdge(calls[0], calls[1])
    graph.addEdge(calls[1], calls[0])
  if graph.relatedVerts(terro_A, terro_B):
    for j in range(10000):
      calls[0], calls[1] = call_list[i + j]
      prev_graph.addEdge(calls[0], calls[1])
      prev_graph.addEdge(calls[1], calls[0])
      if prev_graph.relatedVerts(terro_A, terro_B):
        print("Connected at {0}".format(i + j))
        sys.exit(0)
  else:
    i = i + 10000
print("Not connected")
