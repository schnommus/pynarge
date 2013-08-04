from pn_entitymanager import EntityManager
from pn_entity import Entity
from pn_utils import IdDispensor, Time
from pn_renderer import Renderer
from pn_resourcemanager import ResourceManager
from pn_input import Input
from pn_physics import PhysicsWorld
from pn_engineshaders import EngineShaders
from pn_debug import FPS_Counter
from pn_settings import Settings

class GameCore(object):
    def __init__(self, settings = Settings() ):
        print "Initializing core engine components..."

        self.settings = settings
        
        self.renderer = Renderer(self)
        self.renderer.Initialize(settings.window_title, settings.display_size.x, settings.display_size.y, settings.display_fullscreen, settings.antialiasing)

        self.resourceManager = ResourceManager()
        self.input = Input(self)

        self.engineShaders = EngineShaders(self)

        self.physicsWorld = PhysicsWorld(self)
        self.physicsWorld.Initialize()
        
        self.idDispensor = IdDispensor()
        self.uiManager = EntityManager(self)
        self.entityManager = EntityManager(self)

        self.time = Time()

        self.isRunning = False

        if self.settings.display_fps:
            self.uiManager.AddEntity( FPS_Counter() )

    def Run(self):
        self.renderer.AlignShaders()
        
        self.isRunning = True
        while self.isRunning:
            self.time.Tick()

            self.physicsWorld.Update()
            
            self.entityManager.UpdateEntities()

            self.uiManager.UpdateEntities()

            self.renderer.SetViewToCamera()
            
            self.entityManager.DrawEntities()

            self.renderer.DrawShaders()

            self.renderer.SetViewToUI()

            self.uiManager.DrawEntities()
            
            self.renderer.Update()

        self.Cleanup()

    def Cleanup(self):
        print "Closing gracefully."

    def Quit(self):
        self.isRunning = False
        print "Core loop terminated."
