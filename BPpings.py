# coding=utf-8

import BPradar
import sys

class BPpings:

  def __init__(self):
    self.pings = {}

  def inList(self,ping):
    for e in self.pings:
      if abs(e-ping) < BPradar.EPSILON:
        return e
    return None

  def age(self,age):
    pings = {}
    for e in self.pings:
      self.pings[e] = (self.pings[e][0], self.pings[e][1]-age)
      if self.pings[e][1] > 0 :
        pings[e] = self.pings[e]
      else:
        pass
    self.pings = pings

  def add(self,angle,distance,age):
    self.pings[angle] = (distance,age)

  def refresh(self,old,new,distance,age):
    del self.pings[old]
    self.pings[new] = (distance,age)

  def getClosest(self):
    closest = None
    distance = 0
    for e in self.pings:
      if closest == None or distance > self.pings[e][0]:
        closest = e
        distance = self.pings[e][0]
    return closest
