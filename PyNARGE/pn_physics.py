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

    def LocalToScreen(self, coords):
        return Vec2(float(coords.x)*self.physicsScale, float(coords.y)*self.physicsScale)

    def LocalToWorld(self, coords):
        return Vec2(float(coords.x)/self.physicsScale, float(coords.y)/self.physicsScale)

    def GlobalToScreen(self, coords):
        return Vec2(float(coords.x)*self.physicsScale+self.core.renderer.window.size.x/2, self.core.renderer.window.size.y/2-float(coords.y)*self.physicsScale)
    
    def GlobalToWorld(self, coords):
        return Vec2((float(coords.x)-self.core.renderer.window.size.x/2)/self.physicsScale, (self.core.renderer.window.size.y/2-float(coords.y))/self.physicsScale)

class StaticBody_Rectangular(Component):
    def __init__( self, size, position=(0,0) ):
        self.size = Vec2(size)
        self.position = Vec2(position)
        
    def Init(self):
        self.size = self.core.physicsWorld.LocalToWorld(self.size)
        self.position = self.core.physicsWorld.GlobalToWorld(self.position)
        print self.size, self.position
        b=self.core.physicsWorld.world.CreateStaticBody( position=self.position, shapes=b2PolygonShape(box=self.size) )

class RigidBody_Rectangular(Component):
    def __init__( self, size, position=(0,0) ):
        self.size = Vec2(size)
        self.position = Vec2(position)
        self.body = None

    def Init(self):
        self.size = self.core.physicsWorld.LocalToWorld(self.size)
        self.position = self.core.physicsWorld.GlobalToWorld(self.position)
        self.body = self.core.physicsWorld.world.CreateDynamicBody(position=self.position)
        self.body.CreatePolygonFixture(box=self.size, density=1, friction=0.3)

    def Step(self):
        self.entity.rotation = 180*self.body.angle/3.1416
        self.entity.position = self.core.physicsWorld.GlobalToScreen(self.body.position)

class RigidBody_Circular(Component):
    def __init__( self, radius, position=(0,0) ):
        self.radius = float(radius)
        self.position = Vec2(position)
        self.body = None

    def Init(self):
        self.radius /= self.core.physicsWorld.physicsScale
        self.position = self.core.physicsWorld.GlobalToWorld(self.position)
        self.body = self.core.physicsWorld.world.CreateDynamicBody(position=self.position)
        self.body.CreateFixture(shape=b2CircleShape(radius=self.radius), density=1, friction=0.3)

    def Step(self):
        self.entity.rotation = 180*self.body.angle/3.1416
        self.entity.position = self.core.physicsWorld.GlobalToScreen(self.body.position)
