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
                self.core.renderer.SetCameraPosition( newPosition )
            self.lastPosition = self.currentPosition
        else:
            self.lastPosition = None

class SmoothCameraController(ComponentEntity):
    def Build(self):
        self.target = None;

    def SetTarget(self, target):
        self.target = target
    
    def Step(self):
        if self.target and not self.core.input.mouse.is_button_pressed( self.core.input.mouse.MIDDLE ):
            diff = (self.target.position-self.core.renderer.GetCameraPosition())*self.core.time.GetDelta()*5
            self.core.renderer.SetCameraPosition( self.core.renderer.GetCameraPosition()+diff )
            
            diff2 = (int(self.target.rotation)%360-int(self.core.renderer.cameraView.rotation)%360)*self.core.time.GetDelta()*5
            self.core.renderer.cameraView.rotation += diff2

class NiceText( ComponentEntity ):
    def __init__(self, text, position, size, color = Color.WHITE, angle=0.0 ):
        ComponentEntity.__init__(self)
        self.text = text
        self.position = position
        self.color = color
        self.size = size
        self.weight = 0.0
        self.rotation = angle
        self.active = False

    def SetActive(self, active):
        self.active = active
    
    def Build(self):
        self.AddComponent( TextComponent(self.text, None, self.size, self.color) )

    def Draw(self):
        self.FetchComponent( TextComponent ).color = Color( 255, 255, 255, 255-(1+math.cos(self.weight))/2*255 )
        if self.weight < 3.0 and self.active:
            self.weight += self.core.time.GetDelta()*4
        else:
            if self.weight > 1.0:
                self.weight -= self.core.time.GetDelta()*4
        if self.weight > 0:
            self.FetchComponent( TextComponent ).scale = 1+(1+math.cos(self.weight))/10
            self.FetchComponent( TextComponent ).ReCenter()


class PresentationController( ComponentEntity ):
    def Build(self):
        app.entityManager.AddEntity( BackgroundImage( app.resourceManager.FetchTexture("media\\blueprint.jpg") ) )
        self.controller = self.core.entityManager.AddEntity(SmoothCameraController())
        self.core.entityManager.AddEntity(CameraController())

        self.frames = []

        self.frames.append( self.core.entityManager.AddEntity( NiceText("Reality", (0, 0), 200, Color(0, 0, 0, 0) ) ) )
        self.frames.append( self.core.entityManager.AddEntity( NiceText("Time to circumvent.", (0, 200), 60, Color(0, 0, 0, 0), 0 ) ) )
        self.frames.append( self.core.entityManager.AddEntity( NiceText("But how?!", (30, 200), 80, Color(0, 0, 0, 0), 40 ) ) )
        self.frames.append( self.core.entityManager.AddEntity( NiceText("Well.", (0, 600), 400, Color(0, 0, 0, 0), 80 ) ) )
        self.frames.append( self.core.entityManager.AddEntity( NiceText("If we take a nuke...", (0, 1300), 150, Color(0, 0, 0, 0), 0 ) ) )
        self.frames.append( self.core.entityManager.AddEntity( NiceText("BLOW SHIT UP", (400, 1300), 150, Color(0, 0, 0, 0), -30 ) ) )
        self.frames.append( self.core.entityManager.AddEntity( NiceText("Then say goodbye", (600, 1300), 150, Color(0, 0, 0, 0), -30 ) ) )
        self.frames.append( self.core.entityManager.AddEntity( NiceText("Then we're done.", (900, 1300), 100, Color(0, 0, 0, 0), -45 ) ) )

        self.current_frame = 0
        
        self.SetFrame(0)
        
        self.controller.SetTarget( self.frames[self.current_frame] )

        self.leftdown = False
        self.rightdown = False

    def SetFrame(self, frame):
        print frame
        self.frames[self.current_frame].SetActive(False)
        
        self.current_frame = frame
        
        if self.current_frame == len(self.frames):
            self.current_frame = len(self.frames)-1
        if self.current_frame < 0:
            self.current_frame = 0

        self.frames[self.current_frame].SetActive(True)
    
    def Step(self):
        self.controller.SetTarget( self.frames[self.current_frame] )

        keyboard = self.core.input.keyboard

        if keyboard.is_key_pressed(keyboard.RIGHT):
            if not self.rightdown:
                self.SetFrame(self.current_frame + 1) ; self.rightdown = True
        else: self.rightdown = False

        if keyboard.is_key_pressed(keyboard.LEFT):
            if not self.leftdown:
                self.SetFrame(self.current_frame - 1) ; self.leftdown = True
        else: self.leftdown = False
        
        

# PROGRAM BEGINS
settings = Settings()
settings.limit_framerate = False
settings.window_title = "Present"
settings.display_size = appSize
settings.display_fullscreen = True
settings.enable_lmb_manipulation = True

app = GameCore(settings)

app.entityManager.AddEntity( PresentationController() )

app.Run()
