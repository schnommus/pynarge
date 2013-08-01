from PyNARGE import *
import random
import math

appSize = Vec2(800, 600)

class Respawnable(ComponentEntity):
    def Step(self):
        if self.position.y > appSize.y+100: # If object is offscreen
            self.core.entityManager.AddEntity( type(self)() ) # Spawn new object
            self.core.entityManager.RemoveEntity(self) # Destroy self

class Crate(Respawnable):
    def Build(self):
        self.AddComponent( SpriteComponent( self.core.resourceManager.FetchTexture("media\\crate.png") ) )
        self.AddComponent( RigidBody_Rectangular((16, 16), (random.randint(200,appSize.x-200), (random.randint(-400, -100))) ) )

class Stone(Respawnable):
    def Build(self):
        self.AddComponent( SpriteComponent( self.core.resourceManager.FetchTexture("media\\circle.png") ) )
        self.AddComponent( RigidBody_Circular(20, (random.randint(200, appSize.x-200), (random.randint(-400, -100))) ) )

class Ground(ComponentEntity):
    def Build(self):
        self.AddComponent( StaticBody_Rectangular( Vec2(300, 10), Vec2(appSize.x/2, appSize.y-100) ) )
        self.AddComponent( SpriteComponent( self.core.resourceManager.FetchTexture("media\\bar.png") ) )

class HelperText(ComponentEntity):
    def Build(self):
        self.AddComponent( TextComponent("Click and drag mouse to manipulate objects") )
        self.position = (appSize.x/2-200, appSize.y-65)

class Background(ComponentEntity):
    def Build(self):
        self.AddComponent( SpriteComponent( self.core.resourceManager.FetchTexture("media\\background.jpg"), (appSize.x, appSize.y) ) )
        self.position = (appSize.x/2, appSize.y/2)
        
# PROGRAM BEGINS

app = GameCore(False, "Crates Demo", appSize.x, appSize.y, False)

app.renderer.window.framerate_limit = 60

app.entityManager.AddEntity( Background() )
app.entityManager.AddEntity( HelperText() )
app.entityManager.AddEntity( Ground() )

for i in range(100):
    app.entityManager.AddEntity( Crate() )
    app.entityManager.AddEntity( Stone() )
    
app.Run()
