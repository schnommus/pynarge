from pn_componententity import *
from pn_standardcomponents import *
from pn_physics import *
from pn_resources import *


class GUI_Dialog(ComponentEntity):
    def __init__(self, name = "UntitledDialogue", size=Vec2(150, 100), position=Vec2(0, 0)):
        ComponentEntity.__init__(self)
        self.name = name
        self.size = Vec2(size)
        self.position = Vec2(position)
    
    def Build(self):
        self.body_rectangle = RectangleShape( self.size )
        self.body_rectangle.fill_color = Color(0, 0, 0, 128)
        self.body_rectangle.position = self.position
        self.body_rectangle.outline_color = Color(255, 255, 255, 100)
        self.body_rectangle.outline_thickness = 1
        self.titlebar_rectangle = RectangleShape( Vec2(self.size.x, 20) )
        self.titlebar_rectangle.fill_color = Color(0, 0, 0, 128)
        self.titlebar_rectangle.position = self.position
        self.titlebar_rectangle.outline_color = Color(255, 255, 255, 100)
        self.titlebar_rectangle.outline_thickness = 1
        self.AddComponent( TextComponent( self.name, None, 16, offset=Vec2(4, 0) ) )

        self.lastPosition = None
        self.currentPosition = None
        
        self.isSelected = False
        
    def Step(self):

        if( self.isSelected ):
            self.titlebar_rectangle.outline_color = Color(255, 255, 255, 255)
            self.currentPosition = self.core.input.GetMousePositionUI()
            if not self.lastPosition ==  None:
                newPosition = self.position + (self.currentPosition-self.lastPosition)
                self.position = newPosition
            self.lastPosition = self.currentPosition
        else:
            self.titlebar_rectangle.outline_color = Color(255, 255, 255, 100)
            self.lastPosition = None

        if self.position.x < 0:
            self.position.x = 0
        if self.position.y < 0:
            self.position.y = 0
        if self.position.x > self.core.renderer.GetWindowSize().x-self.size.x:
            self.position.x = self.core.renderer.GetWindowSize().x-self.size.x
        if self.position.y > self.core.renderer.GetWindowSize().y-self.size.y:
            self.position.y = self.core.renderer.GetWindowSize().y-self.size.y

        mouse = self.core.input.mouse
        if( mouse.is_button_pressed( mouse.LEFT ) ):
            mouse_pos = self.core.input.GetMousePositionUI()
            if ( mouse_pos.x > self.position.x ) and ( mouse_pos.x < self.position.x + self.size.x ) and ( mouse_pos.y > self.position.y ) and ( mouse_pos.y < self.position.y + 20 ):
                self.isSelected = True
            else:
                self.isSelected = False
        else:
            self.isSelected = False

        self.body_rectangle.position = self.position
        self.titlebar_rectangle.position = self.position

    def Draw(self):
        self.core.renderer.Draw(self.body_rectangle)
        self.core.renderer.Draw(self.titlebar_rectangle)

class GUI_Button(ComponentEntity):
    def __init__(self, parent, name = "UntitledButton", size=Vec2(70, 30), offset=Vec2(0, 0), function=None):
        ComponentEntity.__init__(self)
        self.name = name
        self.size = Vec2(size)
        self.offset = Vec2(offset)
        self.parent = parent
        self.function = function

    def OnClick(self):
        print "Button: '" + self.name + "' (with ID " + str(self.id) + ") was pressed"
        
        if self.function:
            self.function(self.core)
    
    def Build(self):
        self.body_rectangle = RectangleShape( self.size )
        self.body_rectangle.fill_color = Color(0, 0, 0, 128)
        self.body_rectangle.position = self.position
        self.body_rectangle.outline_color = Color(255, 255, 255, 100)
        self.body_rectangle.outline_thickness = 1
        self.AddComponent( TextComponent( self.name, None, 16, offset=Vec2(4, (self.size.y)/2.0-16) ) )

        
        self.isHovered = False
        self.wasClicked = False
        
    def Step(self):

        mouse = self.core.input.mouse

        if( self.isHovered ):
            self.body_rectangle.outline_color = Color(255, 255, 255, 255)
            if( mouse.is_button_pressed( mouse.LEFT ) ):
                self.wasClicked = True
                self.body_rectangle.fill_color = Color(128, 128, 255, 128)
            else:
                if self.wasClicked:
                    self.OnClick()
                    self.wasClicked = False
                    
                self.body_rectangle.fill_color = Color(0, 0, 0, 128)
        else:
            self.wasClicked = False
            self.body_rectangle.outline_color = Color(255, 255, 255, 100)
            self.body_rectangle.fill_color = Color(0, 0, 0, 128)

        mouse_pos = self.core.input.GetMousePositionUI()
        if ( mouse_pos.x > self.position.x ) and ( mouse_pos.x < self.position.x + self.size.x ) and ( mouse_pos.y > self.position.y ) and ( mouse_pos.y < self.position.y + self.size.y ):
            self.isHovered = True
        else:
            self.isHovered = False


        self.position = self.parent.position + self.offset
        self.body_rectangle.position = self.position

    def Draw(self):
        self.core.renderer.Draw(self.body_rectangle)

