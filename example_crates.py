from PyNARGE import *
import random
import math

appSize = Vec2(800, 600)

class Crate(ComponentEntity):
    def Build(self):
        self.AddComponent( SpriteComponent( self.core.resourceManager.FetchTexture("media\\crate.png") ) )
        self.AddComponent( RigidBody_Rectangular((16, 16), (random.randint(200,appSize.x-200), (random.randint(-400, -100))) ) )

    def Step(self):
        if self.position.y > appSize.y+100: # If object is offscreen
            self.core.entityManager.AddEntity( Crate() ) # Spawn new object
            self.core.entityManager.RemoveEntity(self) # Destroy self

class Stone(ComponentEntity):
    def Build(self):
        self.AddComponent( SpriteComponent( self.core.resourceManager.FetchTexture("media\\circle.png") ) )
        self.AddComponent( RigidBody_Circular(20, (random.randint(200, appSize.x-200), (random.randint(-400, -100))) ) )
        
    def Step(self):
        if self.position.y > appSize.y+100:
            self.core.entityManager.AddEntity( Stone() )
            self.core.entityManager.RemoveEntity(self)

class Ground(ComponentEntity):
    def Build(self):
        self.AddComponent( StaticBody_Rectangular( Vec2(300, 10), Vec2(appSize.x/2, appSize.y-100) ) )
        self.AddComponent( SpriteComponent( self.core.resourceManager.FetchTexture("media\\bar.png") ) )


# PROGRAM BEGINS

app = GameCore(False, "Crates Demo", appSize.x, appSize.y)

app.renderer.window.framerate_limit = 60

app.entityManager.AddEntity( Ground() )

for i in range(100):
    app.entityManager.AddEntity( Crate() )
    app.entityManager.AddEntity( Stone() )
    
app.Run()
