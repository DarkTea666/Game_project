from cocos.layer import Layer
from cocos.sprite import Sprite

import starting_stats
from item_menu_layer import ItemMenuLayer

class EquipedLayer(Layer):
    is_event_handler = True
    def __init__(self):
        Layer.__init__(self)
        self.player = False
        self.equipment_dict = {'weapon':[False,Sprite('Sprites/Weapon_empty_slot.png'),760],
                               'armour':[False,Sprite('Sprites/Armour_empty_slot.png'),680],
                               'long_range_1':[False,Sprite('Sprites/Ranged_empty_slot.png'),600],
                               'long_range_2':[False,Sprite('Sprites/Ranged_empty_slot.png'),520],
                               'ring_1':[False,Sprite('Sprites/Ring_empty_slot.png'),440],
                               'ring_2':[False,Sprite('Sprites/Ring_empty_slot.png'),360],
                               'ring_3':[False,Sprite('Sprites/Ring_empty_slot.png'),280],
                               'ring_4':[False,Sprite('Sprites/Ring_empty_slot.png'),200],
                               'artefact_1':[False,Sprite('Sprites/Artefact_empty_slot.png'),120],
                               'artefact_2':[False,Sprite('Sprites/Artefact_empty_slot.png'),40]}
        for name, space in self.equipment_dict.items():
            space[1].position = 1200, space[2]
            space[1].scale = 0.075
            self.add(space[1])

        self.selecter = Sprite('Sprites/Selecter.png')
        self.selecter.scale = 0.05
        self.selecter.opacity = 0
        self.add(self.selecter)


    def equip_item(self,item,inv_layer):
        equip_key = False
        for name, space in self.equipment_dict.items():
            if item.equip_type in name:
                blank = Sprite('Sprites/Blank_inv_space.png')
                blank.scale = 0.075
                if space[0] == False:
                    inv_layer.remove(item)
                    space[0] = item
                    self.remove(space[1])
                    blank.position = 1200, space[2]
                    item.scale = 0.075
                    self.add(blank)
                    item.position = 1200, space[2]
                    self.add(item)
                    equip_key = True
                    break
        if not equip_key:
            print("You don't have enough space to equip this item")

    def on_mouse_press(self,x,y,buttons,modifiers):
        not_press = True
        for name, space in self.equipment_dict.items():
            if x>1200-37.5 and x<1200+37.5 and y>space[2]-37.5 and y<space[2]+37.5:
                self.selecter.position = 1200, space[2]
                self.selecter.scale = 0.075
                self.selecter.opacity = 255
                self.add(self.selecter)
                the_item = space[0]
                not_press = False
                self.add(ItemMenuLayer(the_item, from_equiped_layer = False))
        if not_press:
            self.selecter.opacity = 0






