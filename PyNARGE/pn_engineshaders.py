from pn_resources import *
from pn_resourcemanager import *
from pn_utils import *
from pn_shader import *

class EngineShaders(object):
    """For getting instances to some standard engine shaders, usually the bottom of a :class:`PyNARGE.ShaderPass` stack"""
    def __init__(self, core):
        self.core = core

    def GetPixelateShader(self):
        if not hasattr(self, "_pixelateShader"):
            self._pixelateShader = self.core.renderer.AddShaderPass( ShaderPass( self.core.resourceManager.FetchShader(EngineMediaDirectory()+r"shaders\pixelate.glsl") ) )
            self._pixelateShader.SetTarget( self.core.renderer )
            
        return self._pixelateShader

    def GetWaterShader(self, withPixelate=False):
        """Returns the engine's 2D water shader as :class:`PyNARGE.ShaderPass`. See :class:`PyNARGE.WaterParticle` for an example usage.

        :returns: :class:`ShaderPass` -- the shader instance"""
        # If the shader hasn't been used before, create ShaderPass stack; otherwise return the top pass for drawing too.
        if not hasattr(self, "_waterShader"):
            self._waterShader = self.core.renderer.AddShaderPass( ShaderPass( self.core.resourceManager.FetchShader(EngineMediaDirectory()+r"shaders\water_pass1.glsl") ) )
            waterPass2 = self.core.renderer.AddShaderPass( ShaderPass( self.core.resourceManager.FetchShader(EngineMediaDirectory()+r"shaders\water_pass2.glsl") ) )
            self._waterShader.SetTarget( waterPass2 )

            result = None
            
            if not withPixelate:
                waterPass2.SetTarget( self.core.renderer )
            else:
                waterPass2.SetTarget( self.GetPixelateShader() )

            self._waterShader.SetParameter( "size_x", self.core.renderer.GetWindowSize().x )
            self._waterShader.SetParameter( "size_y", self.core.renderer.GetWindowSize().y )
            waterPass2.SetParameter( "size_x", self.core.renderer.GetWindowSize().x )
            waterPass2.SetParameter( "size_y", self.core.renderer.GetWindowSize().y )
            
        return self._waterShader
