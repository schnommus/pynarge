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
            self.core.entityManager.AddEntity( type(self)() ) # Spawn new object
            self.core.entityManager.RemoveEntity(self) # Destroy self

class WaterParticle(ComponentEntity):
    def __init__(self, shaderPass):
        ComponentEntity.__init__(self)
        self.shaderPass = shaderPass
        
    def Build(self):
        self.AddComponent( SpriteComponent( self.core.resourceManager.FetchTexture("media\\waterparticle.png"), (16, 16), self.shaderPass ) )
        self.AddComponent( RigidBody_Circular(6, (random.randint(200, appSize.x-200), (random.randint(-400, -100))), 0.0, 0.2 ) )

    def Step(self):
        if self.position.y > appSize.y+100: # If object is offscreen
            self.core.entityManager.AddEntity( type(self)(self.shaderPass) ) # Spawn new object
            self.core.entityManager.RemoveEntity(self) # Destroy self

class Ground(ComponentEntity):
    def __init__(self, size, position, angle):
        ComponentEntity.__init__(self)
        self._size = Vec2(size)
        self._position = Vec2(position)
        self._angle = float(angle)
        
    def Build(self):
        self.AddComponent( StaticBody_Rectangular( self._size/2, self._position, self._angle ) )
        self.AddComponent( SpriteComponent( self.core.resourceManager.FetchTexture("media\\bar.png"), self._size ) )

class HelperText(ComponentEntity):
    def Build(self):
        self.AddComponent( TextComponent("Click and drag mouse to manipulate objects") )
        self.position = (appSize.x/2-200, appSize.y-65)

class Background(ComponentEntity):
    def Build(self):
        self.AddComponent( SpriteComponent( self.core.resourceManager.FetchTexture("media\\background.jpg"), (appSize.x, appSize.y) ) )
        self.position = (appSize.x/2, appSize.y/2)
        
# PROGRAM BEGINS

app = GameCore(False, "Water Demo", appSize.x, appSize.y, False)

app.renderer.window.framerate_limit = 60

app.entityManager.AddEntity( Background() )
app.entityManager.AddEntity( HelperText() )

pixelate = app.renderer.AddShaderPass( ShaderPass( app.resourceManager.FetchShader("media\\shader\\pixelate.glsl") ) )
pixelate.SetTarget( app.renderer )

app.entityManager.AddEntity( Ground( (300, 20), (appSize.x/2+100, appSize.y/2+100), 45 ) )
app.entityManager.AddEntity( Ground( (300, 20), (appSize.x/2-100, appSize.y/2+100), -45 ) )

app.entityManager.AddEntity( Crate() )

app.entityManager.AddEntity( FPS_Counter() )


waterPass1 = app.renderer.AddShaderPass( ShaderPass( app.resourceManager.FetchShader("media\\shader\\water_pass1.glsl") ) )
waterPass2 = app.renderer.AddShaderPass( ShaderPass( app.resourceManager.FetchShader("media\\shader\\water_pass2.glsl") ) )
waterPass1.SetTarget( waterPass2 )
waterPass2.SetTarget( app.renderer )

for i in range(200):
    app.entityManager.AddEntity(WaterParticle(waterPass1))

app.Run()
