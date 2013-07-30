import sfml

class Input(object):
    def __init__(self, core):
        self.core = core
        self.keyboard = sfml.window.Keyboard
        self.joystick = sfml.window.Joystick
        self.mouse = sfml.window.Mouse

    def GetMousePosition(self):
        return self.core.input.mouse.get_position(self.core.renderer.window)
        
