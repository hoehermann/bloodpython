# coding=utf-8

import BPpings,BPcore
import sys,math

class BPshooter:

  def __init__(self,core):
    self.core = core
    self.maxRotate = 0
    self.minShootEnergy = 0
    self.reset()

  def reset(self):
    self.shotwait = 0
    self.rotateIssued = False

  def setTarget(self,angle):
    pass

  def setMinShootEnergy(self,minShootEnergy):
    self.minShootEnergy = minShootEnergy

  def setMaxRotate(self,maxRotate):
    self.maxRotate = maxRotate

  def rotationReached(self,what):
    if what != 4 and what >= 2:
      self.rotateIssued = False
  
  def act(self):
    if self.core.radar.lastEnemyAngle != None:
      targetAngle = (math.pi*2 + 
                     self.core.radar.lastEnemyAngle + 
                     self.core.radar.lastEnemySpeed)%(math.pi*2)
      if not self.rotateIssued:
        self.core.communicator.send("RotateTo 2 %f %f"%(self.maxRotate,targetAngle))
        self.rotateIssued = True

        self.shotwait = self.shotwait + 1
        if self.shotwait >= self.core.radar.lastEnemyDistance:
          self.shotwait = 0
          self.core.communicator.send("Shoot %f"%(self.minShootEnergy))
