from pn_utils import *

class Entity(object):
    
    # Subclasses should call this first if they want a constructor
    def __init__(self, position=Vec2(0, 0), rotation=0.0, size=Vec2(100,100) ):
        self.id = 0 # Manager will assign before Init() called
        self.core = None # Same here
        
        self.position = Vec2(position)
        self.rotation = float(rotation)
        self.size = Vec2(size)
        self.drawlayer = 0
        self.steplayer = 0
        
    def _Init(self):
        if self.core.debugInfo:
            print str(type(self)) + " initialized with ID " + str(self.id)
        self.Init()
        
    def _Step(self):
        self.Step()
        
    def _Destroy(self):
        if self.core.debugInfo:
            print str(type(self)) + " destroyed " + str(self.id)
        self.Destroy()
        
    def _Draw(self):
        self.Draw()

    def Init(self):
        pass
    def Step(self):
        pass
    def Destroy(self):
        pass
    def Draw(self):
        pass

