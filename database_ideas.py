from cocos.sprite import Sprite
import json
from json import JSONEncoder
import sqlite3

from create_monster import Monster
from map_generation import Tile

def _default(self, obj):
    return getattr(obj.__class__, "to_json", _default.default)(obj)
_default.default = JSONEncoder().default
JSONEncoder.default = _default

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
                json_tile = json.dumps(map_layer.tile_map[i][j])
                db.execute(insert_tile,[i,j,map_layer.level,json_tile])
        for mob in mobs:
            i = mob.tile()['i']+len(map_layer.map)
            j = mob.tile()['j']
            json_mob = json.dumps(mob)
            db.execute(insert_mob,[i,j,map_layer.level,json_mob])
        db.commit()


def find_level_size(tiles):
    max_i, max_j = 0,0
    for tile in tiles:
        i,j,_,_ = tile
        if max_i < i:
            max_i = i
        if max_j < j:
            max_j = j
    return(max_i+1, max_j+1)

def restore_level_from_database(map_layer):#TODO: check that this works in main_scene. remove play_layer, remamber,
    #TODO: items are not saved, and should dissapear when loading a laval for a second time. then restore mobs
    with sqlite3.connect('map_save.db') as db:
        tiles_ = db.execute(select_level_tiles, [map_layer.level])
        tiles = []
        for tile in tiles_:#the cursor itself is only iterable once
            i,j,level,tile_text = tile
            tiles.append( [i, j, level, Tile.from_json(tile_text)] )
        max_ij = find_level_size(tiles)
        map_layer.map = [ [ [] for j in range(0,max_ij[1]) ] for i in range(0,max_ij[0])]
        map_layer.tile_map = [ [ [] for j in range(0,max_ij[1]) ] for i in range(0,max_ij[0])]

        for tile in tiles:
            i, j, level, tile_obj = tile
            map_layer.tile_map[i][j] = tile_obj
            if tile_obj.passable == True:
                map_layer[i][j] = 0
                T0 = map_layer.tile_map[i][j]
            elif tile_obj.passable == False:
                map_layer[i][j] = 1
                T1 = map_layer.tile_map[i][j]
            if tile_obj.exit == True:
                map_layer[i][j] = 'f'
            elif tile_obj.entrance == True:
                map_layer[i][j] = 'b'#as in forward and backwards

        map_layer.draw_map(T0, T1, overlays1 = True, overlays0 = True)

def restore_mobs_from_database(play_layer,map_layer):
    with sqlite3.connect('map_save.db') as db:
        mobs_ = db.execute(select_level_mobs, [map_layer.level])
        mobs = []
        for mob in mobs_:#the cursor itself is only iterable once
            i,j,level,mob_text = mob
            mob = (i, j, level, Monster.from_json(mob_text))
            mobs.append(mob)
        m_len = len(map_layer.map)
        for mob in mobs:
            i, j, level, actual_mob = mob
            actual_mob.position = (j+1)*50, (m_len-i)*50
            play_layer.add(actual_mob)
            play_layer.mobs.append(actual_mob)

