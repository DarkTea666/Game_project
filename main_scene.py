from cocos.scene import Scene
from cocos import layer, scene
from cocos.scenes import *
from cocos.director import director

from visibility import calculate_visibility
import starting_stats
import config
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

class MainScene(Scene):
    def __init__(self, chosen_race = config.Human, chosen_class = config.Warlock):
        Scene.__init__(self)

        player1 = Player(chosen_race, chosen_class)

        map_layer = LevelMap(1, subject1=player1)
        map_layer.generate_map()
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
        play_layer.spawn_initial_mobs()
        play_layer.spawn_items()

        self.add(map_layer, z=0)
        self.add(interactive_layer, z=1)
        self.add(play_layer, z=2)
        self.add(effect_layer, z=3)
        self.add(visibility_layer, z=5)
        self.add(equip_layer, z=6)
