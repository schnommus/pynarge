from PyNARGE import *
import random
import math

appSize = Vec2(800, 600)

def OffscreenCondition( ent ):
    return ent.position.y > appSize.y+100

class Crate(ComponentEntity):
    def Build(self):
        self.AddComponent( SpriteComponent( self.core.resourceManager.FetchTexture("media\\crate.png") ) )
        self.AddComponent( RigidBody_Rectangular((16, 16), (appSize.x/2, -200) ) )
        self.AddComponent( RespawnableComponent( OffscreenCondition ) )

class RespawningWaterParticle(WaterParticle):
    def Build(self):
        # Must set entity's position THEN build particle so it knows where to spawn
        self.position = (random.randint(appSize.x/2-200, appSize.x/2+200), random.randint(-400, -100))
        WaterParticle.Build(self)
        self.AddComponent( RespawnableComponent( OffscreenCondition ) )

class Ground(ComponentEntity):
    def Build(self):
        self.AddComponent( StaticBody_Rectangular( self.size/2, self.position, self.rotation ) )
        self.AddComponent( SpriteComponent( self.core.resourceManager.FetchTexture("media\\bar.png"), self.size ) )

        
# PROGRAM BEGINS
settings = Settings()
settings.window_title = "Water Demo"
settings.display_size = appSize
settings.enable_lmb_manipulation = True

app = GameCore(settings)

app.uiManager.AddEntity( DefaultText("Click and drag mouse to manipulate objects", (appSize.x/2-200, appSize.y-65) ) )

app.entityManager.AddEntity( BackgroundImage( app.resourceManager.FetchTexture("media\\background.jpg") ) )

app.entityManager.AddEntity( Ground( (appSize.x/2+150, appSize.y/2+100), 90, (100, 20) ) )
app.entityManager.AddEntity( Ground( (appSize.x/2-150, appSize.y/2+100), -90, (100, 20) ) )
app.entityManager.AddEntity( Ground( (appSize.x/2, appSize.y/2+150), 0, (300, 20) ) )

for i in range(3):
    app.entityManager.AddEntity( Crate() )

for i in range(200):
    app.entityManager.AddEntity( RespawningWaterParticle() )

app.Run()
