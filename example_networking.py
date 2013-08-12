from PyNARGE import *
import random
import math

import sys
##
##def trace(frame, event, arg):
##    print "%s, %s:%d" % (event, frame.f_code.co_filename, frame.f_lineno)
##    return trace
##
##sys.settrace(trace)

appSize = Vec2(800, 600)

def OffscreenCondition( ent ):
    return ent.position.y > appSize.y+100

class Crate(ComponentEntity):
    def Build(self):
        self.AddComponent( SpriteComponent( self.core.resourceManager.FetchTexture("media\\crate.png") ) )
        self.AddComponent( RigidBody_Rectangular((16, 16), (random.randint(200,appSize.x-200), (random.randint(-400, -100))) ) )
        self.AddComponent( RespawnableComponent( OffscreenCondition ) )
        self.networked = True

class MouseVisualizer(ComponentEntity):
    def __init__(self, index):
        ComponentEntity.__init__(self)
        self.index = index
    
    def Build(self):
        self.AddComponent( SpriteComponent( self.core.resourceManager.FetchTexture("media\\client.png"), None, None, (20, 7) ) )
        self.drawlayer = 100
        
    def Step(self):
        if len(self.core.networking.clients) > self.index:
            self.position = self.core.networking.clients[self.index].mouse_position
        else:
            self.position = (10000, 10000)

        
class Stone(ComponentEntity):
    def Build(self):
        self.AddComponent( SpriteComponent( self.core.resourceManager.FetchTexture("media\\circle.png") ) )
        self.AddComponent( RigidBody_Circular(20, (random.randint(200, appSize.x-200), (random.randint(-400, -100))) ) )
        self.AddComponent( RespawnableComponent( OffscreenCondition ) )
        self.networked = True

class BigCrate(ComponentEntity):
    def Build(self):
        self.AddComponent( SpriteComponent( self.core.resourceManager.FetchTexture(r"media\big_crate.png") ) )
        self.AddComponent( RigidBody_Rectangular((32, 32), self.position) )
        self.networked = True

class MetalCrate(ComponentEntity):
    def Build(self):
        self.AddComponent( SpriteComponent( self.core.resourceManager.FetchTexture(r"media\metal_crate.png") ) )
        self.AddComponent( RigidBody_Rectangular((64, 64), self.position, density=3.0) )
        self.networked = True

class Ground(ComponentEntity):
    def Build(self):
        self.AddComponent( StaticBody_Rectangular( self.size/2, self.position, self.rotation ) )
        self.AddComponent( SpriteComponent( self.core.resourceManager.FetchTexture("media\\bar.png"), self.size ) )

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

class Ground(ComponentEntity):
    def Build(self):
        self.AddComponent( StaticBody_Rectangular( self.size/2, self.position, self.rotation ) )
        self.AddComponent( SpriteComponent( self.core.resourceManager.FetchTexture(r"media\ground.png"), self.size ) )

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

def SpawnStuff(app):
    app.uiManager.Clean()
    app.entityManager.Clean()

    if app.networking.is_server:
        for i in range(3):
            app.entityManager.AddEntity( Crate() )
            app.entityManager.AddEntity( Crate() )
            app.entityManager.AddEntity( Crate() )
            app.entityManager.AddEntity( Crate() )
            app.entityManager.AddEntity( Crate() )
            app.entityManager.AddEntity( Crate() )
            app.entityManager.AddEntity( Crate() )
            app.entityManager.AddEntity( Crate() )
            app.entityManager.AddEntity( Crate() )
            app.entityManager.AddEntity( Crate() )
            app.entityManager.AddEntity( Crate() )
            app.entityManager.AddEntity( Crate() )
            app.entityManager.AddEntity( Stone() )
            app.entityManager.AddEntity( BigCrate() )
            app.entityManager.AddEntity( MetalCrate() )

        app.entityManager.AddEntity( MouseVisualizer(0) )
        app.entityManager.AddEntity( MouseVisualizer(1) )
        app.entityManager.AddEntity( MouseVisualizer(2) )
        app.entityManager.AddEntity( MouseVisualizer(3) )

    else:
        app.entityManager.RegisterType( Crate )
        app.entityManager.RegisterType( Stone )
        app.entityManager.RegisterType( BigCrate )
        app.entityManager.RegisterType( MetalCrate )

    app.entityManager.AddEntity( BackgroundImage( app.resourceManager.FetchTexture("media\\background.jpg") ) )
    
    app.entityManager.AddEntity( Ground( Vec2(appSize.x/2, appSize.y-100), 0, Vec2(600, 20) ) )
    app.entityManager.AddEntity( CameraController() )

    for i in range(20):
        app.entityManager.AddEntity( Ground( ((i-10)*361+appSize.x/2, appSize.y-64), 0, (361, 128) ) )

    for i in range(12):
        app.entityManager.AddEntity( Cloud() )

def ClientMode(app):
    app.settings.enable_lmb_manipulation = True
    
    try:
        app.networking.InitializeAsClient('127.0.0.1')
    except:
        ConnectionErrorScreen(app)
        return

    app.networking.on_disconnected = ConnectionErrorScreen
    
    SpawnStuff(app)
    app.uiManager.AddEntity( DefaultText("CLIENT: Click and drag mouse to manipulate objects", (appSize.x/2-200, appSize.y-65) ) )

def ServerMode(app):
    app.settings.enable_lmb_manipulation = False
    app.networking.InitializeAsServer()
    SpawnStuff(app)
    app.uiManager.AddEntity( DefaultText("SERVER: Watch clients move objects around", (appSize.x/2-200, appSize.y-65) ) )


def StartScreen(app):
    app.uiManager.Clean()

    dialog = app.uiManager.AddEntity( GUI_Dialog( "Select networking mode", (200, 70), (300, 250) ) )
    app.uiManager.AddEntity( GUI_Button(dialog, "Client mode", (84, 30), (10, 30), ClientMode ) )
    app.uiManager.AddEntity( GUI_Button(dialog, "Server mode", (88, 30), (100, 30), ServerMode ) )

def ConnectionErrorScreen(app):
    app.uiManager.Clean()
    dialog = app.uiManager.AddEntity( GUI_Dialog( "Connection error!", (200, 70), (300, 250) ) )
    app.uiManager.AddEntity( GUI_Button(dialog, "Okay :(", (84, 30), (10, 30), StartScreen ) )
    
    
# PROGRAM BEGINS

settings = Settings()
settings.window_title = "Crates Demo"
settings.display_size = appSize

app = GameCore(settings)

app.entityManager.AddEntity( BackgroundImage( app.resourceManager.FetchTexture("media\\background.jpg") ) )

StartScreen(app)

app.Run()
