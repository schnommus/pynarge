from pn_entity import Entity
from pn_standardcomponents import TextComponent
from pn_utils import Vec2

class ComponentEntity(Entity):
    """Base class for entities that are created using components"""
    
    def __init__(self, position=Vec2(0, 0), rotation=0.0, size=Vec2(100,100) ):
        """Constructor

        :param position: Coordinates at which entity will be created
        :type position: Vec2
        :param rotation: Initial entity rotation, degrees
        :type rotation: float
        :param size: Size of entities' bounding box
        :type size: Vec2"""
        Entity.__init__(self, position, rotation, size)
        self.components = []
    
    def AddComponent(self, component):
        """Adds a component to an entity
        :param component: The component to add
        :type component: :class:`PyNARGE.Component`
        :returns: The component that was added"""
        self.components.append(component)
        component.core = self.core
        component.entity = self
        return component

#       Maybe a later feature, adding components after an entity has been initialized
##        if self.core != None:
##            component.Init()

    def FetchComponent(self, componentClass):
        """Retrieves a component by type, i.e `theComponent = entity.FetchComponent( SomeComponentType )`"""
        for component in self.components:
            if type(component)==componentClass:
                return component

    def Build(self):
        """This is where components should be added to an entity - it's called just before :func:`PyNARGE.ComponentEntity.Init()`"""
        pass
        
    def _Init(self):
        self.Build()

        if self.core.settings.label_entity_types:
            self.AddComponent(TextComponent(str(type(self).__name__), self.core.resourceManager.FetchDefaultFontMono(), 12, Vec2(0, -10)))
        
        for component in self.components:
            component.Init()
        self.Init()
        
    def _Step(self):
        self.Step()
        for component in self.components:
            component.Step()
        
    def _Destroy(self):
        for component in self.components:
            component.Destroy()
        self.Destroy()
        
    def _Draw(self):
        self.Draw()
        for component in self.components:
            component.Draw()

