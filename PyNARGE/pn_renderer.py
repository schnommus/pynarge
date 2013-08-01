import sfml
from pn_utils import Vec2

class Renderer(object):
    def __init__(self, core):
        self.core = core
        self.window = None
        self.size = Vec2(0, 0)
        self.shaderpasses = []
    
    def Initialize( self, title="PyNARGE Window", size_x=800, size_y=600, fullscreen=False, antialiasing=False ):
        print "Creating render window..."
        self.size = Vec2(size_x, size_y)
        self.window = sfml.RenderWindow(sfml.VideoMode(size_x, size_y), title, sfml.window.Style.FULLSCREEN if fullscreen else sfml.window.Style.DEFAULT, sfml.window.ContextSettings(0, 0, 8) if antialiasing else None )
        self._draw = self.window.draw
        
    def AddShaderPass( self, shaderpass ):
        shaderpass.core = self.core
        shaderpass.Initialize( self.size )
        self.shaderpasses.append( shaderpass )
        return shaderpass

    def Draw( self, ent, shaderpass=None ):
        if shaderpass==None:
            self.window.draw(ent)
        else:
            shaderpass.Draw(ent)
    
    def Update( self ):
        for event in self.window.events:
            if type(event) is sfml.CloseEvent:
                self.window.close()
                self.core.Quit()

        for p in self.shaderpasses:
            p.SendToDisplay()
        
        self.window.display()
        self.window.clear(sfml.Color(0, 0, 0))

    def GetWindowSize(self):
        return self.size
