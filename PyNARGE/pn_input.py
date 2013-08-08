from pn_utils import *
import sfml

class Input(object):
    """For retrieving various input info (mouse, keyboard, joystick)"""
    def __init__(self, core):
        self.core = core
        self.keyboard = sfml.window.Keyboard
        self.joystick = sfml.window.Joystick
        self.mouse = sfml.window.Mouse

    def GetMousePosition(self):
        """Gets the mouse position in world coordinates, transformed using the camera position"""
        mouse = Vec2(self.core.input.mouse.get_position(self.core.renderer.window))
        camera = self.core.renderer.GetCameraPosition()-self.core.renderer.GetWindowSize()/2
        return mouse + camera

    def GetMousePositionUI(self):
        """Gets the mouse position using the UI transformation (static)"""
        return Vec2(self.core.input.mouse.get_position(self.core.renderer.window))
