from PyNARGE import *
import random
import math

class Crate(ComponentEntity):
    def Build(self):
        self.AddComponent( SpriteComponent( self.core.resourceManager.FetchTexture("media\circle.png") ) )
        self.AddComponent( RigidBody((1, 1), (random.randint(1, 100)/5, 4) ) )

# PROGRAM BEGINS

app = GameCore(True, "Crates Demo")

app.renderer.window.framerate_limit = 60

for i in range(10):
    app.entityManager.AddEntity( Crate() )
    
app.Run()
