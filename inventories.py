from pyglet.window.key import symbol_string

from cocos.layer import Layer
from cocos.director import director
from cocos.actions import MoveBy
from cocos.sprite import Sprite
from cocos.text import RichLabel

from functools import partial
from observer_class import Observer
from item_menu_layer import ItemMenuLayer

class InventoryLayer(Layer, Observer):
    is_event_handler = True
    def __init__(self, play_layer, interactive_layer, equip_layer):
        Layer.__init__(self)
        self.handling_clicks = True

        self.play_layer = play_layer
        self.equip_layer = equip_layer
        self.interactive_layer = interactive_layer
        self.k = 1
        self.item_menu = False

        self.inv_img = Sprite('Sprites/Inventory_menu.png')
        self.inv_img.position = 625, 400
        self.add(self.inv_img)

        self.selecter = Sprite('Sprites/Selecter.png')
        self.selecter.scale = 0.05
        self.selecter.opacity = 0
        self.add(self.selecter)
        
        self.weapons_inv = [[False for i in range(4)] for x in range(4)]
        self.alchemy_inv = [[False for i in range(4)] for x in range(4)]
        self.scrolls_inv = [[False for i in range(4)] for x in range(4)]
        self.all_inv = [[False for i in range(4)] for x in range(4)]

        self.dict_inv = {'weapons':(self.weapons_inv, 350, 275),
                         'alchemy':(self.alchemy_inv, 350, 675),
                         'scrolls':(self.scrolls_inv, 750, 675),
                         'all':(self.all_inv, 750, 275)}

    def add_to_inventory(self, item):
        it_key = False
        for inv_name, inv_list in self.dict_inv.items():
            if item.inv_type == inv_name:
                c = 0
                x = inv_list[1]
                y = inv_list[2]
                that_inv_list = inv_list[0]
                for row in range(0,4):
                    c += 1
                    for place in range(0,4):
                        if that_inv_list[row][place] == False and not it_key:
                            func_dict = {name:partial(item.buttons[name],self) for name in item.buttons}
                            that_inv_list[row][place] = (item, func_dict)
                            item.position = x+place*50, y-row*50
                            item.inv_place = (c-1, len(that_inv_list[row])-1)
                            self.add(item)
                            it_key = True
                            item.inv_layer = self
                            break
        return it_key

    def on_mouse_press(self,x,y,buttons,modifiers):
        if self.handling_clicks:
            not_press_key = True
            for inv_name, inv_list in self.dict_inv.items():
                x_b = inv_list[1]-25
                y_b = inv_list[2]+25
                if x > x_b and x < x_b+200 and y < y_b and y > y_b-200:
                    quaters_list = [[(x_b+j*50,y_b-i*50) for j in range(0,4)] for i in range(0,4)]
                    for row in quaters_list:
                        for x0, y0 in row:
                            if x > x0 and x < x0+50 and y < y0 and y > y0-50:
                                self.selecter.position = x0+25, y0-25
                                self.selecter.opacity = 255
                    self.check_item_selected()
                    not_press_key = False
            if not_press_key:
                self.selecter.opacity = 0

    def check_item_selected(self):        
        for inv_name, inv_list in self.dict_inv.items():
            for row in range(0,4):
                for the_item in inv_list[0][row]:
                    if the_item != False and self.selecter.opacity == 255 and\
                    the_item[0].position == self.selecter.position:
                        item_inv = ItemMenuLayer(the_item)
                        self.add(item_inv)
                            #TO DO: make normal text pixelated


