from cocos.scene import Scene
from cocos import layer, scene
from cocos.scenes import *
from cocos.director import director

from algorithms.algorithms_visibility import calculate_visibility
from util import util_starting_stats as starting_stats
import config
from database_ideas import clear_level_database, move_level_to_database,\
find_level_size, restore_level_from_database, restore_mobs_from_database

from create_character import Player
from map_generation import LevelMap
from interract_layer import InteractableLayer
from effect_layer import EffectLayer
from visibility_layer import VisibilityLayer
from inventories import InventoryLayer
from equiped_layer import EquipedLayer
from util.util_selecting_layer import SelectLayer
from play_layer import PlayingLayer
import items

class FirstScene(Scene):
    def __init__(self, level = 1, chosen_race = False, chosen_class = False, levels_visited = []):
        Scene.__init__(self)
        self.level = level
        self.levels_visited = levels_visited

        if self.level == 1:#later level == 0
            try:
                player1 = Player(chosen_race, chosen_class)
            except:
                TypeError("the chosen race and/or class have not been specified!")
            equip_layer = EquipedLayer()
            player1.equip_layer = equip_layer
            inventory_layer = InventoryLayer(equip_layer)
            equip_layer.inv_layer = inventory_layer
            equip_layer.visualise_equiped_items()

        map_layer = LevelMap(self.level, subject1=player1)
        map_layer.generate_map()
        play_layer = PlayingLayer(player1, map_layer, subj1=player1)
        play_layer.spawn_initial_mobs()

        if self.level in self.levels_visited:
            map_layer = LevelMap(level, subject1=player1)
            restore_level_from_database(map_layer)
            play_layer.mobs = []
            restore_mobs_from_database(play_layer, map_layer)
        else:
            pass
        interactive_layer = InteractableLayer(map_layer, subj1=player1, subj2=play_layer)
        effect_layer = EffectLayer(map_layer)
        visibility_layer = VisibilityLayer(map_layer, subj1=play_layer, subj2=player1)

        inventory_layer.interactive_layer = interactive_layer
        play_layer.effect_layer = effect_layer
        play_layer.player.inventory = inventory_layer
        play_layer.interactive_layer = interactive_layer
        inventory_layer.play_layer = play_layer
        play_layer.spawn_items()#for now, will later be done by interact_layer

        self.add(map_layer, z=0)
        self.add(interactive_layer, z=1)
        self.add(play_layer, z=2)
        self.add(effect_layer, z=3)
        self.add(visibility_layer, z=5)
        self.add(equip_layer, z=6)

        self.levels_visited.append(level)#later will be level 0

        #database testing zone ,    WILL BE REMOVED SOON

        clear_level_database()
        move_level_to_database(map_layer, play_layer.mobs)

        self.remove(map_layer)
        map_layer = LevelMap(1, subject1=player1)
        restore_level_from_database(map_layer)
        self.add(map_layer, z=0)
        #mobs:
        for mob in play_layer.mobs:
            play_layer.remove(mob)
        play_layer.mobs = []
        restore_mobs_from_database(play_layer, map_layer)


class CurrentScene(Scene):
    def __init__(self, player, level, levels_visited):
        Scene.__init__(self)

        self.levls_visited = levels_visited
        if level in levels_visited:
            pass#do database things
        else:
            map_layer = LevelMap(level, subject1=player1)
            map_layer.generate_map()

        #finish this
        play_layer = PlayingLayer(player1, map_layer, subj1=player1)
        interactive_layer = InteractableLayer(map_layer, subj1=player1, subj2=play_layer)
        effect_layer = EffectLayer(map_layer)
        visibility_layer = VisibilityLayer(map_layer, subj1=play_layer, subj2=player1)
        equip_layer = EquipedLayer()
        inventory_layer = InventoryLayer(play_layer, interactive_layer, equip_layer)

        player1.equip_layer = equip_layer
        play_layer.effect_layer = effect_layer
        play_layer.player.inventory = inventory_layer
        play_layer.interactive_layer = interactive_layer
        equip_layer.inv_layer = inventory_layer
        play_layer.spawn_initial_mobs()
        play_layer.spawn_items()
        equip_layer.visualise_equiped_items()

        self.add(map_layer, z=0)
        self.add(interactive_layer, z=1)
        self.add(play_layer, z=2)
        self.add(effect_layer, z=3)
        self.add(visibility_layer, z=5)
        self.add(equip_layer, z=6)