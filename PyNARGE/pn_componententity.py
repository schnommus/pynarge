from pn_entity import Entity
from pn_standardcomponents import TextComponent
from pn_utils import Vec2

class ComponentEntity(Entity):
    def __init__(self, position=Vec2(0, 0), rotation=0.0, size=Vec2(100,100) ):
        Entity.__init__(self, position, rotation, size)
        self.components = []
    
    def AddComponent(self, component):
        self.components.append(component)
        component.core = self.core
        component.entity = self
        return component

##        if self.core != None:
##            component.Init()

    def FetchComponent(self, componentClass):
        for component in self.components:
            if type(component)==componentClass:
                return component

    def Build(self):
        pass
        
    def _Init(self):
        self.Build()

        if self.core.settings.label_entity_types:
            self.AddComponent(TextComponent(str(type(self).__name__), self.core.resourceManager.FetchDefaultFontMono(), 12, Vec2(0, -10)))
        
        for component in self.components:
            component.Init()
        self.Init()
        
    def _Step(self):
        for component in self.components:
            component.Step()
        self.Step()
        
    def _Destroy(self):
        for component in self.components:
            component.Destroy()
        self.Destroy()
        
    def _Draw(self):
        for component in self.components:
            component.Draw()
        self.Draw()

