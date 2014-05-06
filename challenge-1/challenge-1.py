#! /usr/bin/env python

import sys

class Student:
  name = ""
  gender = ""
  age = 0
  studies = ""
  academic_year = 0
  def __init__(self, line):
    fields = [x for x in line.split(',')]
    if len(fields) > 4 :
      self.name = fields[0]
      self.gender = fields[1]
      self.age = int(fields[2])
      self.studies = fields[3]
      self.academic_year = int(fields[4])
    else:
      self.gender = fields[0]
      self.age = int(fields[1])
      self.studies = fields[2]
      self.academic_year = int(fields[3])

  def __eq__(self, other):
    if self.gender == other.gender and \
       self.age == other.age and \
       self.studies == other.studies and \
       self.academic_year == other.academic_year:
      return True
    return False

class StudentManager:
  student_list = []

  def addStudent(self, student):
    self.student_list.append(student)

  def loadStudents(self, filename):
    student_file = open(filename, 'r')
    student_lines = student_file.readlines()
    for line in student_lines:
      self.addStudent(Student(line))
    student_file.close()

  def getMatches(self, student):
    matches_list = []
    for st in self.student_list:
      if st == student:
        matches_list.append(st)
    matches_list = sorted([x.name for x in matches_list])
    return matches_list

manager = StudentManager()
manager.loadStudents("students")

num_cases = int(sys.stdin.readline())

for i in range(num_cases):
  line = sys.stdin.readline()
  new_student = Student(line)
  matches = manager.getMatches(new_student)
  case_string = "Case #{0}: ".format(i + 1)
  if len(matches) > 0 :
    print case_string + ",".join(matches)
  else:
    print case_string + "NONE"
