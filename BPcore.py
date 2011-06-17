# coding=utf-8

import BPcommunicator, BPnavigator, BPradar, BPshooter
import sys

IDLE = 0
AIMING = 1
SHOOTING = 2
TURNING = 3
MOVING = 4

class BPcore:

  def __init__(self):
    self.navigator = BPnavigator.BPnavigator(self)
    self.radar = BPradar.BPradar(self)
    self.communicator = BPcommunicator.BPcommunicator(self)
    self.shooter = BPshooter.BPshooter(self)
    self.reset()
    self.maxEnergy = 0
    self.name = "bloodpython"
    self.color1 = "0x44FF44"
    self.color2 = "0x009900"

  def reset(self):
    self.energy = 1
    self.dead = False
    self.state = IDLE
    self.radar.reset()
    self.shooter.reset()

  def act(self):
    if self.state <= SHOOTING:
      self.radar.act()
      self.shooter.act()
    self.navigator.act()

  def setState(self,state):
    self.state = state
#    if state > SHOOTING:
#      self.radar.reset()
#      self.shooter.reset()
    pass

  def initialize(self,sequence):
    self.communicator.sendName(self.name)
    self.communicator.sendColor(self.color1,self.color2)

  def getCookie(self,angle):
    self.communicator.say("cookie at %f!"%angle)
    self.navigator.moveInDirection(angle)
    pass

  def setName(self,name):
    self.name = name

  def setColor(self,color):
    self.color = color

  def processGameOption(self,option,value):
    o = int(option)
    if o == 0:
      self.navigator.setMaxRotate(float(value))
    if o == 1:
      self.shooter.setMaxRotate(float(value))
    elif o == 2:
      self.radar.setMaxRotate(float(value))
    elif o == 3:
      self.navigator.setMaxAccel(float(value))
    elif o == 5:
      self.maxEnergy = float(value)
    elif o == 9:
      self.shooter.setMinShootEnergy(float(value))
    pass

  def setEnergy(self,energy):
    self.energy = energy

  def processCollision(self,kind,angle):
    #if self.energy < self.maxEnergy/2:
    #  self.communicator.say("ouch")
    #  self.getCookie()
    pass

  def processInfo(self,a,b,c):
    pass

  def processWarning(self,a,b):
    pass

  def retire(self):
    self.dead = True

  def die(self):
    self.dead = True
    self.communicator.say("died gloriously")

  def exit(self):
    self.communicator.say("was told to exit")
    sys.exit(0)
