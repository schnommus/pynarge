from PyNARGE import *
import random
import math

appSize = Vec2(1024, 768)

class CameraController(ComponentEntity):
    def Build(self):
        self.lastPosition = None
        self.currentPosition = None
        
    def Step(self):
        keyboard = self.core.input.keyboard
        mouse = self.core.input.mouse

        if keyboard.is_key_pressed( keyboard.EQUAL ):
            self.core.renderer.cameraView.zoom(1.0+0.1*self.core.time.GetDelta())
        
        if mouse.is_button_pressed( mouse.MIDDLE ):
            self.currentPosition = self.core.input.GetMousePositionUI()
            if not self.lastPosition ==  None:
                newPosition = self.core.renderer.GetCameraPosition() - (self.currentPosition-self.lastPosition)
                newPosition.y = newPosition.y if newPosition.y <= appSize.y/2 else appSize.y/2
                self.core.renderer.SetCameraPosition( newPosition )
            self.lastPosition = self.currentPosition
        else:
            self.lastPosition = None

class Spawner(ComponentEntity):
    def Build(self):
        self.AddComponent( TextComponent( "Will spawn: ", None, 40 ) )
        self.possibleTypes = [Crate, Stone, WaterParticle]
        self.currentType = 0
        self.hasSpawned = False
        self.hasChanged = False
        
    def Step(self):
        self.FetchComponent( TextComponent ).SetText("Will spawn: " + str(self.possibleTypes[self.currentType].__name__))
        
        mouse = self.core.input.mouse
        keyboard = self.core.input.keyboard
        currentPosition = self.core.input.GetMousePosition()

        if keyboard.is_key_pressed(keyboard.N): # Next item
            if not self.hasChanged:
                self.currentType += 1
                if self.currentType == len(self.possibleTypes):
                    self.currentType = 0
                self.hasChanged = True
        else:
            self.hasChanged = False
        
        if keyboard.is_key_pressed(keyboard.S): # Single spawn
            if not self.hasSpawned:
                app.entityManager.AddEntity( self.possibleTypes[self.currentType]( currentPosition + Vec2(random.random(), random.random()) ) )
            self.hasSpawned = True
        else:
            self.hasSpawned = False

        if keyboard.is_key_pressed(keyboard.X): # Multi spawn
            app.entityManager.AddEntity( self.possibleTypes[self.currentType]( currentPosition + Vec2(random.random(), random.random()) ) )


class Cloud(ComponentEntity):
    def Build(self):
        self.drawlayer = -99
        self.speed = 10+random.random()*8
        self.AddComponent( SpriteComponent( self.core.resourceManager.FetchTexture(r"media\cloud.png"), (random.randint(200, 300), random.randint(100, 200)) ) )
        self.position = Vec2( ((random.random()-0.5)*361*20), 50+random.randint(1, 250) )
    def Step(self):
        self.position.x += self.speed*self.core.time.GetDelta()
        if self.position.x > 361*10:
            self.position.x = -361*10

class Crate(ComponentEntity):
    def Build(self):
        self.AddComponent( SpriteComponent( self.core.resourceManager.FetchTexture(r"media\crate.png") ) )
        self.AddComponent( RigidBody_Rectangular((16, 16), self.position) )

class Stone(ComponentEntity):
    def Build(self):
        self.AddComponent( SpriteComponent( self.core.resourceManager.FetchTexture(r"media\circle.png") ) )
        self.AddComponent( RigidBody_Circular(20, self.position) )
        
    def OnCollision(self, other):
        if type(other) != Ground and type(other) != Stone:
            self.core.entityManager.RemoveEntity(other)

class Ground(ComponentEntity):
    def Build(self):
        self.AddComponent( StaticBody_Rectangular( self.size/2, self.position, self.rotation ) )
        self.AddComponent( SpriteComponent( self.core.resourceManager.FetchTexture(r"media\ground.png"), self.size ) )

app = GameCore(False, "Level Editing Demo", appSize.x, appSize.y, False)

app.renderer.window.framerate_limit = 60

app.uiManager.AddEntity( FPS_Counter() )
app.uiManager.AddEntity( DefaultText("S - Spawn single item\nX - Spawn multiple items\nN - Change item to spawn\nLMB - Manipulate objects\nMMB - Move camera\nRMB - Delete objects", (10, 90) ) )

app.entityManager.AddEntity( BackgroundImage( app.resourceManager.FetchTexture(r"media\background.jpg") ) )
app.entityManager.AddEntity( CameraController() )
app.uiManager.AddEntity( Spawner( (0, 30) ) )

for i in range(20):
    app.entityManager.AddEntity( Ground( ((i-10)*361+appSize.x/2, appSize.y-64), 0, (361, 128) ) )

for i in range(12):
    app.entityManager.AddEntity( Cloud() )

app.Run()
