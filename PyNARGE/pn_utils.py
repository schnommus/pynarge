from pygame_vec2 import *

class IdDispensor(object):
    def __init__(self):
        self.currentID = 0
        
    def GetNewID(self):
        self.currentID += 1
        return self.currentID
    
    def FreeID(self, the_id):
        pass

import sfml

class Time(object):
    def __init__(self):
        self.clock = sfml.Clock()
        self.delta = 0.0
    def Tick(self):
        self.delta = self.clock.restart().seconds
    def GetDelta(self):
        return self.delta

# Just wrapping pygame's class for now
class Vec2(Vec2d):
    pass
