from cocos.layer import Layer
from cocos.sprite import Sprite
from cocos.actions import FadeIn, FadeOut, Delay, CallFunc

from observer_class import Observer

from util import util_starting_stats as starting_stats

class EffectLayer(Layer):
    def __init__(self, map_layer, subj1 = False, subj2 = False):
        Layer.__init__(self)

        self.map_layer = map_layer
        self.gases = {}
        self.gases_active = []
        self.strikes = {'normal': Sprite('Sprites/Strike_normal.png')}
        self.progectiles = {}
        for strikename, strike in self.strikes.items():
            strike.scale = 0.05
            strike.opacity = 0
            self.add(strike)
            self.remove(strike)
            self.add(strike)

    def change_position(self, sprite, x, y):
        sprite.position = x, y

    def normal_strike(self, x, y, the_player):
        strike = self.strikes['normal']
        place_strike = CallFunc(self.change_position, strike, x, y) + \
                       FadeIn(0.1) + FadeOut(0.1)
        if the_player:
            strike.do(place_strike)
        else:
            strike.do(Delay(0.2) + place_strike)


