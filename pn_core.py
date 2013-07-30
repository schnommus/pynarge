from pn_entitymanager import EntityManager
from pn_entity import Entity
from pn_utils import IdDispensor, Time
from pn_renderer import Renderer
from pn_resourcemanager import ResourceManager

from pn_debug import FPS_Counter

class GameCore(object):
    def __init__(self):
        print "Initializing core engine components..."
        
        self.renderer = Renderer(self)
        self.renderer.Initialize()

        self.resourceManager = ResourceManager()
        
        self.idDispensor = IdDispensor()
        self.uiManager = EntityManager(self)
        self.entityManager = EntityManager(self)

        self.time = Time()

        self.isRunning = False

        self.debugInfo = True

        if self.debugInfo:
            self.entityManager.AddEntity( FPS_Counter() )

    def Run(self):
        self.isRunning = True
        while self.isRunning:
            self.time.Tick()
            
            self.entityManager.UpdateEntities()
            
            self.entityManager.DrawEntities()
            
            self.renderer.Update()

        self.Cleanup()

    def Cleanup(self):
        print "Closing gracefully."

    def Quit(self):
        self.isRunning = False
        print "Core loop terminated."

from pn_componententity import ComponentEntity
from pn_standardcomponents import TextComponent, BrownianComponent
from pn_utils import Vec2
import random

class HelloText(ComponentEntity):
    def Build(self):
        self.AddComponent( TextComponent("Hello") )
        self.AddComponent( BrownianComponent() )
    def Init(self):
        self.position = Vec2(random.randint(1, 500), random.randint(1, 500))

x = GameCore()
for i in range(100):
    x.entityManager.AddEntity( HelloText() )
x.Run()
