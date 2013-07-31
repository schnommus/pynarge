from PyNARGE import *
import random
import math

class Crate(ComponentEntity):
    def Build(self):
        self.AddComponent( SpriteComponent( self.core.resourceManager.FetchTexture("media\crate.png") ) )
        self.AddComponent( RigidBody_Rectangular((1, 1), (random.randint(1, 100)/5, (random.randint(1, 100)/5)) ) )

class Stone(ComponentEntity):
    def Build(self):
        self.AddComponent( SpriteComponent( self.core.resourceManager.FetchTexture("media\circle.png") ) )
        self.AddComponent( RigidBody_Circular(1.25, (random.randint(1, 100)/5, (random.randint(1, 100)/5)) ) )

class Ground(ComponentEntity):
    def Build(self):
        self.AddComponent( StaticBody_Rectangular( Vec2(50, 10), Vec2(0, -10) ) )

# PROGRAM BEGINS

app = GameCore(False, "Crates Demo")

app.renderer.window.framerate_limit = 60

app.entityManager.AddEntity( Ground() )

for i in range(50):
    app.entityManager.AddEntity( Crate() )
    app.entityManager.AddEntity( Stone() )
    
app.Run()
