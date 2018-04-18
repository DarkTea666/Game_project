from observer_class import Observer

from cocos.layer import Layer
from items import items_base, items_weapons, items_sceptres, items_misc
from util import util_starting_stats as starting_stats
from random import randrange
import random


class InteractableLayer(Layer, Observer):#holds items, doors, chests, crates(ex: bookcases)...
    def __init__(self, map_layer, subj1 = False, subj2 = False):
        Layer.__init__(self)
        Observer.__init__(self, subject1 = subj1, subject2 = subj2)

        self.items = []
        self.doors = []
        self.chests = []
        self.high_vegetation_tiles = []
        self.crates = []

        self.level = map_layer.level
        self.map_layer = map_layer

    def generate_items_open_area(self):#for a full game, a lot of changes must be made
        all_items = []
        num_of_food = randrange(1,3)
        num_of_weak_health_potions = randrange(0,3)
        
        level_key = items_misc.LevelKey('Level '+str(self.level)+' Key', 'Sprites/Item_Golden_key.png', None, self.level)
        
        blue_fire_sceptre = items_sceptres.Sceptre(starting_stats.Bluefire_sceptre, None)
        long_sword = items_weapons.Weapon(starting_stats.Long_sword, None)
        short_sword = items_weapons.Weapon(starting_stats.Short_sword, None)
        strong_health_menu = ['This healing potion will fully heal you and', 'fulfill your hunger']
        strong_health_potion = items_misc.Potion('Strong Healing Potion','Sprites/Item_strong_red_potion.png',
                                                  None, strong_health_menu, effect = 'Strong_Healing' )

        
        if self.level == 1:
            forest_items = [short_sword, long_sword, strong_health_potion]
            all_items.append(items_sceptres.Sceptre(starting_stats.Bluefire_sceptre, None))
            num_of_forest_items = randrange(1,2)
        else:
            forest_items = [blue_fire_sceptre, short_sword, long_sword, strong_health_potion]
            num_of_forest_items = randrange(0,4)
        
        all_items = random.sample(forest_items, num_of_forest_items)
        all_items.append(level_key)
        
        if self.level % 3 == 0:
            strength_potion = items_misc.Potion('Strength potion', 'Sprites/Item_green_potion.png', None,
                                               ['This potion will increase your strength.'], effect = 'Strength_Addition')
            all_items.append(strength_potion)
        print(all_items)#not nessesary  
        
        for food in range(num_of_food):#change this as well
            bread = items_misc.Food('Bread', 'Sprites/Item_bread.png', None, 'Just a piece of bread.', adds_hunger = 20)
            all_items.append(bread)

        weak_health_menu = ['This healing potion will heal you for a ', 'quater of your health']
        for potion in range(num_of_weak_health_potions):#change this as well
            weak_health_potion = items_misc.Potion('Weak Healing Potion', 'Sprites/Item_weak_red_potion.png', None, weak_health_menu)
            all_items.append(weak_health_potion)
            print('POTION')

        all_possible_tiles = []
        for i in range(len(self.map_layer.map)):
            for j in range(len(self.map_layer[0])):
                if self.map_layer[i][j] == 0:
                    all_possible_tiles.append((i,j))
        for item in all_items:
            tile = random.choice(all_possible_tiles)
            all_possible_tiles.remove(tile)
            item.tile = tile
            i,j = item.tile
            item.position = (j+1)*50, (len(self.map_layer.map)-i)*50
            item.scale = 0.05
            self.items.append(item)
            self.add(item)
#TODO: add strong health potions to forest items




