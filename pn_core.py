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
    
x = GameCore()
x.entityManager.AddEntity(FPS_Counter())
x.Run()
