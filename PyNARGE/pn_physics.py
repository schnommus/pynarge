from Box2D import *
from pn_utils import Vec2
from pn_component import Component

class PhysicsWorld(object):
    def __init__(self, core):
        self.core = core
    
    def Initialize(self, physicsScale=32):
        self.world = b2World(gravity=(0,-10))
        self.physicsScale=physicsScale
        self.timeStep = 1.0 / 60
        self.vel_iters, self.pos_iters = 6, 2

    def Update( self ):
        self.world.Step(self.timeStep, self.vel_iters, self.pos_iters)
        self.world.ClearForces()

    def GetWindowSize(self):
        return self.size

    def ToScreenCoords(self, coords):
        return Vec2(coords.x*self.physicsScale, 500-coords.y*self.physicsScale)
    
    def ToWorldCoords(self, coords):
        return Vec2(coords.x/self.physicsScale, (500-coords.y)/self.physicsScale)

class StaticBody_Rectangular(Component):
    def __init__( self, size=(1, 1), position=(0, 0) ):
        self.size = Vec2(size)
        self.position = Vec2(position)
        
    def Init(self):
        self.core.physicsWorld.world.CreateStaticBody( position=self.position, shapes=b2PolygonShape(box=self.size) )

class RigidBody_Rectangular(Component):
    def __init__( self, size=(1, 1), position=(0, 0) ):
        self.size = Vec2(size)
        self.position = Vec2(position)
        self.body = None

    def Init(self):
        self.body = self.core.physicsWorld.world.CreateDynamicBody(position=self.position)
        self.body.CreatePolygonFixture(box=self.size, density=1, friction=0.3)

    def Step(self):
        self.entity.rotation = 180*self.body.angle/3.1416
        self.entity.position = self.core.physicsWorld.ToScreenCoords(self.body.position)

class RigidBody_Circular(Component):
    def __init__( self, radius=1.0, position=(0, 0) ):
        self.radius = radius
        self.position = Vec2(position)
        self.body = None

    def Init(self):
        self.body = self.core.physicsWorld.world.CreateDynamicBody(position=self.position)
        self.body.CreateFixture(shape=b2CircleShape(radius=self.radius), density=1, friction=0.3)

    def Step(self):
        self.entity.rotation = 180*self.body.angle/3.1416
        self.entity.position = self.core.physicsWorld.ToScreenCoords(self.body.position)
