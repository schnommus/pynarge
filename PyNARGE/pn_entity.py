from pn_utils import *

class Entity(object):
    
    # Subclasses must call this first if they want a constructor
    def __init__(self, my_position=Vec2(0, 0), rotation=0.0):
        self.id = 0 # Manager will assign before Init() called
        self.core = None # Same here
        
        self.position = my_position
        self.rotation = rotation
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

