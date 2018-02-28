from pyglet.window.key import symbol_string

from cocos.layer import Layer
from cocos.sprite import Sprite
from cocos.batch import BatchNode
from cocos.text import RichLabel

from item_menu_layer import ItemMenuLayer

class EquipedLayer(Layer):
    is_event_handler = True
    def __init__(self):
        Layer.__init__(self)

        self.inv_layer = False

        self.batch = BatchNode()
        self.add(self.batch)

        self.info = {}
        self.info_list = []

        self.all_info = {}
        self.all_info_list = []

        self.equipment_dict = {}
        self.stats_visible = False

        self.selecter = Sprite('Sprites/Selecter.png')
        self.selecter.scale = 0.05
        self.selecter.opacity = 0
        self.add(self.selecter)

    def visualise_equiped_items(self):
        self.equipment_dict = {'weapon': [False, Sprite('Sprites/Weapon_empty_slot.png'), 760],
                               'armour': [False, Sprite('Sprites/Armour_empty_slot.png'), 680],
                               'long_range_1': [False, Sprite('Sprites/Ranged_empty_slot.png'), 600],
                               'long_range_2': [False, Sprite('Sprites/Ranged_empty_slot.png'), 520],
                               'ring_1': [False, Sprite('Sprites/Ring_empty_slot.png'), 440],
                               'ring_2': [False, Sprite('Sprites/Ring_empty_slot.png'), 360],
                               'ring_3': [False, Sprite('Sprites/Ring_empty_slot.png'), 280],
                               'ring_4': [False, Sprite('Sprites/Ring_empty_slot.png'), 200],
                               'artefact_1': [False, Sprite('Sprites/Artefact_empty_slot.png'), 120],
                               'artefact_2': [False, Sprite('Sprites/Artefact_empty_slot.png'), 40]}
        for name, space in self.equipment_dict.items():
            space[1].position = 1200, space[2]
            space[1].scale = 0.075
            self.batch.add(space[1])

    def update_player_information(self):
        player = self.inv_layer.play_layer.player
        self.all_info = {'health':[player.health,'/',player.max_health],
                     'strength':[player.strength],
                     'damage':[int(player.damage)],
                     'defence':[player.defence],
                     'regeneration':[player.regen],
                     'speed':[player.speed],
                     'energy':[player.energy, '/', player.max_energy],
                     'intellect':[player.intellect],
                     'preferred weapon type':[player.pref_weapon_type],
                     'preferred armour type':[player.pref_armour_type]}

    def visualise_player_information(self, de_vis = False):
        self.update_player_information()
        if de_vis:
            for label in self.info_list:
                self.remove(label)

        self.info_list = []
        base_y = 700
        for name, stats in self.all_info.items():
            text = name + ': '
            for stat in stats:
                text += str(stat)
            label = RichLabel(text, (20, base_y), font_size = 12)
            self.info_list.append(label)
            base_y -= 20

        if not de_vis:
            for label in self.info_list:
                self.add(label)


    def equip_item(self,item,inv_layer):
        equip_key = False
        for name, space in self.equipment_dict.items():
            if item.equip_type in name:
                blank = Sprite('Sprites/Blank_inv_space.png')
                blank.scale = 0.075
                if space[0] == False:
                    inv_layer.remove(item)
                    space[0] = (item, item.buttons)
                    self.batch.remove(space[1])
                    blank.position = 1200, space[2]
                    item.scale = 0.075
                    self.batch.add(blank)
                    item.position = 1200, space[2]
                    self.add(item)
                    equip_key = True
                    return True
                    break
        if not equip_key:
            return False
            print("You don't have enough space to equip this item")

    def on_mouse_press(self,x,y,buttons,modifiers):
        not_press = True
        for name, space in self.equipment_dict.items():
            if 1200+37.5>=x>=1200-37.5 and space[2]+37.5>=y>=space[2]-37.5:
                self.selecter.position = 1200, space[2]
                self.selecter.scale = 0.075
                self.selecter.opacity = 255
                self.batch.add(self.selecter)
                the_item = space[0]
                not_press = False
                if the_item != False:
                    self.add(ItemMenuLayer(the_item, from_equiped_layer = True))
        if not_press:
            self.selecter.opacity = 0

        if self.inv_layer.play_layer.inv_open == False and self.stats_visible == True:
            self.visualise_player_information(de_vis=True)
            self.stats_visible = False

    def on_key_press(self, key, modifiers):
        if self.inv_layer.play_layer.inv_open == False:
            if symbol_string(key) == 'H':
                a_key = True
                if not self.stats_visible:
                    self.visualise_player_information()
                    self.stats_visible = True
                    a_key = False
                if self.stats_visible and a_key:
                    self.visualise_player_information(de_vis = True)
                    self.stats_visible = False

            if symbol_string(key) != 'H' and self.stats_visible == True:
                self.visualise_player_information(de_vis=True)
                self.stats_visible = False






