# coding=utf-8

import BPcore
import sys

class BPcommunicator:
  def __init__(self,core):
    self.core = core
    self.f = open("servermessages.log",'w')

  def processServerMessage(self,message):
    self.f.write(message)
    #print >> sys.stderr, 'recieved message from server: %s'%(message)
    parts = message.split()
    if parts[0] == "Initialize":
      self.core.initialize(int(parts[1]))
    elif parts[0] == "YourName":
      self.core.setName(parts[1])
    elif parts[0] == "YourColour":
      self.core.setColor(parts[1])
    elif parts[0] == "GameOption":
      self.core.processGameOption(parts[1],parts[2])
    elif parts[0] == "GameStarts":
      self.core.reset()
    elif parts[0] == "Radar":
      if self.core.state <= BPcore.SHOOTING:
        self.core.radar.processInput(float(parts[1]),int(parts[2]),float(parts[3]))
    elif parts[0] == "Info":
      self.core.processInfo(parts[1],parts[2],parts[3])
    elif parts[0] == "Coordinates":
      #self.core.navigator.setCoordinates(float(parts[1]),float(parts[2]),float(parts[3]))
      pass
    elif parts[0] == "RobotInfo":
      pass
    elif parts[0] == "RotationReached":
      self.core.navigator.rotationReached(int(parts[1]))
      self.core.radar.rotationReached(int(parts[1]))
      self.core.shooter.rotationReached(int(parts[1]))
    elif parts[0] == "Energy":
      self.core.setEnergy(float(parts[1]))
      # und weil energy das letzte im satz ist
      self.core.act()
    elif parts[0] == "RobotsLeft":
      pass
    elif parts[0] == "Collision":
      self.core.navigator.processCollision(int(parts[1]),float(parts[2]))
      self.core.processCollision(int(parts[1]),float(parts[2]))
    elif parts[0] == "Warning":
      self.core.processWarning(parts[1],parts[2])
    elif parts[0] == "Dead":
      self.core.die()
    elif parts[0] == "GameFinishes":
      self.core.retire()
    elif parts[0] == "ExitRobot":
      self.core.exit()
    else:
      self.say("unknown server message %s"%(parts[0]))
      #sys.exit(2)

  def sendName(self,name):
    print "Name %s"%(name)

  def sendColor(self,color1,color2):
    print "Colour %s %s"%(color1,color2)

  def say(self,string):
    print "Print %s"%(string)
    print >> sys.stderr, string

  def send(self,string):
    if not self.core.dead:
      print string
      self.f.write(string+"\n")
