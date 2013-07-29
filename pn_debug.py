from pn_entity import Entity
from pn_resources import Text, Color

class FPS_Counter(Entity):
    def Init(self):
        self.text = Text()
        self.text.font = self.core.resourceManager.FetchDefaultFont()
        self.text.character_size = 20
        self.text.color = Color.WHITE
        
    def Step(self):
        self.text.position = self.position
        self.text.string = str(int(1.0/self.core.time.GetDelta())) + " FPS"
        
    def Draw(self):
        self.core.renderer.window.draw(self.text)
        
