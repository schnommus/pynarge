from PyNARGE import *
import random
import math

appSize = Vec2(800, 600)

def OffscreenCondition( ent ):
    return ent.position.y > appSize.y+100

class Crate(ComponentEntity):
    def Build(self):
        self.AddComponent( SpriteComponent( self.core.resourceManager.FetchTexture("media\\crate.png") ) )
        self.AddComponent( RigidBody_Rectangular((16, 16), (random.randint(200,appSize.x-200), (random.randint(-400, -100))) ) )
        self.AddComponent( RespawnableComponent( OffscreenCondition ) )

class Stone(ComponentEntity):
    def Build(self):
        self.AddComponent( SpriteComponent( self.core.resourceManager.FetchTexture("media\\circle.png") ) )
        self.AddComponent( RigidBody_Circular(20, (random.randint(200, appSize.x-200), (random.randint(-400, -100))) ) )
        self.AddComponent( RespawnableComponent( OffscreenCondition ) )

class Ground(ComponentEntity):
    def Build(self):
        self.AddComponent( StaticBody_Rectangular( self.size/2, self.position, self.rotation ) )
        self.AddComponent( SpriteComponent( self.core.resourceManager.FetchTexture("media\\bar.png"), self.size ) )

# PROGRAM BEGINS

app = GameCore(False, "Crates Demo", appSize.x, appSize.y, False)

app.renderer.window.framerate_limit = 60

app.uiManager.AddEntity( FPS_Counter() )
app.uiManager.AddEntity( DefaultText("Click and drag mouse to manipulate objects", (appSize.x/2-200, appSize.y-65) ) )

app.entityManager.AddEntity( BackgroundImage( app.resourceManager.FetchTexture("media\\background.jpg") ) )
app.entityManager.AddEntity( Ground( Vec2(appSize.x/2, appSize.y-100), 0, Vec2(600, 20) ) )

for i in range(100):
    app.entityManager.AddEntity( Crate() )
    app.entityManager.AddEntity( Stone() )
    
app.Run()
