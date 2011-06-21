# coding=utf-8

import BPcore
import sys,math

class BPnavigator:

  def __init__(self,core):
    self.core = core
    self.maxRotate = 0
    self.rotationIssued = False
    self.targetAngle = 0
    self.maxAccel = 1.0

  def processCollision(self,kind,angle):
    if kind != 1:
      self.core.setState(BPcore.IDLE)

  def setMaxAccel(self,maxAccel):
    self.maxAccel = maxAccel

  def setMaxRotate(self,maxRotate):
    self.maxRotate = maxRotate

  def rotationReached(self,what):
    if what == 1:
      self.core.setState(BPcore.MOVING)

  def moveInDirection(self,angle):
    angle = angle%(math.pi*2)
    if angle > math.pi:
      angle = angle - math.pi*2
    self.targetAngle = angle
    self.rotationIssued = False
    self.core.setState(BPcore.TURNING)
    
  def act(self):
    if self.core.state == BPcore.IDLE:
      self.core.communicator.send("Brake 1")
      self.core.communicator.send("Accelerate 0")
      self.core.communicator.send("Rotate 1 0")
    elif self.core.state == BPcore.TURNING:
      self.core.communicator.send("Brake 0")
      self.core.communicator.send("Accelerate 0")
      if not self.rotationIssued:
        self.rotationIssued = True
        self.core.communicator.send("RotateAmount 1 %f %f"%(self.maxRotate,self.targetAngle))
    elif self.core.state == BPcore.MOVING:
      self.core.communicator.send("Brake 0")
      self.core.communicator.send("Accelerate %f"%self.maxAccel)
      self.core.communicator.send("Rotate 1 0")

