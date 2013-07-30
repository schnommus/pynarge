from pn_component import Component
from pn_resources import Text, Color, Sprite
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

class SpriteComponent(Component):
    def __init__(self, texture):
        self.sprite = Sprite(texture)
        self.sprite.origin = Vec2(texture.size)/2

    def Draw(self):
        self.sprite.position = self.entity.position
        self.core.renderer.window.draw(self.sprite)

class FollowComponent(Component):
    def __init__(self, target=None, offset=Vec2(0,0)):
        self.target = target
        self.offset = Vec2(offset)

    def SetTarget(self, target):
        self.target = target

    def SetOffset(self, offset):
        self.offset = Vec2(offset)

    def Step(self):
        if self.target:
            self.entity.position = self.target.position + self.offset

class BrownianComponent(Component):
    def Init(self, factor=100):
        self.factor = factor
        
    def Step(self):
        self.entity.position.x += randint(-self.factor, self.factor)*self.core.time.GetDelta()
        self.entity.position.y += randint(-self.factor, self.factor)*self.core.time.GetDelta()


