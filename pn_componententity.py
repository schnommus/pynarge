from pn_entity import Entity

class ComponentEntity(Entity):
    def __init__(self):
        Entity.__init__(self)
        self.components = []
    
    def AddComponent(self, component):
        self.components.append(component)
        component.core = self.core
        component.entity = self
        component.Init()
        
    def Step(self):
        for component in self.components:
            component.Step()
        
    def Destroy(self):
        print str(type(self)) + " destroyed " + str(self.id)
        for component in self.components:
            component.Destroy()
        
    def Draw(self):
        for component in self.components:
            component.Draw()

