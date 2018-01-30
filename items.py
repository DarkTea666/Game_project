
from cocos.sprite import Sprite
from cocos.text import RichLabel
from cocos.layer import Layer
from cocos.actions import RotateBy, MoveBy, MoveTo

import math

import starting_stats

from selecting_layer import SelectLayer
from visibility import tile_line_vis, ray_to_border

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
                    inv_layer.equip_layer.batch.add(item_space[1])
            if remove_name != False:
                inv_layer.equip_layer.equipment_dict[remove_name][0] = False
        else:
            print('the inventory of that type is full')

    def Missile_path_function(self, target_i, target_j):
        player = self.inv_layer.play_layer.player
        map_layer = self.inv_layer.play_layer.map_layer
        x, y = (target_j+1)*50, (len(map_layer.map)-target_i)*50
        x_p, y_p = player.race_sprite.position
        line_end_coords = ray_to_border(x_p, y_p, x, y, 1225, 25, 775, 25)
        x0,y0 = line_end_coords
        xc, yc = x0 - (x%50)+25, y0-(y%50)+25
        j_e, i_e = xc/50-1, -yc/50+len(map_layer.map)
        j_p, i_p = player.tile()['i'] + len(map_layer.map), player.tile()['j']
        line_of_fire = tile_line_vis(j_p, i_p, target_j, target_i, map_layer)#SOMETIMES RANDOMLY DOESN'T WORK
        return line_of_fire


class Weapon(Item):
    def __init__(self,weapon_stats, tile, enchantment = False, level = 1):
        Item.__init__(self,
                      weapon_stats.name,
                      weapon_stats.image,
                      tile,
                      weapon_stats.menu,
                      {'Drop':self.Drop, 'Equip':self.Equip, 'Unequip':self.Unequip})

        self.inv_type = 'weapons'
        self.equip_type = 'weapon'
        self.level = level

        self.base_damage = weapon_stats.base_damage
        self.weapon_type = weapon_stats.weapon_type
        self.req_strength = weapon_stats.req_strength
        self.miss_chance = weapon_stats.miss_chance
        self.enchantment = enchantment


class Sceptre(Item):
    def __init__(self,sceptre_stats, tile, enchantment = False, level = 1):
        Item.__init__(self,
                      sceptre_stats.name,
                      sceptre_stats.image,
                      tile,
                      sceptre_stats.menu,
                      {'Drop':self.Drop, 'Equip':self.Equip, 'Unequip':self.Unequip, 'Recharge':self.Recharge,
                       'Cast':self.Cast})
        self.inv_type = 'all'
        self.equip_type = 'long_range'
        self.level = level

        self.base_damage = sceptre_stats.base_damage
        self.req_intelligence = sceptre_stats.req_intelligence
        self.max_ammo = sceptre_stats.max_ammo
        self.ammo = sceptre_stats.max_ammo
        self.strike_effect = sceptre_stats.strike_effect

    def Recharge(self):
        inv_layer = self.inv_layer
        class_dict = inv_layer.play_layer.player.class_dict
        if 'mana' in class_dict:
            if class_dict['mana'] >= self.max_ammo*50:
                class_dict['mana'] -= self.max_ammo*50
                self.ammo = self.max_ammo

    def Cast(self):
        inv_layer = self.inv_layer
        play_layer = inv_layer.play_layer
        if play_layer.inv_open == True:
            play_layer.inv_open = False
        play_layer.handling_moves = True
        try:
            play_layer.parent.remove(inv_layer)
        except:
            pass
        select_layer = SelectLayer(inv_layer)
        select_layer.function = self.Bluefire_cast
        #puts it's value, None into select_layer.function
        inv_layer.parent.add(select_layer, z = 4)
        #   FINISH THIS

    def Bluefire_cast(self, select_layer, effect_layer, target_i = False, target_j = False):
        player = self.inv_layer.play_layer.player
        map_layer = self.inv_layer.play_layer.map_layer

        missile_path = self.Missile_path_function(target_i, target_j)
        end_i, end_j = missile_path[len(missile_path)-1][0], missile_path[len(missile_path)-1][1]
        print(end_j,end_i)
        x0, y0 = (end_j+1)*50, (len(map_layer.map)-end_i)*50

        missile_image = 'Sprites/Effect_Blue_Fireball.png'
        missile_sprite = Sprite(missile_image)
        missile_sprite.scale = 0.05
        missile_sprite.position = player.race_sprite.position
        effect_layer.add(missile_sprite)
        missile_sprite.do(MoveTo((x0,y0),len(missile_path)/10))



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
                 level):

        Item.__init__(self,name,image,inv_image,tile,menu)

        self.inv_type = 'jewellery'
        self.level = level
        
#artefacts are items, created individually
#-----------------------------UNLESS I FIX A PROBLEM WITH EVENTS, NO ITEMS CAN BE PRE-EQUIPPED---------------------