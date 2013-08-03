from pn_componententity import *
from pn_standardcomponents import *

class BackgroundImage(ComponentEntity):
    def __init__(self, texture):
        ComponentEntity.__init__(self)
        self.texture = texture
    
    def Build(self):
        self.drawlayer = -100
        self.steplayer = 100
        self.AddComponent( SpriteComponent( self.texture, self.core.renderer.GetWindowSize() ) )
        self.position = self.core.renderer.GetWindowSize()/2
        
    def Step(self):
        self.position = self.core.renderer.GetCameraPosition()


class DefaultText(ComponentEntity):
    def __init__(self, text, position):
        ComponentEntity.__init__(self)
        self.text = text
        self.position = position
        
    def Build(self):
        self.AddComponent( TextComponent(self.text) )
