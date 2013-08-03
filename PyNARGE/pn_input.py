from pn_utils import *
import sfml

class Input(object):
    def __init__(self, core):
        self.core = core
        self.keyboard = sfml.window.Keyboard
        self.joystick = sfml.window.Joystick
        self.mouse = sfml.window.Mouse

    def GetMousePosition(self):
        mouse = Vec2(self.core.input.mouse.get_position(self.core.renderer.window))
        camera = self.core.renderer.GetCameraPosition()-self.core.renderer.GetWindowSize()/2
        return mouse + camera

    def GetMousePositionUI(self):
        return Vec2(self.core.input.mouse.get_position(self.core.renderer.window))
