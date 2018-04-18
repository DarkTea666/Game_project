from cocos.sprite import Sprite
from cocos.text import RichLabel
from cocos.layer import Layer
from cocos.actions import RotateBy, MoveBy, MoveTo, CallFunc, FadeIn, FadeOut, Delay

from items.items_base import Item

class Weapon(Item):
    def __init__(self,weapon_stats, tile, enchantment = False, level = 1):
        Item.__init__(self,
                      weapon_stats.name,
                      weapon_stats.image,
                      tile,
                      weapon_stats.menu,
                      {'Drop':self.Drop, 'Equip':self.Equip_and_Add_stats,
                       'Unequip':self.Unequip_and_Remove_stats})

        self.inv_type = 'weapons'
        self.equip_type = 'weapon'
        self.level = level

        self.base_damage = weapon_stats.base_damage
        self.damage = self.base_damage
        self.weapon_type = weapon_stats.weapon_type
        self.req_strength = weapon_stats.req_strength
        self.miss_chance = weapon_stats.miss_chance
        self.enchantment = enchantment

    def Equip_and_Add_stats(self):
        self.Add_stats()
        self.Equip()

    def Unequip_and_Remove_stats(self):
        self.Remove_stats()
        self.Unequip()

    def Remove_stats(self):
        player = self.inv_layer.play_layer.player
        player.damage -= (self.damage + (self.level-1)*5)

    def Add_stats(self):
        player = self.inv_layer.play_layer.player
        player.damage += (self.damage + (self.level-1)*5)



