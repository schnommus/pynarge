from pn_componententity import *
from pn_standardcomponents import *
from pn_physics import *
from pn_resources import *

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


class WaterParticle(ComponentEntity):
    def Build(self):
        self.AddComponent( SpriteComponent( self.core.resourceManager.FetchTexture(EngineMediaDirectory()+r"textures\waterparticle.png"), (16, 16), self.core.engineShaders.GetWaterShader()) )
        self.AddComponent( RigidBody_Circular(6, self.position, 0.0, 0.2 ) )
