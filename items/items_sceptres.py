from cocos.sprite import Sprite
from cocos.text import RichLabel
from cocos.layer import Layer
from cocos.actions import RotateBy, MoveBy, MoveTo, CallFunc, FadeIn, FadeOut, Delay

from items.items_base import Item, rotate_missile

from util.util_selecting_layer import SelectLayer


class Sceptre(Item):
    def __init__(self, sceptre_stats, tile, enchantment=False, level=1):
        Item.__init__(self,
                      sceptre_stats.name,
                      sceptre_stats.image,
                      tile,
                      sceptre_stats.menu,
                      {'Drop': self.Drop, 'Equip': self.Equip, 'Unequip': self.Unequip, 'Recharge': self.Recharge,
                       'Cast': self.Cast})
        self.inv_type = 'weapons'
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
            if class_dict['mana'] >= self.max_ammo * 50:
                class_dict['mana'] -= self.max_ammo * 50
                self.ammo = self.max_ammo

    def Damage(self, opponent):
        try:
            opponent.health -= (self.base_damage + (self.level - 1) * 5)
            try:
                print('You hit', opponent.name, '!')
            except:
                print("Your shot hit it's target!")
        except:
            print('You cannot damage that!')
        self.inv_layer.play_layer.player.turn += 1
        self.inv_layer.play_layer.do_after_turn()

    def Cast(self):
        inv_layer = self.inv_layer
        play_layer = inv_layer.play_layer
        if play_layer.inv_open == True:
            play_layer.inv_open = False
        play_layer.handling_moves = False
        try:
            play_layer.parent.remove(inv_layer)
        except:
            pass
        select_layer = SelectLayer(inv_layer)
        select_layer.function = self.Visualise_cast_Normal
        # maybe give select_layer the image to make Visualise_cast_Normal more general?
        play_layer.parent.add(select_layer, z=4)

    def Visualise_cast_Normal(self, select_layer, effect_layer, target_i=False, target_j=False):
        play_layer = self.inv_layer.play_layer
        player = play_layer.player
        map_layer = play_layer.map_layer
        len_m = len(map_layer.map)

        missile_path = self.Missile_path_function(target_i, target_j)
        end_j, end_i = missile_path[len(missile_path) - 1][0], missile_path[len(missile_path) - 1][1]
        x0, y0 = (end_j + 1) * 50, (len_m - end_i) * 50

        # remove this if you are making this function more normal
        missile_sprite = Sprite('Sprites/Effect_Blue_Fireball.png')
        missile_sprite.scale = 0.05
        missile_sprite.position = player.race_sprite.position
        effect_layer.add(missile_sprite)
        after_effect = Sprite('Sprites/Effect_Blue_Fireball_hit.png', opacity=0)

        key = True
        for j, i in missile_path:
            mob_inf = play_layer.check_tile_for_mob(j, i)
            if mob_inf[0]:
                mob = mob_inf[1]
                end_i, end_j = i, j  #
                missile_time = missile_path.index((j, i)) / 6  #
                rotate_missile(missile_sprite,
                               player.tile()['i'] + len_m, player.tile()['j'],
                               end_i, end_j)
                move_action = MoveTo((50 * (end_j + 1), 50 * (len_m - end_i)), missile_time)  ##
                damage_action = CallFunc(self.Damage, mob)
                key = False
                break
        if key:
            end_j, end_i = x0 / 50 - 1, -y0 / 50 + len_m  #
            missile_time = len(missile_path) / 6  #
            rotate_missile(missile_sprite,
                           player.tile()['i'] + len_m, player.tile()['j'],
                           end_i, end_j)
            move_action = MoveTo((x0, y0), missile_time)  ##
            damage_action = CallFunc(self.Damage, None)

        disappear_action = CallFunc(effect_layer.effect_remove, missile_sprite)
        after_effect.position = missile_sprite.position  # MAKE AN ACTION THAT MAKES A SPRITE FADEIN AND FADEOUT
        # put part of this or all of this fully into effect_layer?
        missile_sprite.do(move_action + damage_action + disappear_action)

