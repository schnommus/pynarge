from PyNARGE import *
import random
import math

appSize = Vec2(1920, 1080)

def OffscreenCondition( ent ):
    return ent.position.y > appSize.y+100

class PixelCrate(ComponentEntity):
    def Build(self):
        self.position.x = -200 # to hide the respawning frame before physics takes over
        self.AddComponent( PixelSpriteComponent( self.core.resourceManager.FetchTexture("media\\pixelcrate.png"), None, True ) )
        self.AddComponent( RigidBody_Rectangular((31, 31), (random.randint(200,appSize.x-200), (random.randint(-400, -100))) ) )
        self.AddComponent( RespawnableComponent( OffscreenCondition ) )

class PixelBall(ComponentEntity):
    def Build(self):
        self.position.x = -200
        self.AddComponent( PixelSpriteComponent( self.core.resourceManager.FetchTexture("media\\pixelball.png"), None, True ) )
        self.AddComponent( RigidBody_Circular(32, (random.randint(200, appSize.x-200), (random.randint(-400, -100))) ) )
        self.AddComponent( RespawnableComponent( OffscreenCondition ) )

class PixelMoon(ComponentEntity):
    def Build(self):
        self.AddComponent( PixelSpriteComponent( self.core.resourceManager.FetchTexture("media\\pixelmoon.png"), None, False ) )

    def Step(self):
        self.position = self.core.renderer.GetCameraPosition() + Vec2(-400,-100)

class PixelStar(ComponentEntity):
    def Build(self):
        self.velocity = random.randint(1, 3)
        self.myoffset = self.position
        self.AddComponent( PixelSpriteComponent( self.core.resourceManager.FetchTexture("media\\pixelstar.png"), None, False ) )

    def Step(self):
        self.position = (self.core.renderer.GetCameraPosition() + self.myoffset)/self.velocity


class PixelBar(ComponentEntity):
    def Build(self):
        self.AddComponent( StaticBody_Rectangular( self.size/2, self.position, self.rotation ) )
        self.AddComponent( PixelSpriteComponent( self.core.resourceManager.FetchTexture("media\\pixelbar.png"), None, False ) )

class CameraController(ComponentEntity):
    def Build(self):
        self.lastPosition = None
        self.currentPosition = None
        
    def Step(self):
        mouse = self.core.input.mouse
        if mouse.is_button_pressed( mouse.MIDDLE ):
            self.currentPosition = self.core.input.GetMousePositionUI()
            if not self.lastPosition ==  None:
                newPosition = self.core.renderer.GetCameraPosition() - (self.currentPosition-self.lastPosition)
                newPosition.y = newPosition.y if newPosition.y <= appSize.y/2 else appSize.y/2
                self.core.renderer.SetCameraPosition( newPosition )
            self.lastPosition = self.currentPosition
        else:
            self.lastPosition = None

class RespawningWaterParticle(PixelWaterParticle):
    def Build(self):
        # Must set entity's position THEN build particle so it knows where to spawn
        self.position = (random.randint(appSize.x/2-200, appSize.x/2+200), random.randint(-400, -100))
        PixelWaterParticle.Build(self)
        self.AddComponent( RespawnableComponent( OffscreenCondition ) )

# PROGRAM BEGINS

settings = Settings()
settings.window_title = "Retro Demo"
settings.display_size = appSize
settings.display_fps = True
settings.display_fullscreen = True
settings.enable_lmb_manipulation = True

app = GameCore(settings)

app.entityManager.AddEntity( CameraController() )

app.entityManager.AddEntity( PixelMoon( Vec2(300, 400) ) )

for i in range(150):
    app.entityManager.AddEntity( PixelStar( Vec2( random.randint(-3000, 3000), random.randint(-3000, 3000)) ) )

app.uiManager.AddEntity( DefaultPixelText("Click and drag mouse to manipulate", (appSize.x/2-324, appSize.y-64) ) )

app.entityManager.AddEntity( PixelBar( Vec2(appSize.x/2, appSize.y-97), 0, Vec2(600, 20) ) )
app.entityManager.AddEntity( PixelBar( Vec2(appSize.x/2+300, appSize.y-397), 90, Vec2(600, 20) ) )
app.entityManager.AddEntity( PixelBar( Vec2(appSize.x/2-300, appSize.y-397), 90, Vec2(600, 20) ) )


for i in range(120):
    app.entityManager.AddEntity( RespawningWaterParticle() )

for i in range(10):
    app.entityManager.AddEntity( PixelCrate() )
    if i % 4 == 0: app.entityManager.AddEntity( PixelBall() )

app.Run()
#import cProfile
#print cProfile.run("app.Run()", None, 'tottime')
