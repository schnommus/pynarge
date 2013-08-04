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

class RenderTexture(sfml.RenderTexture):
    pass

class Shader(sfml.Shader):
    pass

class RenderStates(sfml.RenderStates):
    pass

class SoundBuffer(sfml.SoundBuffer):
    pass

class Sound(sfml.Sound):
    pass

import os

def EngineMediaDirectory():
    return os.path.dirname(os.path.realpath(__file__))+"\\EngineMedia\\"
