from pn_utils import *

class Entity(object):
    def __init__(self, my_position=Vec2(0, 0)):
        print "Entity pre-initialization"
        self.id = 0 # Manager will assign before Init() called
        self.core = None # Same here
        
        self.position = my_position
        
    def Init(self):
        print str(type(self)) + " initialized with ID " + str(self.id)
        
    def Step(self):
        pass
        
    def Destroy(self):
        print str(type(self)) + " destroyed " + str(self.id)
        
    def Draw(self):
        pass

