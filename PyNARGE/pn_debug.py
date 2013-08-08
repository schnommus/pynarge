from pn_componententity import ComponentEntity
from pn_standardcomponents import TextComponent
from pn_resources import Text, Color

class FPS_Counter(ComponentEntity):
    """Stock entity that will display application FPS in the top-left corner"""
    def Build(self):
        self.text = TextComponent("", self.core.resourceManager.FetchDefaultFontMono())
        self.AddComponent( self.text )
        
    def Step(self):
        self.text.SetText( str(int(1.0/self.core.time.GetDelta())) + " FPS")
        
