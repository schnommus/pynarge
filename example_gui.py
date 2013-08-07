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

class Stone(ComponentEntity):
    def Build(self):
        self.AddComponent( SpriteComponent( self.core.resourceManager.FetchTexture("media\\circle.png") ) )
        self.AddComponent( RigidBody_Circular(20, (random.randint(200, appSize.x-200), (random.randint(-400, -100))) ) )
        self.AddComponent( RespawnableComponent( OffscreenCondition ) )


class Ground(ComponentEntity):
    def Build(self):
        self.AddComponent( StaticBody_Rectangular( self.size/2, self.position, self.rotation ) )
        self.AddComponent( SpriteComponent( self.core.resourceManager.FetchTexture("media\\bar.png"), self.size ) )

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

def SpawnCube( core ):
    core.entityManager.AddEntity( Crate() )

def SpawnStone( core ):
    core.entityManager.AddEntity( Stone() )

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

dialog = app.uiManager.AddEntity( GUI_Dialog( "Groovy Spawnin' Dialog", (200, 70), (400, 500) ) )
app.uiManager.AddEntity( GUI_Button(dialog, "Spawn Cube", (84, 30), (10, 30), SpawnCube ) )
app.uiManager.AddEntity( GUI_Button(dialog, "Spawn Stone", (88, 30), (100, 30), SpawnStone ) )

app.entityManager.AddEntity(CameraController())

for i in range(15):
    app.entityManager.AddEntity( Crate() )

app.Run()
