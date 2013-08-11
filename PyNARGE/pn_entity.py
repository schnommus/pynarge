from pn_utils import *

class Entity(object):
    """Base class of all entities, most entities should inherit from :class:`PyNARGE.ComponentEntity`, however."""
    # Subclasses should call this first if they want a constructor
    def __init__(self, position=Vec2(0, 0), rotation=0.0, size=Vec2(100,100) ):
        """Constructor

        :param position: Coordinates at which entity will be created
        :type position: Vec2
        :param rotation: Initial entity rotation, degrees
        :type rotation: float
        :param size: Size of entities' bounding box
        :type size: Vec2"""
        self.id = 0 # Manager will assign before Init() called
        self.core = None # Same here
        
        self.position = Vec2(position)
        self.rotation = float(rotation)
        self.size = Vec2(size)
        self.drawlayer = 0
        self.steplayer = 0
        self.networked = False
        self.spawned_by_server = False
        
    def _Init(self):
        self.Init()
        
    def _Step(self):
        self.Step()
        
    def _Destroy(self):
        self.Destroy()
        
    def _Draw(self):
        self.Draw()

    def OnMouseOver(self):
        """For normal entities, this is currently never called. For physics entities, this function will be called when a mouse is over the entities' physics body."""
        pass

    def OnCollision(self, other):
        """For physics entities, this is called whenever another object collides with the entity"""
        pass

    def Init(self):
        """Called as soon as an entity is attached to an :class:`PyNARGE.EntityManager`"""
        pass
    def Step(self):
        """Called every frame. To change step ordering, you can alter `Entity.steplayer` (higher is later)"""
        pass
    def Destroy(self):
        """Called just before an entity is destroyed"""
        pass
    def Draw(self):
        """Called every frame. To change draw layer, you can alter `Entity.drawlayer` (higher is later)"""
        pass

