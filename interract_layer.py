from observer_class import Observer

from cocos.layer import Layer
from items import items_base, items_weapons, items_sceptres
from util import util_starting_stats as starting_stats

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

    def generate_items_open_area(self):
        sword3 = items_weapons.Weapon(starting_stats.Broad_sword, (8, 10))
        self.items.append(sword3)
        y, x = sword3.tile
        sword3.scale = 0.05
        sword3.position = ((x + 1) * 50, (len(self.map_layer.map) - y) * 50)
        self.add(sword3)

        sword3 = items_sceptres.Sceptre(starting_stats.Bluefire_sceptre, (7, 10))
        self.items.append(sword3)
        y, x = sword3.tile
        sword3.scale = 0.05
        sword3.position = ((x + 1) * 50, (len(self.map_layer.map) - y) * 50)
        self.add(sword3)

        sword3 = items_weapons.Weapon(starting_stats.Long_sword, (6, 10))
        self.items.append(sword3)
        y, x = sword3.tile
        sword3.scale = 0.05
        sword3.position = ((x + 1) * 50, (len(self.map_layer.map) - y) * 50)
        self.add(sword3)

        sword3 = items_weapons.Weapon(starting_stats.Short_sword, (5, 10))
        self.items.append(sword3)
        y, x = sword3.tile
        sword3.scale = 0.05
        sword3.position = ((x + 1) * 50, (len(self.map_layer.map) - y) * 50)
        self.add(sword3)








