import sfml

class Font(sfml.Font):
    pass

class Text(sfml.Text):
    pass

class Color(sfml.Color):
    pass

class Sprite(sfml.Sprite):
    pass

class Texture(sfml.Texture):
    pass

import os

def EngineMediaDirectory():
    return os.path.dirname(os.path.realpath(__file__))+"\\EngineMedia\\"