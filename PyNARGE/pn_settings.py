from pn_utils import *

class Settings(object):
    """Stores settings for passing to a GameCore"""
    def __init__(self):
        self.window_title = "PyNARGE Window" #: The title of the application window
        self.display_size = Vec2(800, 600) #: Resolution of the display
        self.display_fps = True #: Show an FPS counter top-left of screen
        self.label_entity_types = False #: Label entities with underlying class type
        self.display_fullscreen = False #: Should the application run fullscreen
        self.antialiasing = False #: Enable 8x antialiasing
        self.enable_lmb_manipulation = False #: Enables physics interaction with left mouse button
        self.enable_rmb_destruction = False #: Enables destruction of physics entities with right mouse button
        self.limit_framerate = True #: Limits framerate to 60FPS. Required when using physics subsystem because changing timestep is unstable
        
