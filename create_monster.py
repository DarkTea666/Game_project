from cocos.sprite import Sprite
from cocos.actions import MoveBy, CallFunc

from random import randrange
import json


from util import util_starting_stats
from util.util_starting_stats import All_mobs
from algorithms.algorithms_pathfinding import pathfind_to_target
from algorithms.algorithms_visibility import calculate_visibility
#import loot_tables

class Monster(Sprite): #non-boss

    def __init__(self, image, monster_type, dungeon_level, special_stats = False):
        Sprite.__init__(self, image)

        self.image_path = image
        #Universal attributes:
        self.moves = 0
        self.speed = monster_type.speed
        self.type = monster_type
        self.name = monster_type.name
        self.dungeon_level = dungeon_level
 
        #TO DO: make those a bit random and depend on the dungeon_level
        self.max_health = monster_type.max_health
        self.health = monster_type.max_health
        self.defence = monster_type.defence
        self.damage = monster_type.damage

        self.flying = monster_type.flying
        self.spectral = monster_type.spectral
        self.undead = monster_type.undead
        self.ranged = monster_type.ranged
        self.loot = []

        self.scale = 0.05

    def to_json(obj):
        return {'type': 'Monster', 'image_path': obj.image_path, 'level': obj.dungeon_level, 'moves': obj.moves,
                'speed': obj.speed, 'name': obj.name, 'health': obj.health,
                'defence': obj.defence, 'damage': obj.damage, 'loot': obj.loot,
                'ranged': obj.ranged}
    @classmethod
    def from_json(cls, string):
        attrs = json.loads(string)
        if attrs['type'] == cls.__name__:
            mob = cls(attrs['image_path'], All_mobs[attrs['name']], attrs['level'])
            mob.health = attrs['health'];mob.damage = attrs['damage'];mob.defance = attrs['defence']
            mob.loot = attrs['loot'];mob.ranged = attrs['ranged'];mob.moves = attrs['moves'];mob.speed = attrs['speed']
            return mob
        raise TypeError("Monster's from_json classmethod doesn't work")


    def tile(self):
        p,q = self.position
        return {'i':int(-q/50), 'j':int(p/50-1)}
    #you need to add +len(map_layer.map) to i for this to work
    
    def go(self, d1,d2):
        self.do(actions.MoveBy((d1*50, d2*50)),0.1)
        self.moves += 1

    def close_range_attack(self,opponent):
        opponent.health -= self.damage
        self.moves = self.speed
 

    def close_combat_check(self,player,map_layer):
        directions = [(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]
        key = False
        for x,y in directions:
            if self.tile()['j'] == player.tile()['j']+x and\
               self.tile()['i'] == player.tile()['i']-y:
                key = True
        return key
                

    def check_for_death(self,player):
        result = False
        if self.health < 1: #fills up Vampires and Ghosts
            if player.race == util_starting_stats.Vampire:
                if player.race == Vampire and not self.undead and \
                   player.vampire_attributes['blood_level'] > 10:
                    player.vampire_attributes['blood_level'] += 1
            if player.race == util_starting_stats.Ghost:
                if player.race == Ghost and not self.spectral and \
                   player.ghost_attributes['soul_level'] <= 10:
                    player.ghost_attributes['soul_level'] += 1
            result = True
        return result

            
    def long_range_attack(self,opponent,long_distance_weapon):
        opponent.health -= long_distance_weapon.damage
        self.moves = self.speed

    def check_moves(self):
        if self.moves == self.speed:
            self.moves = 0
            self.turn += 1

    def allow_movement(self):
        self.parent.handling_moves = True

    def move_if_close_range(self):
        map_layer = self.parent.map_layer
        player = self.parent.player
        mobs = self.parent.mobs
        self.moves = 0
        moving_actions = []

        player_is_visible = False
        i_m = self.tile()['i'] + len(map_layer.map)
        j_m = self.tile()['j']
        i_player = player.tile()['i'] + len(map_layer.map)
        j_player = player.tile()['j']
        vis_map = calculate_visibility(i_m, j_m, map_layer)
        if vis_map[i_player][j_player] != '#':
            player_is_visible = True

        if player_is_visible:
            count = 0
            while self.speed != self.moves:
                if self.close_combat_check(player,map_layer):
                    self.close_range_attack(player)
                    print('You got hit by',self.name,'!')
                    self.moves = self.speed
                    x,y = player.race_sprite.position
                    #moving_actions.append(CallFunc(self.parent.effect_layer.normal_strike(x,y)))
                    self.parent.effect_layer.normal_strike(x, y, False)#the one above this is right, but doesn't work.
                else:
                    p,q = 0,0
                    blocked_tiles = []
                    while (p,q) == (0,0) and count <= 8:
                        path = pathfind_to_target(map_layer, self.tile()['i']+len(map_layer.map), self.tile()['j'],
                                           player.tile()['i']+len(map_layer.map), player.tile()['j'], blocked_tiles)
                        y, x = path[0]
                        if self.parent.check_tile_for_mob(x,y)[0]:
                            blocked_tiles.append((y, x))
                        else:
                            i1, j1 = self.tile()['i'] + len(map_layer.map), self.tile()['j']
                            p, q = (x - j1) * 50, -(y - i1) * 50
                            self.moves += 1
                            moving_actions.append(MoveBy((p, q), 0.1))
                        count += 1
                    if count == 9:# an exeption for when a mob is stuck #FIXED
                        self.moves += 1
                        moving_actions.append(MoveBy((p, q), 0.1))

                
        if not player_is_visible:#move randomly
            not_moved_key = True
            while not_moved_key:
                x = randrange(-1,2)
                y = randrange(-1,2)
                if self.parent.check_passability(x,y,self):
                    moving_actions.append(MoveBy((x*50, y*50), 0.1))
                    not_moved_key = False

        result_action = MoveBy((0, 0), 0)
        for action in moving_actions:
            result_action += action
        if mobs.index(self) == len(mobs) - 1:  # allows player to move after last mob
            self.do(result_action + \
                    CallFunc(self.allow_movement))
        else:
            self.do(result_action + \
                    CallFunc(mobs[mobs.index(self) + 1].move_if_close_range))


