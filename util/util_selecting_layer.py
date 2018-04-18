from cocos.layer import Layer
from cocos.sprite import Sprite

from functools import partial

from algorithms.algorithms_visibility import calculate_visibility

class SelectLayer(Layer):
    is_event_handler = True
    def __init__(self, inv_layer):
        Layer.__init__(self)

        self.inv_layer = inv_layer
        self.map_layer = self.inv_layer.play_layer.map_layer
        self.player = self.inv_layer.play_layer.player

        self.function = False
        self.handling_mouse = True

        j_p, i_p = self.player.tile()['i'] + len(self.map_layer.map), self.player.tile()['j']
        self.vis_map = calculate_visibility(j_p, i_p, self.map_layer, visualise_in_text=True)

        self.tile_selecter = Sprite('Sprites/Selecter.png')
        self.tile_selecter.scale = 0.049
        self.tile_selecter.position = self.player.tile()['j'], self.player.tile()['i'] + len(self.map_layer.map)
        #if self.vis_map[i1][j1] == '#':
        #    self.tile_selecter.opacity == 0
        self.add(self.tile_selecter)


    def on_mouse_press(self,x,y,buttons,modifiers):
        if self.handling_mouse:
            x0, y0 = self.tile_selecter.position
            j0, i0 = x0/50-1, -y0/50+len(self.map_layer.map)
            #try:
            print(i0,j0)
            self.function(self, self.inv_layer.play_layer.effect_layer, target_i = i0, target_j = j0)
            self.parent.remove(self)
            self.inv_layer.play_layer.handling_moves = True

    def on_mouse_motion(self, x, y, dx, dy):
        print(x,y)
        if 1225>=x>=25 and 775>=y>=25 and self.handling_mouse:
            x1, y1 = x-((x+25)%50)+25, y-((y+25)%50)+25
            j1, i1 = int(x1/50)-1, -int(y1/50) + len(self.map_layer.map)
            print(self.vis_map[i1][j1])
            if self.vis_map[i1][j1] != '#':
                self.tile_selecter.position = x1,y1



