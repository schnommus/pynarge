from pn_resources import Font

class ResourceManager(object):
    def __init__(self):
        self.fonts = {}
        self.images = {}

    def FetchFont(self, filename):
        if filename not in self.fonts.keys():
            self.fonts[filename] = Font.from_file(filename)
        return self.fonts[filename]

    def FetchDefaultFont(self):
        return self.FetchFont("pn_font.ttf")

    def FetchDefaultFontMono(self):
        return self.FetchFont("pn_fontmono.ttf")
        
