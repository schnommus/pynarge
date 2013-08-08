.. PyNARGE documentation master file, created by
   sphinx-quickstart on Sat Aug 03 21:18:44 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

PyNARGE
=======

An Overview
-----------

	.. image:: screenshot1.jpg
		:height: 350
		:width: 600
		:align: center

	PyNARGE (or Python's Not A Real Game Engine) is a slightly more abstract 2D game
	engine than what I've seen around in the Python world today: it supports physics,
	some default shaders (i.e water, blurring, pixellation), GUI elements, entity management, component-based entities
	and a bunch of other stuff straight off the bat.

Using The Engine
----------------

	PyNARGE's API has been designed to get a functioning application up and running as quickly as possible. For example, the following code
	will open a window, load images for a crate, treat it as a physics entity, set a static background & display some info text.
	The crate will respawn if it falls offscreen; allowing the player another chance to catch it with the mouse if they're too slow: ::
	
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
		
	Currently, the best way to learn how to use PyNARGE is to read the API docs and example code available.
	If there's enough interest, a tutorial series may well be incoming!

The API
-------
	
	.. toctree::
	   :maxdepth: 2
	   
	   coresettings
	   
	   

	.. autoclass:: PyNARGE.Component
		:members

	.. autoclass:: PyNARGE.ShaderPass
		:members:
		
	.. autoclass:: PyNARGE.EngineShaders
		:members:
		
	.. automodule:: PyNARGE.pn_entitymanager
		:members:

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

