from cocos.layer import Layer
from cocos.sprite import Sprite
from cocos.actions import MoveBy, CallFunc
from pyglet.event import EventDispatcher
from cocos.director import director

from functools import partial
import random

from observer_class import Observer
from util import util_starting_stats
from main_scene import PlayScene
from database_ideas import move_level_to_database

class Player(Layer, EventDispatcher, Observer):

    def __init__(self, Race, Class):
        Layer.__init__(self)
        EventDispatcher.__init__(self)
        #Race attributes
        self.race = Race
        self.max_health = Race.max_health
        self.health = Race.max_health
        self.strength = Race.strength
        self.damage = Race.strength/3
        self.defence = 0
        self.level_rate = Race.level_rate#TO DO
        self.regen = Race.regen

        #Special race attributes
        self.max_hunger = Race.hunger
        self.max_gold_hunger = Race.gold_hunger
        self.max_blood_thirst = Race.blood_thirst
        self.hunger = Race.hunger
        self.gold_hunger = Race.gold_hunger
        self.blood_thirst = Race.blood_thirst
        
        self.vampire_attributes = False 
        self.ghost_attributes = False

        #Class_attributes
        self.max_energy = Class.max_energy
        self.energy = Class.max_energy
        self.energy_regen = Class.energy_regen
        self.intellect = Class.intellect

        self.class_dict = Class.class_dict

        self.pref_weapon_type = Class.pref_weapon_type
        self.pref_armour_type = Class.pref_armour_type
        
        #Universal attributes
        self.inventory = False
        self.equip_layer = False

        self.turn = 0
        self.moves = 0
        self.speed = Race.speed
        self.level = 1
        self.exp = 0
        self.direction = (0, 0)#could be used for turning while walking
        self.current_map = False
        
        self.class_sprite = Sprite(Class.class_sprite)
        self.class_sprite.scale = 0.05
        self.add(self.class_sprite)

        self.race_sprite = Sprite(Race.race_sprite)
        self.race_sprite.scale = 0.05
        self.add(self.race_sprite)

    #DISPATCER EVENTS                      #events only transport values None and True
    def move_if_possible(self):
        play_layer = self.inventory.play_layer 
        map_layer = play_layer.map_layer
        play_layer_do_after_turn = partial(self.dispatch_event,'do_after_turn')
        x,y = self.direction
        
        self.update_damage()
        self.update_sprite_direction()
        
        i_p,j_p = self.tile()['i']+len(map_layer.map), self.tile()['j']
        tile_stepping_on = map_layer.tile_map[i_p-y][j_p+x]
        start_next_level = True
        if tile_stepping_on.exit == 'unlocked' or tile_stepping_on.entrance == 'unlocked':
            if tile_stepping_on.exit == 'unlocked':
                d = 1
                print('exit')
            if tile_stepping_on.entrance == 'unlocked' and map_layer.level != 1:
                d = -1
                print('entrance')
            if tile_stepping_on.entrance == 'unlocked' and map_layer.level == 1:
                start_next_level = False
                print('One does not leave the first level like that!')
            
            if start_next_level:
                move_level_to_database(map_layer, play_layer.mobs)#
            
                play_layer.mobs = []
                play_layer.remove(self)
                play_layer.player_killed = True
                del play_layer
                this_scene = self.parent.parent
                this_scene = self.parent.parent
                next_scene = PlayScene(self, level = this_scene.level+d,
                    levels_visited = this_scene.levels_visited, prev_level = this_scene.level)
                del self
                director.run(next_scene)
        #
        passability = play_layer.check_passability(x, y)#this was a dispatch_event ealier
        if passability:
            print('Moves:',self.moves)
            if self.moves != self.speed - 1:
                self.class_sprite.do(MoveBy((x * 50, y * 50), 0.1))
                self.race_sprite.do(MoveBy((x * 50, y * 50), 0.1))
                self.moves += 1
            elif self.moves == self.speed - 1:
                self.class_sprite.do(MoveBy((x * 50, y * 50), 0.1))
                self.race_sprite.do(MoveBy((x * 50, y * 50), 0.1) + CallFunc(play_layer_do_after_turn))
                self.moves += 1
            self.check_moves()
        #TO DO: dispatch a play_layer event that checks for a mob and hits it
        #maybe?

    def tile(self):
        p,q = self.race_sprite.position
        return {'i':int(-q/50), 'j':int(p/50-1)}

    #ACTIVE

    def check_for_death(self):
        result = False
        if self.health <= 0:
            result = True
        return result

    def close_range_attack(self,opponent, miss_chance = 0):
        if random.random() <= miss_chance:
            print('You missed!')
        else:
            opponent.health -= self.damage
            self.moves = self.speed

    def long_range_attack(self,opponent,long_distance_weapon):
        opponent.health -= long_distance_weapon.damage
        self.moves = self.speed

    def update_damage(self):
        self.damage = int(self.strength/3) 
        if self.equip_layer.equipment_dict['weapon'][0] != False:
            self.damage +=  self.equip_layer.equipment_dict['weapon'][0][0].damage
        #also add the ring buffs after I add rings

    def update_sprite_direction(self):
        if self.direction[0] == 1:
            self.race_sprite.scale_x = 1
            self.class_sprite.scale_x = 1 
        if self.direction[0] == -1:
            self.race_sprite.scale_x = -1
            self.class_sprite.scale_x = -1

            
    #PASSIVE
    def check_moves(self):# do I just NOT do that anywhere?
        if self.moves == self.speed:
            self.moves = 0
            self.turn += 1

    def add_hunger(self):
        hungers = [self.hunger, self.gold_hunger, self.blood_thirst]
        max_hungers = [self.max_hunger,
                       self.max_gold_hunger,
                       self.max_blood_thirst]
        if self.hunger != 'none':
            self.hunger -= 100/self.max_hunger
            if self.hunger <= 0:
                self.hunger = 0
        if self.gold_hunger != 'none':
            self.gold_hunger -= 100/self.max_gold_hunger
            if self.gold_hunger <= 0:
                self.gold_hunger = 0
        if self.blood_thirst != 'none':
            self.blood_thirst -= 100/self.max_blood_thirst
            if self.blood_thirst <= 0:
                self.blood_thirst = 0

    def add_regen(self):
        self.health += self.regen
        if self.health > self.max_health:
            self.health = self.max_health
            
    def check_hunger(self):#for regen or decay
        hungers = [self.hunger, self.gold_hunger, self.blood_thirst]
        max_hungers = [self.max_hunger,
                       self.max_gold_hunger,
                       self.max_blood_thirst]
        self.health -= hungers.count(0)

        key = True
        for i in range(0,3):
            if hungers[i] != 'none' and hungers[i] < max_hungers[i]-20:
                key = False
        if key:
            self.add_regen()

    #VAMPIRE ATTRIBUTES

    def add_blood_regen(self):
        self.health += self.vampire_attributes['blood_regen']
        if self.health > self.max_health:
            self.health = self.max_health

    def add_blood_strength(self):
        self.damage += self.vampire_attributes['blood_strength']

    def do_if_vampire(self):
        if self.race == util_starting_stats.Vampire:
            self.vampire_attributes = util_starting_stats.vampire_dict
            self.vampire_attributes['blood_strength'] = self.vampire_attributes['blood_level']/10
            self.vampire_attributes['blood_strength'] = self.vampire_attributes['blood_level']

            self.add_blood_regen
            self.add_blood_strength

    #fills up in a monster method on death


Player.register_event_type('do_after_turn')

