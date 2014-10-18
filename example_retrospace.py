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
        self.AddComponent( RigidBody_Rectangular((31, 31), (random.randint(200,appSize.x-200), (random.randint(-200, 200))) ) )
        self.AddComponent( RespawnableComponent( OffscreenCondition ) )

class PixelBullet(ComponentEntity):
    def Build(self):
        self.AddComponent( PixelSpriteComponent( self.core.resourceManager.FetchTexture("media\\pixelbullet.png"), None, False ) )
        self.body = self.AddComponent( RigidBody_Circular(4, self.position, density=12.0) ).body

    def Init(self):
        force = 100000
        self.body.ApplyForce( (force*math.cos( (self.rotation*3.141)/180 ), force*math.sin( (self.rotation*3.141)/180 )), self.body.GetWorldPoint( (0, 0) ), wake=True )
        self.body.bullet = True

    def OnCollision(self, other):
        self.sound = Sound( self.core.resourceManager.FetchSound("media\dud.wav") )
        self.sound.volume = 50
        self.sound.play()
        self.core.entityManager.RemoveEntity( self )

class PixelShip(ComponentEntity):
    def Build(self):
        self.position.x = -200 # to hide the respawning frame before physics takes over
        self.AddComponent( PixelSpriteComponent( self.core.resourceManager.FetchTexture("media\\pixelship.png"), None, True ) )
        self.AddComponent( RigidBody_Rectangular((31, 31), (random.randint(200,appSize.x-200), (random.randint(-200, 200))) ) )
        self.AddComponent( RespawnableComponent( OffscreenCondition ) )
        self.hasShot = False
        self.sound2 = None

    def Step(self):
        self.core.renderer.SetCameraPosition( self.position )
        keyboard = self.core.input.keyboard
        vel = Vec2(0, 0)
        if keyboard.is_key_pressed(keyboard.A):
            vel.x += -1
        if keyboard.is_key_pressed(keyboard.D):
            vel.x += 1
        if keyboard.is_key_pressed(keyboard.W):
            vel.y += 1
        if keyboard.is_key_pressed(keyboard.S):
            vel.y += -1


        if keyboard.is_key_pressed(keyboard.SPACE)and not self.hasShot:
            self.hasShot = True
            self.rotation += 90
            self.core.entityManager.AddEntity( PixelBullet(self.position + Vec2(80*math.cos( (self.rotation*3.141)/180 ), -80*math.sin( (self.rotation*3.141)/180 ) ), self.rotation) )
            self.rotation -= 90
            self.sound = Sound( self.core.resourceManager.FetchSound("media\pew2.wav") )
            self.sound.play()

        if not keyboard.is_key_pressed( keyboard.SPACE ):
            self.hasShot = False

        
        if vel != Vec2(0, 0):
            self.FetchComponent( PixelSpriteComponent ).SetTexture( self.core.resourceManager.FetchTexture("media\\pixelshipfire.png"), None, True )
            self.FetchComponent( RigidBody_Rectangular ).body.angle = math.atan2(vel.y, vel.x)-3.14/2
            self.FetchComponent( RigidBody_Rectangular ).body.angularVelocity = 0
            if self.sound2 == None:
                self.sound2 = Sound( self.core.resourceManager.FetchSound("media\engines.wav") )
                self.sound2.play()
        else:
            self.sound2 = None
            self.FetchComponent( PixelSpriteComponent ).SetTexture( self.core.resourceManager.FetchTexture("media\\pixelship.png"), None, True )
        self.FetchComponent( RigidBody_Rectangular ).body.linearVelocity.x += vel.x
        self.FetchComponent( RigidBody_Rectangular ).body.linearVelocity.y += vel.y

class PixelBall(ComponentEntity):
    def Build(self):
        self.position.x = -200
        self.AddComponent( PixelSpriteComponent( self.core.resourceManager.FetchTexture("media\\pixelball.png"), None, True ) )
        self.AddComponent( RigidBody_Circular(32, (random.randint(200, appSize.x-200), (random.randint(-200, 200))) ) )
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
        pass
##        mouse = self.core.input.mouse
##        if mouse.is_button_pressed( mouse.MIDDLE ):
##            self.currentPosition = self.core.input.GetMousePositionUI()
##            if not self.lastPosition ==  None:
##                newPosition = self.core.renderer.GetCameraPosition() - (self.currentPosition-self.lastPosition)
##                newPosition.y = newPosition.y if newPosition.y <= appSize.y/2 else appSize.y/2
##                self.core.renderer.SetCameraPosition( newPosition )
##            self.lastPosition = self.currentPosition
##        else:
##            self.lastPosition = None

class RespawningWaterParticle(PixelWaterParticle):
    def Build(self):
        # Must set entity's position THEN build particle so it knows where to spawn
        self.position = (random.randint(appSize.x/2-200, appSize.x/2+200), random.randint(-200, 200))
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

app.uiManager.AddEntity( DefaultPixelText("WASD: Fire engines  -  SPACE: Shoot  -  MOUSE: Manipulate", (appSize.x/2-474, appSize.y-64) ) )

for i in range(6):
    app.entityManager.AddEntity( PixelBar( Vec2(appSize.x/2+(i-3)*600, 800), 0, Vec2(600, 20) ) )

for i in range(6):
    app.entityManager.AddEntity( PixelBar( Vec2(appSize.x/2+(i-3)*600, -300), 0, Vec2(600, 20) ) )

for i in range(3):
    app.entityManager.AddEntity( PixelBar( Vec2(appSize.x/2+(0-3)*600, appSize.y/2+(i-2)*600+300), 90, Vec2(600, 20) ) )

for i in range(3):
    app.entityManager.AddEntity( PixelBar( Vec2(appSize.x/2+(5-3)*600, appSize.y/2+(i-2)*600+300), 90, Vec2(600, 20) ) )

app.entityManager.AddEntity( PixelShip() )

for i in range(150):
    app.entityManager.AddEntity( RespawningWaterParticle() )

for i in range(30):
    app.entityManager.AddEntity( PixelCrate() )
    if i % 4 == 0: app.entityManager.AddEntity( PixelBall() )

app.physicsWorld.SetGravity( (0, 0) )

app.Run()
#import cProfile
#print cProfile.run("app.Run()", None, 'tottime')
