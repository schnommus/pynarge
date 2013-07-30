from Box2D import *
from pn_utils import Vec2

class PhysicsWorld(object):
    def __init__(self, core):
        self.core = core
    
    def Initialize(self):
        self.world = b2World(gravity=(0,-7))
        self.world.CreateStaticBody( position=(0,-10), shapes=b2PolygonShape(box=(50,10)) )
        self.timeStep = 1.0 / 60
        self.vel_iters, self.pos_iters = 6, 2

    def Update( self ):
        self.world.Step(self.timeStep, self.vel_iters, self.pos_iters)
        self.world.ClearForces()

    def GetWindowSize(self):
        return self.size

from pn_component import Component

class RigidBody(Component):
    def __init__( self, size=(1, 1), position=(0, 4) ):
        self.size = Vec2(size)
        self.position = Vec2(position)

    def Init(self):
        self.body = self.core.physicsWorld.world.CreateDynamicBody(position=self.position, fixtures=b2FixtureDef(
                            shape=b2CircleShape(radius=1),
                            density=1.0))

    def Step(self):
        print self.body.position.x, self.body.position.y
        self.entity.rotation = 180*self.body.angle/3.1416
        self.entity.position = Vec2( self.body.position.x*40+100, self.body.position.y*40)
        #self.entity.position.y = 400-self.entity.position.y
