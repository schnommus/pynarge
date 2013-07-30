from pn_entitymanager import EntityManager
from pn_entity import Entity
from pn_utils import IdDispensor, Time
from pn_renderer import Renderer
from pn_resourcemanager import ResourceManager
from pn_input import Input
from pn_physics import PhysicsWorld

from pn_debug import FPS_Counter

class GameCore(object):
    def __init__(self, debugInfo=False, title="PyNARGE Window", size_x=800, size_y=600, fullscreen=False, antialiasing=False ):
        print "Initializing core engine components..."
        
        self.renderer = Renderer(self)
        self.renderer.Initialize(title, size_x, size_y, fullscreen, antialiasing)

        self.resourceManager = ResourceManager()
        self.input = Input(self)

        self.physicsWorld = PhysicsWorld(self)
        self.physicsWorld.Initialize()
        
        self.idDispensor = IdDispensor()
        self.uiManager = EntityManager(self)
        self.entityManager = EntityManager(self)

        self.time = Time()

        self.isRunning = False

        self.debugInfo = debugInfo

        if self.debugInfo:
            self.entityManager.AddEntity( FPS_Counter() )

    def Run(self):
        self.isRunning = True
        while self.isRunning:
            self.time.Tick()

            self.physicsWorld.Update()
            
            self.entityManager.UpdateEntities()
            
            self.entityManager.DrawEntities()
            
            self.renderer.Update()

        self.Cleanup()

    def Cleanup(self):
        print "Closing gracefully."

    def Quit(self):
        self.isRunning = False
        print "Core loop terminated."
