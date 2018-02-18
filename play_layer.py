from pyglet.window.key import symbol_string
from pyglet.event import EventDispatcher

from cocos import layer

from random import randrange
import math

from observer_class import Observer
from algorithms.algorithms_visibility import calculate_visibility
from util import util_starting_stats
from create_monster import Monster

class PlayingLayer(layer.Layer, EventDispatcher, Observer):
    is_event_handler = True

    def __init__(self, player1, map_layer, subj1 = False, subj2 = False):
        layer.Layer.__init__(self)
        EventDispatcher.__init__(self)
        Observer.__init__(self, subject1 = subj1, subject2 = subj2)

        self.handling_moves = True
        self.inv_open = False

        self.map_layer = map_layer
        self.interactive_layer = False
        self.effect_layer = False

        self.player = player1
        self.add(self.player)
        self.player.current_map = self.map_layer.map

        self.mobs = []

        self.this_turn = self.player.turn


        #FOR TESTS: infinite health
        #self.player.health = math.inf

    def spawn_items(self):
        self.interactive_layer.generate_items_open_area()
        #TO DO: MAKE IT SPAWN ITEMS DIFFERENTLY WITH EACH TYPE OF LEVEL


    def spawn_initial_mobs(self):
        i_p = self.player.tile()['i'] + len(self.map_layer.map)
        j_p = self.player.tile()['j']
        vis_map = calculate_visibility(i_p, j_p, self.map_layer)
        self.dispatch_event('draw_player_vision',vis_map)

        max_mobs = self.map_layer.level + 2
        amount_mobs = 0
        for i in range(0,len(self.map_layer.map)):
            for j in range(0,len(self.map_layer.map[0])):
                if self.map_layer[i][j] == 0 and randrange(100)>96 and\
                   len(self.mobs) < max_mobs and \
                   self.player.tile()['j'] != j and \
                   self.player.tile()['i'] + len(self.map_layer.map) != i:
                    amount_mobs += 1
                    mob = Monster(util_starting_stats.Gnoll_hunter.monster_sprite,
                                  util_starting_stats.Gnoll_hunter,
                                  self.map_layer.level)
                    self.mobs.append(mob)
                    mob.position = (j+1)*50, (len(self.map_layer.map)-i)*50
                    self.add(mob)

    def check_tile_for_mob(self,j,i):
        result = [False]
        for mob in self.mobs:
            if mob.tile()['j'] == j and \
               mob.tile()['i'] + len(self.map_layer.map) == i:
                result = [True, mob]
        return result

    def move(self, d1, d2):#NOT CURRENTLY USED
        self.player.direction = (d1, d2)
        for child in self.get_children():
            child.move()
        self.player.move()

    def check_passability(self,x1,y1,called_by_mob = False):
        result = False
        if not called_by_mob:
            i = self.player.tile()['i'] + len(self.map_layer.map) - y1
            j = self.player.tile()['j'] + x1
        else:
            i = called_by_mob.tile()['i'] + len(self.map_layer.map) - y1
            j = called_by_mob.tile()['j'] + x1
        a_mob_here = self.check_tile_for_mob(j,i)[0]
        if self.map_layer[i][j] == 0 and not a_mob_here:
            result = True
        return result

    def do_after_turn(self):
        self.handling_moves = False

        i_p = self.player.tile()['i'] + len(self.map_layer.map)
        j_p = self.player.tile()['j']
        vis_map = calculate_visibility(i_p, j_p, self.map_layer)
        self.dispatch_event('draw_player_vision', vis_map)

        print('turn:',self.player.turn)
        print('health:',self.player.health)
        for mob in self.mobs:
            if mob.check_for_death(self.player):
                self.remove(mob)
                self.mobs.remove(mob)
                print('You killed the',mob.name,'!')

        if self.mobs == []:
            self.handling_moves = True
        if self.mobs != []:
            self.mobs[0].move_if_close_range()

        if self.player.check_for_death() == True:
            self.remove(self.player)
            self.handling_moves = False
            print('You died!')#for now
        if self.mobs == []:
            print('You win!')#for now
        self.this_turn += 1

    def player_do_turn(self, x, y):
        self.player.current_map = self.map_layer.map
        self.player.direction = x,y
        mob_tile = self.check_tile_for_mob(self.player.tile()['j'] + x,
                                           self.player.tile()['i'] - y + len(self.map_layer.map))
        self.player.move_if_possible()

        if  mob_tile[0]:# hit if there is a mob
            mob = mob_tile[1]
            print('You hit the', mob.name, '!')
            self.player.close_range_attack(mob)
            x1, y1 = mob.position
            self.effect_layer.normal_strike(x1, y1, True)
            self.player.check_moves()
            if self.this_turn == self.player.turn - 1:
                self.do_after_turn()
            #TO DO: MAKE IT SO THST THIS IS DONE WITHIN THE PLAYER

    def on_key_press(self, key, modifiers):#move with keys
        buttons = {'D':(1,0), 'E':(1,1), 'W':(0,1), 'Q':(-1,1),
                   'A':(-1,0), 'Z':(-1,-1), 'X':(0,-1), 'C':(1,-1)}
        print(self.handling_moves)
        if self.handling_moves and self.this_turn == self.player.turn:
            if symbol_string(key) in buttons and self.handling_moves:
                x,y = buttons[symbol_string(key)]
                self.player.direction = x, y
                self.player_do_turn(x,y)

        if symbol_string(key) == 'I':#switch to inventory
            if not self.inv_open:
                self.inv_open = True
                self.handling_moves = False
                self.parent.add(self.player.inventory, z = 5)
                self.player.inventory.handling_events = True
            elif self.inv_open:
                self.inv_open = False
                self.handling_moves = True
                self.parent.remove(self.player.inventory)

        if symbol_string(key) == 'P' and self.handling_moves:#pick up item
            for item in self.interactive_layer.items:
                print(item.tile)
                print(len(self.map_layer.map) + self.player.tile()['i'],
                                  self.player.tile()['j'])
                if item.tile == ( len(self.map_layer.map) + self.player.tile()['i'],
                                  self.player.tile()['j'] ):
                    if self.player.inventory.add_to_inventory(item):
                        self.interactive_layer.items.remove(item)
                        self.interactive_layer.remove(item)
                        self.do_after_turn()
                        self.player.turn += 1

PlayingLayer.register_event_type('draw_player_vision')