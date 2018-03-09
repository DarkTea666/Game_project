from cocos.sprite import Sprite
import json
import sqlite3

from create_monster import Monster
from map_generation import Tile

create_tile_table = '''
CREATE TABLE
IF NOT EXISTS
tiles(
    i INTEGER,
    j INTEGER,
    level INTEGER,
    properties TEXT);'''

create_mob_table = '''
CREATE TABLE
IF NOT EXISTS
mobs(
    i INTEGER,
    j INTEGER,
    level INTEGER,
    properties TEXT);'''

insert_tile = '''
INSERT INTO
tiles
VALUES(?,?,?,?);'''

insert_mob = '''
INSERT INTO
mobs
VALUES(?,?,?,?);'''

select_level_tiles = '''
SELECT *
FROM tiles
WHERE level = ?'''

select_level_mobs = '''
SELECT *
FROM mobs
WHERE level = ?'''

del_mobs = '''DROP TABLE mobs'''
del_tiles = '''DROP TABLE tiles'''

def encode_tile(obj):
    if isinstance(obj, Tile):
        return {'__Tile__':True, 'image':obj.image, 'level':obj.level, 'exit':obj.exit,
                'entrance':obj.entrance, 'passable':obj.passable, 'water':obj.water,
                'void':obj.void, 'vegetation':obj.vegetation, 'cracked':obj.cracked,
                'extend_dict':obj.extend_dict}
    raise TypeError(repr(obj) + " is not JSON serializable")

def as_tile(dct):
    if '__Tile__' in dct:
        return Tile(dct['image'], dct['level'], dct['passable'], exit=dct['exit'], entrance=dct['entrance'],
                    water=dct['water'], void=dct['void'], vegetation=dct['vegetation'], cracked=dct['cracked'],
                    extend_dict=dct['extend_dict'])
    return dct

def encode_mob(obj):
    if isinstance(obj, Monster):
        return {}#TODO: change to attrs
    raise TypeError(repr(obj) + " is not JSON serialisable")

def clear_level_database():
    with sqlite3.connect('map_save.db') as db:
        db.execute(del_mobs)
        db.execute(del_tiles)

def move_level_to_database(map_layer,mobs):
    with sqlite3.connect('map_save.db') as db:
        db.execute(create_tile_table)
        db.execute(create_mob_table)
        for i in range(0,len(map_layer.map)):
            for j in range(0,len(map_layer.map[0])):
                json_tile = json.dumps()#TODO: finish this. remake the way the level restores
                #TODO: from map_layer.tile_map
                db.execute(insert_tile,[i,j,map_layer.level,json_tile])
        for mob in mobs:
            i = mob.tile()['i']+len(map_layer.map)
            j = mob.tile()['j']
            db.execute(insert_mob,[i,j,map_layer.level,
                                   mob.health, mob.name])
        db.commit()


def find_level_size(tiles):
    max_i, max_j = 0,0
    for tile in tiles:
        i,j,_,_,_ = tile
        if max_i < i:
            max_i = i
        if max_j < j:
            max_j = j
    return(max_i+1, max_j+1)

def restore_level_from_database(map_layer):
    with sqlite3.connect('map_save.db') as db:
        tiles_ = db.execute(select_level_tiles, [map_layer.level])
        tiles = []
        for tile in tiles_:#the cursor itself is only iterable once
            tiles.append(tile)
        max_ij = find_level_size(tiles)
        map_layer.map = [ [ [] for j in range(0,max_ij[1]) ] for i in range(0,max_ij[0])]
        T0 = Tile('Sprites/Temp_grass_floor.png', 1, True,extend_dict={'l': 'Sprites/Right_ext_grass.png',
                                                        'r': 'Sprites/Left_ext_grass.png','u': 0,'d': 0})
        T1 = Tile('Sprites/Forest_wall.png', 1, False,extend_dict={'l': 0,'r': 0,'u': 0,'d': 0})
        for tile in tiles:
            i, j, value, level, image = tile
            map_layer[i][j] = value
        for row in map_layer.map:#for now
            print(row)

        map_layer.draw_main_map(T0, T1, overlays1 = True, overlays0 = True)
        for tile in tiles:#TODO: remove that
            image = tile[4]
            if image != '0':
                i,j = tile[0], tile[1]
                pos = (j+1)*50, (len(map_layer.map)-i)*50
                print(image)
                special_sprite = Sprite(image, position = pos, scale = 0.049)
                map_layer.add(special_sprite)
        #make adjustments to decorations and exits/entrances

def restore_mobs_from_database(play_layer):
    with sqlite3.connect('map_save.db') as db:
        mobs = db.execute(select_level_mobs, [map_layer.level])
        mobs_list = []
        for mob in mobs:
            actual_mob = Monster()

        #finish this







