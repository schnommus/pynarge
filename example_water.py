from PyNARGE import *
import random
import math

appSize = Vec2(800, 600)

class Crate(ComponentEntity):
    def Build(self):
        self.AddComponent( SpriteComponent( self.core.resourceManager.FetchTexture("media\\crate.png") ) )
        self.AddComponent( RigidBody_Rectangular((16, 16), (appSize.x/2, -200) ) )
        
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
        self.AddComponent( RigidBody_Circular(6, (random.randint(appSize.x/2-200, appSize.x/2+200), (random.randint(-400, -100))), 0.0, 0.2 ) )

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


        
# PROGRAM BEGINS

app = GameCore(False, "Water Demo", appSize.x, appSize.y, False)

app.renderer.window.framerate_limit = 60

app.uiManager.AddEntity( FPS_Counter() )
app.uiManager.AddEntity( DefaultText("Click and drag mouse to manipulate objects", (appSize.x/2-200, appSize.y-65) ) )


app.entityManager.AddEntity( Ground( (100, 20), (appSize.x/2+150, appSize.y/2+100), 90 ) )
app.entityManager.AddEntity( Ground( (100, 20), (appSize.x/2-150, appSize.y/2+100), -90 ) )
app.entityManager.AddEntity( Ground( (300, 20), (appSize.x/2, appSize.y/2+150), 0 ) )


waterPass1 = app.renderer.AddShaderPass( ShaderPass( app.resourceManager.FetchShader("media\\shader\\water_pass1.glsl") ) )
waterPass2 = app.renderer.AddShaderPass( ShaderPass( app.resourceManager.FetchShader("media\\shader\\water_pass2.glsl") ) )
waterPass1.SetTarget( waterPass2 )
waterPass2.SetTarget( app.renderer )

waterPass1.SetParameter( "size_x", appSize.x )
waterPass1.SetParameter( "size_y", appSize.y )
waterPass2.SetParameter( "size_x", appSize.x )
waterPass2.SetParameter( "size_y", appSize.y )

for i in range(3):
    app.entityManager.AddEntity( Crate() )

for i in range(200):
    app.entityManager.AddEntity(WaterParticle(waterPass1))

app.entityManager.AddEntity( BackgroundImage( app.resourceManager.FetchTexture("media\\background.jpg") ) )

app.Run()
