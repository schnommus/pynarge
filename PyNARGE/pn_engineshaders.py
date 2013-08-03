from pn_resources import *
from pn_resourcemanager import *
from pn_utils import *
from pn_shader import *

class EngineShaders(object):
    def __init__(self, core):
        self.core = core

    def GetWaterShader(self):
        # If the shader hasn't been used before, create ShaderPass stack; otherwise return the top pass for drawing too.
        if not hasattr(self, "_waterShader"):
            self._waterShader = self.core.renderer.AddShaderPass( ShaderPass( self.core.resourceManager.FetchShader(EngineMediaDirectory()+r"shaders\water_pass1.glsl") ) )
            waterPass2 = self.core.renderer.AddShaderPass( ShaderPass( self.core.resourceManager.FetchShader(EngineMediaDirectory()+r"shaders\water_pass2.glsl") ) )
            self._waterShader.SetTarget( waterPass2 )
            waterPass2.SetTarget( self.core.renderer )

            self._waterShader.SetParameter( "size_x", self.core.renderer.GetWindowSize().x )
            self._waterShader.SetParameter( "size_y", self.core.renderer.GetWindowSize().y )
            waterPass2.SetParameter( "size_x", self.core.renderer.GetWindowSize().x )
            waterPass2.SetParameter( "size_y", self.core.renderer.GetWindowSize().y )
            
        return self._waterShader
