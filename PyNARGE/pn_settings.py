from pn_utils import *

class Settings(object):
    def __init__(self):
        self.window_title = "PyNARGE Window"
        self.display_size = Vec2(800, 600)
        self.display_fps = True
        self.label_entity_types = False
        self.display_fullscreen = False
        self.antialiasing = False
        self.enable_lmb_manipulation = False
        self.enable_rmb_destruction = False
        self.limit_framerate = True
        
