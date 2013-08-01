from pn_resources import Font, Texture, Shader, EngineMediaDirectory

class ResourceManager(object):
    def __init__(self):
        self.fonts = {}
        self.textures = {}
        self.shaders = {}

    def FetchFont(self, filename):
        if filename not in self.fonts.keys():
            self.fonts[filename] = Font.from_file(filename)
        return self.fonts[filename]

    def FetchDefaultFont(self):
        return self.FetchFont(EngineMediaDirectory()+"pn_font.ttf")

    def FetchDefaultFontMono(self):
        return self.FetchFont(EngineMediaDirectory()+"pn_fontmono.ttf")

    def FetchTexture(self, filename):
        if filename not in self.textures.keys():
            self.textures[filename] = Texture.from_file(filename)
        return self.textures[filename]

    def FetchShader(self, filename):
        if filename not in self.shaders.keys():
            self.shaders[filename] = Shader.from_file(fragment=filename)
        return self.shaders[filename]
        
