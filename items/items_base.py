from cocos.sprite import Sprite
from cocos.text import RichLabel
from cocos.layer import Layer
from cocos.actions import RotateBy, MoveBy, MoveTo, CallFunc, FadeIn, FadeOut, Delay

import math
from util.util_selecting_layer import SelectLayer
from algorithms.algorithms_visibility import tile_line, ray_to_border

class Item(Sprite):
    def __init__(self,name,image,tile,menu,buttons,inv_type='all'):
        Sprite.__init__(self, image)

        self.name = name
        self.tile = tile
        self.buttons = buttons

        self.inv_type = inv_type
        self.inv_place = False
        self.equip_type = False
        self.menu = menu

        self.inv_layer = False

    def Drop(self):
        inv_layer = self.inv_layer
        for name, inv in inv_layer.dict_inv.items():
            for row in inv[0]:
                for item_num in range(0,3):
                    item_inf = row[item_num]
                    if item_inf != False and item_inf[0] == self:
                        remove_that = (inv[0], inv[0].index(row), item_num)
                        break
        interact_layer = inv_layer.interactive_layer
        inv_layer.remove(self)
        remove_that[0][remove_that[1]][remove_that[2]] = False
        interact_layer.items.append(self)
        self.position = (inv_layer.play_layer.player.race_sprite.position)
        self.scale = 0.05
        x,y = self.position
        self.tile = len(inv_layer.play_layer.map_layer.map)-y/50, x/50-1
        print(self.tile)
        interact_layer.add(self)

    def Equip(self):
        inv_layer = self.inv_layer
        for name, inv in inv_layer.dict_inv.items():
            for row in inv[0]:
                for item_num in range(0,3):
                    item_inf = row[item_num]
                    if item_inf != False and item_inf[0] == self:
                        remove_that = (inv[0], inv[0].index(row), item_num)
                        break
        if inv_layer.equip_layer.equip_item(self,inv_layer):
            remove_that[0][remove_that[1]][remove_that[2]] = False

    def Unequip(self):
        inv_layer = self.inv_layer
        self.scale = 0.05
        remove_name = False
        inv_layer.equip_layer.remove(self)

        if inv_layer.add_to_inventory(self):
            for name, item_space in inv_layer.equip_layer.equipment_dict.items():
                if item_space[0] != False and item_space[0][0] == self:
                    remove_name = name
                    inv_layer.equip_layer.batch.add(item_space[1], z = 100)
            if remove_name != False:
                inv_layer.equip_layer.equipment_dict[remove_name][0] = False
        else:
            print('the inventory of that type is full')

    def Missile_path_function(self, target_i, target_j):
        player = self.inv_layer.play_layer.player
        map_layer = self.inv_layer.play_layer.map_layer
        i_p, j_p = player.tile()['i'] + len(map_layer.map), player.tile()['j']
        print((j_p+0.5, i_p+0.5, target_j+0.5, target_i+0.5))
        line_of_fire = tile_line(j_p+0.5, i_p+0.5, target_j+0.5, target_i+0.5)
        print(line_of_fire)
        return line_of_fire

def rotate_missile(missile_sprite, start_i, start_j, end_i, end_j):
    print('pi:',start_i,'--- pj:',start_j, end_i, end_j)
    delta_i, delta_j = end_i - start_i, end_j - start_j
    if abs(delta_i) <= abs(delta_j):
        try:
            tg_alpha = delta_i/delta_j
        except:
            pass
        if delta_j < 0:
            alpha = math.degrees(tg_alpha) - 90
        elif delta_j > 0:
            alpha = math.degrees(tg_alpha) + 90
        elif delta_j == 0:
            if delta_i>0:
                alpha = 90
            else:
                alpha = -90
    if abs(delta_i) > abs(delta_j):
        try:
            tg_alpha = delta_j/delta_i
        except:
            pass
        if delta_i < 0:
            alpha = -math.degrees(tg_alpha)
        elif delta_i > 0:
            alpha = -math.degrees(tg_alpha) - 180
        elif delta_i == 0:
            if delta_j>0:
                alpha = 90
            else:
                alpha = -90
    missile_sprite.rotation = alpha



class Armour(Item):
    def __init__(self, armour_stats, tile, imbued=False, level=1):

        Item.__init__(self,
                      armour_stats.name,
                      armour_stats.image,
                      tile,
                      armour_stats.menu,
                      {'Drop': self.Drop, 'Equip': self.Drop})

        self.inv_type = 'armour'
        self.equip_type = 'armour'
        self.level = level

        self.base_defence = armour_stats.base_defence
        self.armor_type = armour_stats.armor_type
        self.req_strength = armour_stats.req_strength
        self.fail_chance = armour_stats.fail_chance
        self.imbued = imbued

class Ring(Item):
    def __init__(self,name,image,inv_image,tile,menu,
                 level = 1):

        Item.__init__(self,name,image,inv_image,tile,menu)

        self.inv_type = 'jewellery'
        self.level = level
