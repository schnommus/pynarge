.. PyNARGE documentation master file, created by
   sphinx-quickstart on Sat Aug 03 21:18:44 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

GameCore & Settings
===================

Overview
--------

PyNARGE applications are generally created by supplying a `GameCore` constructor with a `Settings` instance, adding
some entities to the `GameCore`, and then calling `GameCore.Run()`. For example: ::

	# Set some options
	settings = Settings()
	settings.display_size = Vec2(800, 600)

	# Create an app with the options
	app = GameCore(settings)

	# Add an entity
	app.entityManager.AddEntity( SomeEntity() )

	# Begin the main loop   
	app.Run()

API
---

Sphinx doesn't like documenting my initial values for some reason -- check `pn_settings.py` to find default values that `Settings` will use. In short, "PyNARGE Window" at 800x600, windowed.

.. autoclass:: PyNARGE.Settings
	:members:

.. autoclass:: PyNARGE.GameCore
	:members:
	

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

