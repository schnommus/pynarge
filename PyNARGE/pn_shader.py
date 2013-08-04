from pn_resources import *
from pn_resourcemanager import *
from pn_utils import *

class ShaderPass(object):
    """Allows connection of :class:`Shader` instances in 'passes', which eventually lead to the display"""
    def __init__(self, shader, target=None):
        """Constructor

        :param shader: Pixel shader to be represented by this pass
        :type shader: :class:`Shader`
        :param target: Where this pass should draw to
        :type target: Either :class:`Renderer` or :class:`ShaderPass` instance"""
        self.shader = shader
        self.core = None
        self.target = target
        self.renderTexture = None
        self.shaderLoaded = False
        self.renderStates = RenderStates()

    def SetTarget(self, target):
        """Change the shader's target draw surface

        :param target: Where this pass should draw to
        :type target: Either :class:`Renderer` or :class:`ShaderPass` instance"""
        self.target = target

    def SetCenter(self, position):
        """Position of the shader's source, target in global coords. Internally called
        by :func:`Renderer.SetCamera`.

        :param position: Shader's new center
        :type position: :class:`Vec2`"""
        self.renderTexture.view.center = Vec2(position)

    def SetParameter(self, parameter, value):
        """Mechanism for setting a 'uniform' GLSL shader variables

        :param parameter: Name of the GLSL variable
        :type parameter: str
        :param value: Value to set GLSL parameter too
        :type value: float, int, vec2, etc"""
        self.shader.set_parameter(parameter, value)
    
    def Initialize(self, size):
        """Must be executed before the instance can be used.
        Internally called by :class:`Renderer` after :func:`Renderer.AddShaderPass` is called.

        :param size: Size of shader surface (almost always :func:`Renderer.GetWindowSize`)
        :type parameter: Vec2
        """
        self.shaderLoaded = Shader.is_available()
        self.renderStates.shader = self.shader
        self.renderTexture = RenderTexture( size.x, size.y )

        # For shaders drawing to shaders
        self._draw = self.renderTexture.draw

    def Draw(self, ent):
        """Draw something to the shader pass before processing.

        :param ent: Drawable to draw
        :type ent: A Drawable object
        """
        self.renderTexture.draw(ent)

    def SendToTarget(self):
        """Executes shader and draws surface to target"""
        self.renderTexture.display()
        spr = Sprite( self.renderTexture.texture )
        spr.position += self.core.renderer.GetCameraPosition()-self.core.renderer.GetWindowSize()/2
        self.target._draw(spr, self.renderStates)
        self.renderTexture.clear(Color(0, 0, 0, 0))
