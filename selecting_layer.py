from cocos.layer import Layer
from cocos.sprite import Sprite

from functools import partial

class SelectLayer(Layer):
    is_event_handler = True
    def __init__(self, inv_layer):
        Layer.__init__(self)

        self.inv_layer = inv_layer
        self.function = False
        self.handling_mouse = True
        self.tile_selecter = Sprite('Sprites/Selecter.png')
        self.tile_selecter.scale = 0.049
        self.tile_selecter.position = 400,400#temporary, delete later
        self.add(self.tile_selecter)

    def on_mouse_press(self,x,y,buttons,modifiers):
        if self.handling_mouse:
            map_layer = self.inv_layer.play_layer.map_layer
            x0, y0 = self.tile_selecter.position
            j0, i0 = x0/50-1, -y0/50+len(map_layer.map)
            #try:
            print(i0,j0)
            self.function(self, self.inv_layer.play_layer.effect_layer, target_i = i0, target_j = j0)
            self.parent.remove(self)
            """except:
                print('THE FUNCTION THAT IS GIVEN')
                print('TO THE SELECTING_LAYER')
                print('DOES NOT TAKES THOSE ARGS.')
                print("IT SHOULD GET ONLY THE TILE'S I,J")"""

    def on_mouse_drag(self,x,y,dx,dy,buttons,modifiers):
        pass

    def on_mouse_motion(self, x, y, dx, dy):
        if 1225>=x>=25 and 775>=y>=25 and self.handling_mouse:
            x1, y1 = x-((x+25)%50)+25, y-((y+25)%50)+25
            self.tile_selecter.position = x1,y1


