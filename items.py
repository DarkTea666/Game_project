from cocos.sprite import Sprite
import starting_stats

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

    def Drop(self, inv_layer):
        for name, inv in inv_layer.dict_inv.items():
            for row in inv[0]:
                for item_inf in row:
                    if item_inf[0] == self:
                        removing_list = (inv[0], inv[0].index(row), item_inf)
                        break
        interact_layer = inv_layer.interactive_layer
        inv_layer.remove(self)
        removing_list[0][removing_list[1]].remove(item_inf)
        interact_layer.items.append(self)
        self.position = (inv_layer.play_layer.player.race_sprite.position)
        self.scale = 0.05
        x,y = self.position
        self.tile = len(inv_layer.play_layer.map_layer.map)-y/50, x/50-1
        print(self.tile)
        interact_layer.add(self)

    def Equip(self, inv_layer):
        for name, inv in inv_layer.dict_inv.items():
            for row in inv[0]:
                for item_inf in row:
                    if item_inf[0] == self:
                        removing_list = (inv[0], inv[0].index(row), item_inf)
                        break
        inv_layer.equip_layer.equip_item(self,inv_layer)
        removing_list[0][removing_list[1]].remove(item_inf)

    def Unequip(self, inv_layer):
        if not inv_layer.add_to_inventory(self):
            print('the inventory of that type is full')

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
                      {'Drop':self.Drop, 'Equip':self.Equip, 'Unequip':self.Unequip, 'Recharge':self.Recharge})
        self.inv_type = 'weapons'
        self.equip_type = 'long_range'
        self.level = level

        self.base_damage = sceptre_stats.base_damage
        self.req_intelligence = sceptre_stats.req_intelligence
        self.max_ammo = sceptre_stats.max_ammo
        self.ammo = sceptre_stats.max_ammo
        self.strike_effect = sceptre_stats.strike_effect

    def Recharge(self, inv_layer):
        class_dict = inv_layer.play_layer.player.class_dict
        if 'mana' in class_dict:
            if class_dict['mana'] >= self.max_ammo*50:
                class_dict['mana'] -= self.max_ammo*50
                self.ammo = self.max_ammo

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


    #functions: on_equp: +all added stats
    #           on_unequp: -all added stats
        
#artefacts are items, created individually















        

        
