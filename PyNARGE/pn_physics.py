from Box2D import *
from pn_utils import Vec2
from pn_component import Component

class PhysicsWorld(object):
    def __init__(self, core):
        self.core = core
        self.mouseJoint = None
    
    def Initialize(self, physicsScale=32):
        self.world = b2World(gravity=(0,-10),contactListener=CollisionListener(self.core))
        self.physicsScale=physicsScale
        self.timeStep = 1.0 / 60
        self.vel_iters, self.pos_iters = 6, 2

    def Update( self ):
        self.world.Step(self.timeStep, self.vel_iters, self.pos_iters)
        self.world.ClearForces()
        
        self.DoMouseQueries()
        self.Debug_ProcessMouseJoints()

    def GetEntityWithBody(self, body):
        return body.userData
    
    def DoMouseQueries(self):
        self.deleteWithRMB = True
        mouse = self.core.input.mouse
        p = self.GlobalToWorld( self.core.input.GetMousePosition() )
        aabb = b2AABB(lowerBound=p-(0.001, 0.001), upperBound=p+(0.001, 0.001))
        query = fwQueryCallback(p)
        self.world.QueryAABB(query, aabb)
        if query.fixture:
            ent = self.GetEntityWithBody(query.fixture.body)
            if( ent == None ):
                return
            ent.OnMouseOver()
            if self.deleteWithRMB and mouse.is_button_pressed( mouse.RIGHT ):
                self.core.entityManager.RemoveEntity(ent)
    
    def Debug_ProcessMouseJoints( self ):
        mouse = self.core.input.mouse
        p = self.GlobalToWorld( self.core.input.GetMousePosition() )
        
        if mouse.is_button_pressed( mouse.LEFT ):
            if self.mouseJoint != None:
                self.mouseJoint.target = p
                return

            aabb = b2AABB(lowerBound=p-(0.001, 0.001), upperBound=p+(0.001, 0.001))

            query = fwQueryCallback(p)
            self.world.QueryAABB(query, aabb)
            
            if query.fixture:
                body = query.fixture.body
                self.mouseJoint = self.world.CreateMouseJoint(
                        bodyA=self.world.CreateStaticBody(),
                        bodyB=body, 
                        target=p,
                        maxForce=1000.0*body.mass)
                body.awake = True

        else:
            if self.mouseJoint:
                self.world.DestroyJoint(self.mouseJoint)
                self.mouseJoint = None
        
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

class CollisionListener(b2ContactListener):
    def __init__(self, core):
        b2ContactListener.__init__(self)
        self.core = core
    def BeginContact(self, contact):
        ent1 = self.core.physicsWorld.GetEntityWithBody(contact.fixtureA.body)
        ent2 = self.core.physicsWorld.GetEntityWithBody(contact.fixtureB.body)
        ent1.OnCollision(ent2)
        ent2.OnCollision(ent1)
        


# Used for mouse joint debugging
class fwQueryCallback(b2QueryCallback):
    def __init__(self, p): 
        super(fwQueryCallback, self).__init__()
        self.point = p
        self.fixture = None

    def ReportFixture(self, fixture):
        body = fixture.body
        if body.type == b2_dynamicBody:
            inside=fixture.TestPoint(self.point)
            if inside:
                self.fixture=fixture
                # We found the object, so stop the query
                return False
        # Continue the query
        return True

# BEGIN BODY DEFINITIONS

class PhysicsComponent(Component):
    pass

class StaticBody_Rectangular(PhysicsComponent):
    def __init__( self, size, position=(0,0), angle=0.0 ):
        self.size = Vec2(size)
        self.position = Vec2(position)
        self.angledeg = angle
        self.anglerad = 3.141*float(angle)/180.0
        
    def Init(self):
        self.entity.position = self.position
        self.entity.rotation = self.angledeg
        self.size = self.core.physicsWorld.LocalToWorld(self.size)
        self.position = self.core.physicsWorld.GlobalToWorld(self.position)
        self.entity.body=self.core.physicsWorld.world.CreateStaticBody( position=self.position, angle=self.anglerad, shapes=b2PolygonShape(box=self.size) )
        self.entity.body.userData = self.entity
        

class RigidBody_Rectangular(PhysicsComponent):
    def __init__( self, size, position=(0,0), friction=0.3, density=1.0 ):
        self.size = Vec2(size)
        self.position = Vec2(position)
        self.body = None
        self.friction = friction
        self.density = density

    def Init(self):
        self.size = self.core.physicsWorld.LocalToWorld(self.size)
        self.position = self.core.physicsWorld.GlobalToWorld(self.position)
        self.body = self.core.physicsWorld.world.CreateDynamicBody(position=self.position)
        self.body.CreatePolygonFixture(box=self.size, density=self.density, friction=self.friction)
        self.entity.body = self.body
        self.entity.body.userData = self.entity

    def Step(self):
        self.entity.rotation = 180*self.body.angle/3.1416
        self.entity.position = self.core.physicsWorld.GlobalToScreen(self.body.position)

    def Destroy(self):
        self.core.physicsWorld.world.DestroyBody(self.body)

class RigidBody_Circular(PhysicsComponent):
    def __init__( self, radius, position=(0,0), friction=0.3, density=1.0 ):
        self.radius = float(radius)
        self.position = Vec2(position)
        self.body = None
        self.friction = friction
        self.density = density

    def Init(self):
        self.radius /= self.core.physicsWorld.physicsScale
        self.position = self.core.physicsWorld.GlobalToWorld(self.position)
        self.body = self.core.physicsWorld.world.CreateDynamicBody(position=self.position)
        self.body.CreateFixture(shape=b2CircleShape(radius=self.radius), density=self.density, friction=self.friction)
        self.entity.body = self.body
        self.entity.body.userData = self.entity

    def Step(self):
        self.entity.rotation = 180*self.body.angle/3.1416
        self.entity.position = self.core.physicsWorld.GlobalToScreen(self.body.position)

    def Destroy(self):
        self.core.physicsWorld.world.DestroyBody(self.body)
