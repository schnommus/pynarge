from PyNARGE import *
import random
import math

class Crate(ComponentEntity):
    def Build(self):
        self.AddComponent( SpriteComponent( self.core.resourceManager.FetchTexture("media\\crate.png") ) )
        self.AddComponent( RigidBody_Rectangular((32, 32), (random.randint(1,800), (random.randint(1, 400))) ) )

class Stone(ComponentEntity):
    def Build(self):
        self.AddComponent( SpriteComponent( self.core.resourceManager.FetchTexture("media\\circle.png") ) )
        self.AddComponent( RigidBody_Circular(40, (random.randint(1, 800), (random.randint(1, 400))) ) )

class Ground(ComponentEntity):
    def Build(self):
        self.AddComponent( StaticBody_Rectangular( Vec2(300, 25), Vec2(400, 500) ) )
        self.AddComponent( SpriteComponent( self.core.resourceManager.FetchTexture("media\\bar.png") ) )

    def Init(self):
        self.position = Vec2(400, 500)


# PROGRAM BEGINS

app = GameCore(True, "Crates Demo")

app.renderer.window.framerate_limit = 60

app.entityManager.AddEntity( Ground() )

for i in range(50):
    app.entityManager.AddEntity( Crate() )
    app.entityManager.AddEntity( Stone() )
    
app.Run()
