import sfml
from pn_utils import Vec2

class Renderer(object):
    def __init__(self, core):
        self.core = core
        self.window = None
        self.size = Vec2(0, 0)
    
    def Initialize( self, title="PyNARGE Window", size_x=800, size_y=600, fullscreen=False, antialiasing=False ):
        print "Creating render window..."
        self.size = Vec2(size_x, size_y)
        self.window = sfml.RenderWindow(sfml.VideoMode(size_x, size_y), title, sfml.window.Style.FULLSCREEN if fullscreen else sfml.window.Style.DEFAULT, sfml.window.ContextSettings(0, 0, 8) if antialiasing else None )

    def Update( self ):
        for event in self.window.events:
            if type(event) is sfml.CloseEvent:
                self.window.close()
                self.core.Quit()

        self.window.display()
        self.window.clear(sfml.Color(0, 0, 0))

    def GetWindowSize(self):
        return self.size
