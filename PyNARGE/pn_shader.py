from pn_resources import *
from pn_resourcemanager import *
import sfml

class ShaderPass(object):
    def __init__(self, shader, target=None):
        self.shader = shader
        self.core = None
        self.target = target
        self.renderTexture = None
        self.shaderLoaded = False
        self.renderStates = sfml.RenderStates()

    def SetTarget(self, target):
        self.target = target

    def Initialize(self, size):
        self.shaderLoaded = Shader.is_available()
        self.renderStates.shader = self.shader
        self.renderTexture = RenderTexture( size.x, size.y )

        # Purely for shaders drawing to shaders. Note no capitalization
        self._draw = self.renderTexture.draw

    def Draw(self, ent):
        self.renderTexture.draw(ent)

    def SendToDisplay(self):
        self.renderTexture.display()
        spr = Sprite( self.renderTexture.texture )
        self.target._draw(spr, self.renderStates)
        self.renderTexture.clear(Color(0, 0, 0, 0))
