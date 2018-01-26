from cocos.layer import Layer
from cocos.sprite import Sprite
from cocos.batch import BatchNode
from cocos.actions import FadeIn, FadeOut, Delay, CallFunc

from observer_class import Observer

import starting_stats

class VisibilityLayer(Layer,Observer):
    def __init__(self, map_layer, subj1 = False, subj2 = False):
        Layer.__init__(self)
        Observer.__init__(self, subject1 = subj1, subject2 = subj2)

        batch = BatchNode()
        self.batch = batch
        self.add(batch)
        self.all_blacked_out_tiles = [[Sprite('Sprites/non_vis.png',
                                position=((j+1)*50, (len(map_layer.map)-i)*50),
                                scale=0.049) for j in range(0,len(map_layer[0]))]
                                      for i in range(0,len(map_layer.map))]
        self.seen_tiles = []
        for row in self.all_blacked_out_tiles:
            for tile in row:
                self.batch.add(tile)
        self.non_vis_tiles = []
        self.map_layer = map_layer

    def draw_player_vision(self, visibility_map):
        for i in range(len(visibility_map)):
            for j in range(len(visibility_map[0])):
                if visibility_map[i][j] != '#':
                    self.all_blacked_out_tiles[i][j].opacity = 0
                    if (i,j) not in self.seen_tiles:
                        self.seen_tiles.append((i,j))
                elif (i,j) in self.seen_tiles:
                    self.all_blacked_out_tiles[i][j].opacity = 150


