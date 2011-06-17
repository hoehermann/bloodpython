# coding=utf-8

import BPcore
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
      if self.core.radar.previousEnemySpeed != None:
        changerate = self.core.radar.previousEnemySpeed - self.core.radar.lastEnemySpeed
        changerate = abs(changerate)
      else:
        changerate = 1
      speed = self.core.radar.lastEnemySpeed
      targetAngle = (math.pi*2 + 
                     self.core.radar.lastEnemyAngle + 
                     speed)%(math.pi*2)
      if not self.rotateIssued:
        #self.core.communicator.say("aiming...")
        self.core.communicator.send("RotateTo 2 %f %f"%(self.maxRotate,targetAngle))
        self.rotateIssued = True

        self.shotwait = self.shotwait + 1
        if self.shotwait >= self.core.radar.lastEnemyDistance:
          self.shotwait = 0
          shotmodifier = 1/(math.pow(changerate*10,2)+0.25)+1
          self.core.communicator.send("Shoot %f"%(self.minShootEnergy))
