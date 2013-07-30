from PyNARGE import *
import random
import math

class Hydrogen(ComponentEntity):
    def Build(self):
        self.AddComponent( SpriteComponent( self.core.resourceManager.FetchTexture("media\hydrogen.png") ) )
        self.AddComponent( BrownianComponent() )
        self.AddComponent( VelocityComponent() )
        self.AddComponent( AttractedToComponent(None, 10000000) )
        self.grav = None
        
    def Init(self):
        self.position = Vec2(random.randint(0, self.core.renderer.GetWindowSize().x), random.randint(0, self.core.renderer.GetWindowSize().y))

    def SetGrav(self, target):
        self.grav = target

    def Step(self):
        if self.position.get_distance(self.core.input.GetMousePosition()) < 40:
            self.FetchComponent( BrownianComponent ).factor = 1000
        else:
            self.FetchComponent( BrownianComponent ).factor = 100

        if self.core.input.keyboard.is_key_pressed( self.core.input.keyboard.SPACE ):
            self.FetchComponent( AttractedToComponent ).SetTarget(self.grav)
        else:
            self.FetchComponent( AttractedToComponent ).SetTarget(None)

class Electron(ComponentEntity):
    def Build(self):
        self.AddComponent( SpriteComponent( self.core.resourceManager.FetchTexture("media\electron.png") ) )
        self.AddComponent( FollowComponent() )
        self.delta = float(random.randint(0, 12))/2
        
    def SetAtom(self, atom):
        self.FetchComponent( FollowComponent ).SetTarget(atom)

    def Step(self):
        self.FetchComponent( FollowComponent ).SetOffset(Vec2(math.cos(self.delta)*30, math.sin(self.delta)*30))
        self.delta += 10*self.core.time.GetDelta()

class HelperText(ComponentEntity):
    def Build(self):
        self.AddComponent( TextComponent("Mouse over particles to agitate them; space bar creates gravity") )
        self.position = (130, 550)

class GravityCenter(ComponentEntity):
    def Step(self):
        self.position = self.core.input.GetMousePosition()

# PROGRAM BEGINS

app = GameCore(True, "Hydrogen Demo")

grav = GravityCenter()
app.entityManager.AddEntity( grav )

for i in range(50):
    h = Hydrogen()
    app.entityManager.AddEntity( h )
    h.SetGrav(grav)
    e = Electron()
    app.entityManager.AddEntity( e )
    e.SetAtom(h) # called AFTER added to manager, otherwise 'follow' component won't have been built!
    
app.entityManager.AddEntity( HelperText() )

app.Run()
