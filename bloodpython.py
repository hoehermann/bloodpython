#!/usr/bin/python2
# coding=utf-8

import BPcore
import sys, os, time

sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0) 
core = BPcore.BPcore()
print "RobotOption 3 0"
print "RobotOption 1 1"
while True:
  try:
    message = sys.stdin.readline()
    if not message:
      print >> sys.stderr, 'input closed'
      break
    core.communicator.processServerMessage(message)
  except IOError as (errno, strerror):
    if errno == 11:
      pass
    else:
      print >> sys.stderr, "I/O error({0}): {1}".format(errno, strerror)
      sys.exit(4)

  

