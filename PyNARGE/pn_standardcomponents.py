from pn_component import Component
from pn_resources import Text, Color, Sprite, Rectangle
from pn_utils import Vec2
from random import randint

class TextComponent(Component):
    def __init__(self, text, font=None, size=20, color=Color.WHITE, offset=Vec2(0,0)):
        self.message = text
        self.offset = offset
        self.size = size
        self.font = font
        self.color = color
        self.scale = 1.0
    
    def Init(self):
        self.text = Text()
        self.text.font = self.core.resourceManager.FetchDefaultFont() if self.font==None else self.font
        self.text.character_size = self.size
        self.text.color = self.color

    def SetText(self, message):
        self.message = message

    def ReCenter(self):
        self.text.origin = Vec2(self.text.local_bounds.size.x/2, self.size/2)
        
    def Step(self):
        self.text.position = self.entity.position + self.offset
        self.text.string = self.message
        self.text.color = self.color
        self.text.ratio = (self.scale, self.scale)
        self.text.rotation = self.entity.rotation
        
    def Draw(self):
        self.core.renderer.Draw(self.text)

class SpriteComponent(Component):
    def __init__(self, texture, forcedSize=None, shaderPass=None, offset=(0,0)):
        self.sprite = Sprite(texture)
        self.shaderPass = shaderPass
        self.offset = Vec2(offset)
        self.alpha = 255
        self.scale = 1
        self.forcedSize = None
        if forcedSize != None:
            self.forcedSize = Vec2(forcedSize)
            
        self.sprite.origin = Vec2(texture.size)/2
    
    def SetTexture(self, texture, forcedSize=None, shaderPass=None):
        self.sprite = Sprite(texture)
        self.shaderPass = shaderPass
        
        self.forcedSize = Vec2(forcedSize)
            
        self.sprite.origin = Vec2(texture.size)/2
    
    def Draw(self):
        self.sprite.color = Color(255, 255, 255, self.alpha)
        
        
        self.sprite.ratio = Vec2(self.scale, self.scale)
        if self.forcedSize != None:
            self.sprite.scale(
                ( float(self.forcedSize.x)/float(self.sprite.texture.size.x),
                float(self.forcedSize.y)/float(self.sprite.texture.size.y) ) )
            
        self.sprite.position = self.entity.position + self.offset
        self.sprite.rotation = -self.entity.rotation
        if hasattr( self.entity, 'image' ):
            self.sprite.rotation = self.entity.rotation
        self.core.renderer.Draw(self.sprite, self.shaderPass)

class PixelSpriteComponent(Component):
    def __init__(self, texture, shaderPass=None, hasDirectionSheet=False):
        self.sprite = Sprite(texture, Rectangle( (0, 0), (texture.size.x/(8 if hasDirectionSheet else 1), texture.size.y)) )
        self.shaderPass = shaderPass
        self.alpha = 255
        self.scale = 4
        self.hasDirectionSheet = hasDirectionSheet
        
        self.sprite.origin = Vec2(texture.size.x/(8 if hasDirectionSheet else 1), texture.size.y)/2
    
    def SetTexture(self, texture, shaderPass=None, hasDirectionSheet=False):
        self.sprite = Sprite(texture, Rectangle( (0, 0), (texture.size.x/(8 if hasDirectionSheet else 1), texture.size.y)) )
        self.shaderPass = shaderPass
        self.hasDirectionSheet = hasDirectionSheet
            
        self.sprite.origin = Vec2(texture.size.x/(8 if hasDirectionSheet else 1), texture.size.y)/2
    
    def Draw(self):
        self.sprite.color = Color(255, 255, 255, self.alpha)
        
        
        self.sprite.ratio = Vec2(self.scale, self.scale)
            
        self.sprite.position = Vec2(1+4*int(self.entity.position.x/4), 4*int(self.entity.position.y/4))
        self.sprite.rotation = -self.entity.rotation + 22.5
        self.sprite.rotation %= 360

        if self.hasDirectionSheet:
            index = int( self.sprite.rotation/45)
            self.sprite.rotation = 0
            self.sprite.texture_rectangle = Rectangle( (index*self.sprite.texture.size.x/8, 0), (self.sprite.texture.size.x/8, self.sprite.texture.size.y))
        else:
            self.sprite.rotation = int( self.sprite.rotation/90)*90

        self.core.renderer.Draw(self.sprite, self.shaderPass)


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

class RespawnableComponent(Component):
    def __init__(self, condition):
        
        self.condition = condition
        
    def Step(self):
        if self.condition(self.entity):
            self.core.entityManager.RemoveEntity(self.entity) # Destroy self

    def Destroy(self):
        if self.core.networking.is_server or not self.entity.networked:
            self.core.entityManager.AddEntity( type(self.entity)() ) # Spawn new object

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


