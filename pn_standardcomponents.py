from pn_component import Component
from pn_resources import Text, Color
from pn_utils import Vec2
from random import randint

class TextComponent(Component):
    def __init__(self, text, offset=Vec2(0,0)):
        self.message = text
        self.offset = offset
    
    def Init(self):
        self.text = Text()
        self.text.font = self.core.resourceManager.FetchDefaultFont()
        self.text.character_size = 20
        self.text.color = Color.WHITE
        
    def Step(self):
        self.text.position = self.entity.position + self.offset
        self.text.string = self.message
        
    def Draw(self):
        self.core.renderer.window.draw(self.text)


class ShakeComponent(Component):
    def Step(self):
        self.entity.position.x = randint(0, 100)
