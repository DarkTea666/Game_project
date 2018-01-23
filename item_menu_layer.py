from pyglet.window.key import symbol_string
from cocos.layer import Layer
from cocos.sprite import Sprite
from cocos.text import RichLabel

from functools import partial

class ItemMenuLayer(Layer):
    is_event_handler = True
    def __init__(self,the_item, from_equiped_layer = False):
        Layer.__init__(self)

        self.item = the_item[0]
        self.item_funcs = the_item[1]
        self.item_buttons = []
        self.y0 = 0

        self.description = self.item.menu
        self.description_labels = []
        for row in self.description:
            label = RichLabel(row, (425,500 - 20*self.description.index(row)),
                             font_size = 14)
            self.add(label)
            self.description_labels.append(label)

        y = 500 - 20*len(self.description)-20
        for button in self.item.buttons:
            not_key = 'Unequip'
            if from_equiped_layer == True:
                not_key = 'Equip'
            if button != not_key:
                button_text = RichLabel(button, (425, y), bold = True, font_size = 14)
                background = Sprite('Sprites/Button_background.png')
                background.scale_x = len(button)
                background.position = 425 + 11.1*len(button)/2, y+5
                self.y0= y-20
                self.add(background)
                self.add(button_text)
                self.item_buttons.append((button, y))
                y -= 40
