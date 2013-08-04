class Component(object):
    """Base class of components that can be added to entities"""
    def __init__(self):
        self.core = None
        self.entity = None

    def Init(self):
        """Called just after component creation: self.core, self.entity is set"""
        pass
        
    def Step(self):
        """Called every frame"""
        pass
        
    def Destroy(self):
        """Called just before component is destroyed"""
        pass
        
    def Draw(self):
        """Called while the entity is being drawn"""
        pass

