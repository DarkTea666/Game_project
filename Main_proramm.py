from pyglet.window.key import symbol_string
from pyglet.event import EventDispatcher

from cocos import layer, scene
from cocos.scenes import *
from cocos.director import director

from random import randrange
from functools import partial
import math

from visibility import calculate_visibility
import starting_stats
from create_character import Player
from map_generation import LevelMap
from interract_layer import InteractableLayer
from effect_layer import EffectLayer
from visibility_layer import VisibilityLayer
from inventories import InventoryLayer
from equiped_layer import EquipedLayer
from selecting_layer import SelectLayer
from play_layer import PlayingLayer
import items

import menu_scene


if __name__ == '__main__':

    director.init(width=1250, height=800, autoscale=True, resizable=True)

    first_layer = menu_scene.FirstLayer()
    menu_scene = scene.Scene(first_layer)

    director.show_FPS = True

    import profile
    #profile.run('director.run(main_scene)', sort='cumtime')
    director.run(menu_scene)

