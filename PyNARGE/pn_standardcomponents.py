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
    def __init__(self, texture, forcedSize=None):
        self.sprite = Sprite(texture)
        
        if forcedSize != None:
            forcedSize = Vec2(forcedSize)
            self.sprite.scale(
                ( float(forcedSize.x)/float(texture.size.x),
                float(forcedSize.y)/float(texture.size.y) ) )
            
        self.sprite.origin = Vec2(texture.size)/2

    def Draw(self):
        self.sprite.position = self.entity.position
        self.sprite.rotation = -self.entity.rotation
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

class VelocityComponent(Component):
    def Init(self, startingVelocity=Vec2(0, 0)):
        self.velocity = startingVelocity

    def SetVelocity(self, velocity):
        self.velocity = Vec2(velocity)
    
    def Step(self):
        self.entity.position += self.velocity*self.core.time.GetDelta()

class AttractedToComponent(Component):
    def __init__(self, target=None, factor=1.0):
        self.target = target
        self.factor = factor

    def SetTarget(self, target):
        self.target = target

    def SetFactor(self, factor):
        self.factor = factor

    def Step(self):
        if self.target:
            diff = Vec2(self.target.position)-Vec2(self.entity.position)
            dist = max(self.entity.position.get_distance(self.target.position)**2, 3)
            direction = diff.normalized()
            self.entity.FetchComponent( VelocityComponent ).velocity = self.entity.FetchComponent( VelocityComponent ).velocity + direction*((self.factor*self.core.time.GetDelta())/(dist))


