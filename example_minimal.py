from PyNARGE import *

# Create a new entity type
class Crate(ComponentEntity):
    # To build this entity
    def Build(self):
        # Assign a sprite
        self.AddComponent( SpriteComponent( self.core.resourceManager.FetchTexture("media\\crate.png") ) )

        # Adds physics to this entity
        self.AddComponent( RigidBody_Rectangular( (16, 16), (100, -100) ) )

        # Respawn when offscreen
        self.AddComponent( RespawnableComponent( lambda x: x.position.y > 900 ) )

    # Every frame
    def Step(self):
        # Spit out some details to the console
        print "I am a crate @ " + str(self.position)

# Set some options
settings = Settings()
settings.display_size = Vec2(800, 600)
settings.enable_lmb_manipulation = True

# Create an app with the options
app = GameCore(settings)

# Add some text, a background image and finally an instance of our crate
app.uiManager.AddEntity( DefaultText("The cube shall fall off the screen unless you catch it!", (300, 480) ) )
app.entityManager.AddEntity( BackgroundImage( app.resourceManager.FetchTexture("media\\background.jpg") ) )
app.entityManager.AddEntity( Crate() )

# Begin the main loop   
app.Run()
