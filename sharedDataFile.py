
"""
Because python is a scripted langauge it allows the creation of a 'shared data map'. Because both the main thread and
GUI share this import AS IS they share the same mem region. This can be used to pass data between threads, GUIs
and other code sections with ease.

this arguable is the simplist way to share data between python modules.

"""

sharedDataWindowListener = "CONNECTION ERROR: device not detected."