from pn_resources import *
from pn_resourcemanager import *
from pn_utils import *

class ShaderPass(object):
    def __init__(self, shader, target=None):
        self.shader = shader
        self.core = None
        self.target = target
        self.renderTexture = None
        self.shaderLoaded = False
        self.renderStates = RenderStates()

    def SetTarget(self, target):
        self.target = target

    def SetCenter(self, position):
        self.renderTexture.view.center = Vec2(position)

    def SetParameter(self, parameter, value):
        self.shader.set_parameter(parameter, value)
    
    def Initialize(self, size):
        self.shaderLoaded = Shader.is_available()
        self.renderStates.shader = self.shader
        self.renderTexture = RenderTexture( size.x, size.y )

        # For shaders drawing to shaders
        self._draw = self.renderTexture.draw

    def Draw(self, ent):
        self.renderTexture.draw(ent)

    def SendToTarget(self):
        self.renderTexture.display()
        spr = Sprite( self.renderTexture.texture )
        spr.position += self.core.renderer.GetCameraPosition()-self.core.renderer.GetWindowSize()/2
        self.target._draw(spr, self.renderStates)
        self.renderTexture.clear(Color(0, 0, 0, 0))
