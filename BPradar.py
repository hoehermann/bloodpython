# coding=utf-8

import BPpings,BPcore
import sys,math

# Distanz (basierend auf standardpanzergröße und square arena)
# 10 ist mittelmaß
# 3 ist sehr nah
# 15 ist "unendlich" weit weg
CLOSE = 10
SWEEPAMOUNT = math.pi/2

SEARCHING = 0
FOUND = 1
LOCKED = 2
SCANREV = 3
SCANFWD = 4

class BPradar:

  def __init__(self,core):
    self.core = core
    self.maxRotate = 0
    self.reset()

  def reset(self):
    self.state = SEARCHING
    self.lastEnemyAngle = None
    self.lastEnemySpeed = 0
    self.lastEnemyDistance = 10
    self.rotateIssued = False
    self.enemySeen = False
    self.sweepmodifier = 1

  def setMaxRotate(self,maxRotate):
    self.maxRotate = maxRotate

  def rotationReached(self,what):
    if what >= 4:
      self.rotateIssued = False
  
  def act(self):
    if self.state == SEARCHING:
      self.core.communicator.send("Rotate 4 %f"%self.maxRotate)
    
    elif not self.rotateIssued:
      if self.state == LOCKED:
        #self.core.communicator.say("radar: locked")
        self.core.communicator.send("RotateAmount 4 %f %f"%(self.maxRotate,SWEEPAMOUNT/2*self.sweepmodifier))
        self.rotateIssued = True
        self.state = SCANREV
      elif self.state == SCANREV:
        #self.core.communicator.say("radar: scanrev")
        self.core.communicator.send("RotateAmount 4 %f %f"%(self.maxRotate,-SWEEPAMOUNT*self.sweepmodifier))
        self.rotateIssued = True
        self.state = SCANFWD
      elif self.state == SCANFWD:
        if not self.enemySeen and not self.rotateIssued:
          #self.core.communicator.say("radar: target lost")
          self.lastEnemyAngle = None
          self.lastEnemySpeed = 0
          self.state = SEARCHING
        else:
          #self.core.communicator.say("radar: scanfwd")
          self.core.communicator.send("RotateAmount 4 %f %f"%(self.maxRotate,SWEEPAMOUNT/2*self.sweepmodifier))
          self.rotateIssued = True
          self.state = FOUND
      elif self.state == FOUND:
        #self.sweepmodifier = CLOSE / self.core.radar.lastEnemyDistance
        #self.core.communicator.say("radar: swpmod %f"%self.sweepmodifier)
        #if self.sweepmodifier > 2:
        #  self.sweepmodifier = 2
        #futureEnemyAngle = (math.pi*2 + self.lastEnemyAngle + self.lastEnemySpeed)%(math.pi*2)
        futureEnemyAngle = self.lastEnemyAngle
        #self.core.communicator.say("radar: relocking to %f"%futureEnemyAngle)
        self.core.communicator.send("RotateTo 4 %f %f"%(self.maxRotate,futureEnemyAngle))
        self.rotateIssued = True
        self.state = LOCKED
        self.enemySeen = False

  def processInput(self, distance, kind, angle):
    angle = angle%(math.pi*2)
    if kind == 0:
      self.enemySeen = True
      #self.core.communicator.say("radar: enemy at %f"%angle)
      if self.lastEnemyAngle == None:
        #self.core.communicator.say("radar: new enemy")
        self.lastEnemyAngle = angle
        self.futureEnemyAngle = angle
      else:
        if self.state == SCANFWD:
          self.lastEnemySpeed = angle - self.lastEnemyAngle
          #self.core.communicator.say("radar: new speed %f"%self.lastEnemySpeed)
        self.lastEnemyAngle = angle
      self.lastEnemyDistance = distance

      if self.state == SEARCHING:
        self.core.communicator.send("RotateTo 6 %f %f"%(self.maxRotate,angle))
        self.state = LOCKED

    elif kind == 3:
      self.core.getCookie(angle)
    elif kind == 5:
      self.core.communicator.say("radar: got 'same kind'")

