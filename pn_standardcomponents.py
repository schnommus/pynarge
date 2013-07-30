from pn_component import Component
from pn_resources import Text, Color
from pn_utils import Vec2
from random import randint

class TextComponent(Component):
    def __init__(self, text, font=None, size=20, offset=Vec2(0,0)):
        self.message = text
        self.offset = offset
        self.size = size
        self.font = font
    
    def Init(self):
        self.text = Text()
        self.text.font = self.core.resourceManager.FetchDefaultFont() if self.font==None else self.font
        self.text.character_size = self.size
        self.text.color = Color.WHITE

    def SetText(self, message):
        self.message = message
        
    def Step(self):
        self.text.position = self.entity.position + self.offset
        self.text.string = self.message
        
    def Draw(self):
        self.core.renderer.window.draw(self.text)


class BrownianComponent(Component):
    def Step(self):
        self.entity.position.x += randint(-100, 100)*self.core.time.GetDelta()
        self.entity.position.y += randint(-100, 100)*self.core.time.GetDelta()
