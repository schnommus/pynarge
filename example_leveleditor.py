from PyNARGE import *
import random
import math

appSize = Vec2(1920, 1080)

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

class Spawner(ComponentEntity):
    def PopulateTypes(self):
        self.possibleTypes = [Crate, Stone, WaterParticle, BigCrate, MetalCrate, GlassCrate]
        
        # Get an texture representation for each type
        self.possibleTypeTextures = []
        for t in self.possibleTypes:
            ent = self.core.entityManager.AddEntity( t() )
            self.possibleTypeTextures.append( ent.FetchComponent(SpriteComponent).sprite.texture )
            self.core.entityManager.RemoveEntity( ent )
        
    
    def Build(self):
        self.PopulateTypes()
        self.AddComponent( SpriteComponent( self.possibleTypeTextures[0], None, None, (207, 30) ) )
        self.AddComponent( TextComponent( "Will spawn: ", None, 40, Color(0, 0, 0) ) )
        self.currentType = 0
        self.hasSpawned = False
        self.hasChanged = False
        
    def Step(self):
        self.FetchComponent( TextComponent ).SetText("Will spawn:    (" + str(self.possibleTypes[self.currentType].__name__)+")")
        self.FetchComponent( SpriteComponent ).SetTexture( self.possibleTypeTextures[self.currentType], (32, 32) )
        
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


class Cannon(ComponentEntity):
    def Build(self):
        self.barrel = self.core.entityManager.AddEntity( CannonBarrel(self.position) )
        self.base = self.core.entityManager.AddEntity( CannonBase( (self.position.x, self.position.y-10) ) )
        self.hasShot = False
        
    def Step(self):
        self.barrel.position = (self.position.x, self.position.y-10)
        self.base.position = self.position

        keyboard = self.core.input.keyboard
        if keyboard.is_key_pressed( keyboard.LEFT ) or keyboard.is_key_pressed( keyboard.UP ):
            self.barrel.rotation += 25*self.core.time.GetDelta()
        if keyboard.is_key_pressed( keyboard.RIGHT ) or keyboard.is_key_pressed( keyboard.DOWN ):
            self.barrel.rotation -= 25*self.core.time.GetDelta()

        if keyboard.is_key_pressed( keyboard.SPACE ) and not self.hasShot:
            self.hasShot = True
            self.core.entityManager.AddEntity( CannonBall(self.position + Vec2(128*math.cos( (self.barrel.rotation*3.141)/180 ), -128*math.sin( (self.barrel.rotation*3.141)/180 ) ), self.barrel.rotation) )
            self.sound = Sound( self.core.resourceManager.FetchSound("media\cannon_shoot.wav") )
            self.sound.play()
            
        if not keyboard.is_key_pressed( keyboard.SPACE ):
            self.hasShot = False

class CannonBarrel(ComponentEntity):
    def Build(self):
        self.drawlayer = 80
        self.AddComponent( SpriteComponent( self.core.resourceManager.FetchTexture(r"media\cannon_barrel.png") ) )
        
class CannonBase(ComponentEntity):
    def Build(self):
        self.drawlayer=81
        self.AddComponent( SpriteComponent( self.core.resourceManager.FetchTexture(r"media\cannon_base.png") ) )
        self.AddComponent( StaticBody_Rectangular( (16, 16), self.position, self.rotation ) )

class CannonBall(ComponentEntity):
    def Build(self):
        self.drawlayer=50
        self.drawlayer=100
        self.AddComponent( SpriteComponent( self.core.resourceManager.FetchTexture(r"media\cannon_ball.png"), (24, 24) ) )
        self.body = self.AddComponent( RigidBody_Circular(12, self.position, density=12.0) ).body

    def Init(self):
        force = 100000
        self.body.ApplyForce( (force*math.cos( (self.rotation*3.141)/180 ), force*math.sin( (self.rotation*3.141)/180 )), self.body.GetWorldPoint( (0, 0) ), wake=True )
        self.body.bullet = True

    def OnCollision(self, other):
        if type(other) == Stone:
            self.sound = Sound( self.core.resourceManager.FetchSound("media\crate_hit.wav") )
            self.sound.play()
        
    

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

class BigCrate(ComponentEntity):
    def Build(self):
        self.AddComponent( SpriteComponent( self.core.resourceManager.FetchTexture(r"media\big_crate.png") ) )
        self.AddComponent( RigidBody_Rectangular((32, 32), self.position) )

class MetalCrate(ComponentEntity):
    def Build(self):
        self.AddComponent( SpriteComponent( self.core.resourceManager.FetchTexture(r"media\metal_crate.png") ) )
        self.AddComponent( RigidBody_Rectangular((64, 64), self.position, density=3.0) )

class GlassFragment(ComponentEntity):
    def Build(self):
        self.position.x += random.randint(-30, 30)
        self.position.y += random.randint(-30, 30)
        self.rotation = random.randint(0, 360)
        self.AddComponent( SpriteComponent( self.core.resourceManager.FetchTexture(r"media\glass_broken.png"), (40, 20) ) )
        self.body = self.AddComponent( RigidBody_Rectangular((20, 10), self.position, density=0.7) ).body
        
    def Init(self):
        force = 1000
        self.body.ApplyForce( (force*(random.random()-0.5), force*(random.random()-0.5)), self.body.GetWorldPoint( (0, 0) ), wake=True )
        self.body.bullet = True

class GlassCrate(ComponentEntity):
    def Build(self):
        self.AddComponent( SpriteComponent( self.core.resourceManager.FetchTexture(r"media\glass_crate.png") ) )
        self.AddComponent( RigidBody_Rectangular((32, 32), self.position, density=1.5) )
        self.dead = False

    def Step(self):
        if self.dead:
            self.core.entityManager.RemoveEntity(self)
            for i in range(4):
                self.core.entityManager.AddEntity( GlassFragment(self.position) )
                
    def OnCollision(self, other):
        if type(other) == CannonBall:
            self.dead = True

class Stone(ComponentEntity):
    def Build(self):
        self.AddComponent( SpriteComponent( self.core.resourceManager.FetchTexture(r"media\circle.png") ) )
        self.AddComponent( RigidBody_Circular(20, self.position) )
        
    def OnCollision(self, other):
        pass
        #if type(other) != Ground and type(other) != Stone:
        #    self.core.entityManager.RemoveEntity(other)

class Ground(ComponentEntity):
    def Build(self):
        self.AddComponent( StaticBody_Rectangular( self.size/2, self.position, self.rotation ) )
        self.AddComponent( SpriteComponent( self.core.resourceManager.FetchTexture(r"media\ground.png"), self.size ) )

if __name__=="__main__":

    settings = Settings()
    settings.window_title = "Level Editing Demo"
    settings.display_size = appSize
    settings.enable_lmb_manipulation = True
    settings.enable_rmb_destruction = True
    settings.display_fullscreen = True

    app = GameCore(settings)

    app.entityManager.AddEntity( Cannon( (100, appSize.y-128-32-128))  )
    app.entityManager.AddEntity( BigCrate( (132, appSize.y-128-32)) )
    app.entityManager.AddEntity( BigCrate( (68, appSize.y-128-32)) )
    app.entityManager.AddEntity( BigCrate( (100, appSize.y-128-32-64)) )

    text = """S - Spawn single item
    X - Spawn multiple items
    N - Change item to spawn
    LMB - Manipulate objects
    MMB - Move camera
    RMB - Delete objects

    Left/Right - Aim Cannon
    Space - Fire Cannon"""

    app.uiManager.AddEntity( DefaultText(text, (10, 90), Color(0, 0, 0) ) )

    app.entityManager.AddEntity( BackgroundImage( app.resourceManager.FetchTexture(r"media\background.jpg") ) )
    app.entityManager.AddEntity( CameraController() )
    spawner = app.uiManager.AddEntity( Spawner( (5, 30) ) )

    for i in range(20):
        app.entityManager.AddEntity( Ground( ((i-10)*361+appSize.x/2, appSize.y-64), 0, (361, 128) ) )

    for i in range(12):
        app.entityManager.AddEntity( Cloud() )

    from levelcode import *
    LoadLevel(app)

    app.Run()

    #for entity in app.entityManager.entities:
    #    if type(entity) in spawner.possibleTypes:
    #        print "app.entityManager.AddEntity(", type(entity).__name__, '(', entity.position, ',', entity.rotation, ',', entity.size, ") )"
