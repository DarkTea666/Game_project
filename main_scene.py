from cocos.scene import Scene
from cocos import layer, scene
from cocos.scenes import *
from cocos.director import director

from algorithms.algorithms_visibility import calculate_visibility
from util import util_starting_stats as starting_stats
import config
from database_ideas import clear_level_database, move_level_to_database,\
find_level_size, restore_level_from_database, restore_mobs_from_database, delete_level_from_database

from map_generation import LevelMap
from interact_layer import InteractableLayer
from effect_layer import EffectLayer
from visibility_layer import VisibilityLayer
from inventories import InventoryLayer
from equiped_layer import EquipedLayer
from util.util_selecting_layer import SelectLayer
from play_layer import PlayingLayer
import items

class PlayScene(Scene):
    def __init__(self, player, level = 1, levels_visited = [], prev_level = False):
        Scene.__init__(self)
        self.level = level
        self.levels_visited = set(levels_visited)
        self.levels_visited = list(self.levels_visited)
        self.player = player
        self.prev_level = prev_level
       
        map_layer = LevelMap(self.level, subject1=self.player)
        if self.level in self.levels_visited:
            print('prev.level ')
            restore_level_from_database(map_layer)
            play_layer = PlayingLayer(self.player, map_layer, subj1=self.player)
            restore_mobs_from_database(play_layer, map_layer)
            delete_level_from_database(self.level)
            
            if self.prev_level > self.level:
                self.position_the_player(map_layer, _from = 'exit')
            else:
                self.position_the_player(map_layer, _from = 'entrance')

            inventory_layer = self.player.inventory
            equip_layer = self.player.equip_layer
            print(equip_layer.equipment_dict)

            interactive_layer = InteractableLayer(map_layer, subj1=self.player, subj2=play_layer)
            play_layer.interactive_layer = interactive_layer

        
        else:
            if self.level == 1: #later level == 0
                clear_level_database()
                equip_layer = EquipedLayer()
                self.player.equip_layer = equip_layer
                inventory_layer = InventoryLayer(equip_layer)
                equip_layer.inv_layer = inventory_layer
                self.player.inventory = inventory_layer
                equip_layer.visualise_equiped_items()#
            else:
                inventory_layer = self.player.inventory
                equip_layer = self.player.equip_layer
            
            map_layer.generate_map()
            play_layer = PlayingLayer(self.player, map_layer, subj1=self.player)
            play_layer.spawn_initial_mobs()
            self.position_the_player(map_layer, _from = 'entrance')
           
            interactive_layer = InteractableLayer(map_layer, subj1=self.player, subj2=play_layer)
            play_layer.interactive_layer = interactive_layer
            play_layer.spawn_items()#for now, will later be done by interact_layer

        for inv_name, inv_type in inventory_layer.dict_inv.items():
            for row in inv_type[0]:
                for item in row:
                    if item != False:
                        item[0].inv_layer = inventory_layer
        for place_name, place in equip_layer.equipment_dict.items():
            if place[0] != False:
                place[0][0].inv_layer = inventory_layer
                print(11111111111111111111111111111111111111111111111)

        effect_layer = EffectLayer(map_layer)
        visibility_layer = VisibilityLayer(map_layer, subj1=play_layer, subj2=self.player)
        
        #TODO: somehow detete all traces of th old play_layer when a new one loads, as the old one still registers dispatched events. also this may be why past levels
        #act so strangly when loaded. FIX THIS.
        inventory_layer.interactive_layer = interactive_layer
        play_layer.effect_layer = effect_layer
        inventory_layer.play_layer = play_layer
        play_layer.change_player_visibility()

        self.add(map_layer, z=0)
        self.add(interactive_layer, z=1)
        self.add(play_layer, z=2)
        self.add(effect_layer, z=3)
        self.add(visibility_layer, z=5)
        self.add(equip_layer, z=6)
        
        self.levels_visited.append(level)#later will be level 0
        print('levels_visited: ' + str(self.levels_visited))

        equip_layer.update_bars(first_time = True)

    def position_the_player(self,map_layer,_from = None):
        if _from == None:
            RaiseError("'_from' must == 'exit' or 'entrance'")
        elif _from == 'exit':
            for i in range(len(map_layer.map)):
                for j in range(len(map_layer[0])):
                    if map_layer.tile_map[i][j].exit != False:
                        tile = map_layer.tile_map[i][j]
                        self.player.race_sprite.position = tile.position
                        self.player.class_sprite.position = tile.position
                    else:
                        print('it should not be locked!!!!')
        elif _from  == 'entrance':
            for i in range(len(map_layer.map)):
                for j in range(len(map_layer[0])):
                    if map_layer.tile_map[i][j].entrance == 'unlocked':
                        tile = map_layer.tile_map[i][j]
                        self.player.race_sprite.position = tile.position
                        self.player.class_sprite.position = tile.position


