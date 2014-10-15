from PyNARGE import *
import random
import math

appSize = Vec2(800, 600)

def OffscreenCondition( ent ):
    return ent.position.y > appSize.y+100

class PixelCrate(ComponentEntity):
    def Build(self):
        self.position.x = -200 # to hide the respawning frame before physics takes over
        self.AddComponent( PixelSpriteComponent( self.core.resourceManager.FetchTexture("media\\pixelcrate.png") ) )
        self.AddComponent( RigidBody_Rectangular((32, 32), (random.randint(200,appSize.x-200), (random.randint(-400, -100))) ) )
        self.AddComponent( RespawnableComponent( OffscreenCondition ) )

class PixelBall(ComponentEntity):
    def Build(self):
        self.position.x = -200
        self.AddComponent( PixelSpriteComponent( self.core.resourceManager.FetchTexture("media\\pixelball.png") ) )
        self.AddComponent( RigidBody_Circular(32, (random.randint(200, appSize.x-200), (random.randint(-400, -100))) ) )
        self.AddComponent( RespawnableComponent( OffscreenCondition ) )

class PixelBar(ComponentEntity):
    def Build(self):
        self.AddComponent( StaticBody_Rectangular( self.size/2, self.position, self.rotation ) )
        self.AddComponent( StaticPixelSpriteComponent( self.core.resourceManager.FetchTexture("media\\pixelbar.png"), self.size ) )

# PROGRAM BEGINS

settings = Settings()
settings.window_title = "Retro Demo"
settings.display_size = appSize
settings.enable_lmb_manipulation = True

app = GameCore(settings)

app.uiManager.AddEntity( DefaultPixelText("Click and drag mouse to manipulate", (appSize.x/2-324, appSize.y-64) ) )

app.entityManager.AddEntity( BackgroundImage( app.resourceManager.FetchTexture("media\\pixelbackground.png") ) )
app.entityManager.AddEntity( PixelBar( Vec2(appSize.x/2, appSize.y-100), 0, Vec2(600, 20) ) )

for i in range(10):
    app.entityManager.AddEntity( PixelCrate() )
    if i % 4 == 0: app.entityManager.AddEntity( PixelBall() )
    
app.Run()
