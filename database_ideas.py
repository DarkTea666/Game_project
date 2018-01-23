import sqlite3

create_tile_table = '''
CREATE TABLE
IF NOT EXISTS
tiles(
    i INTEGER,
    j INTEGER,
    value INTEGER,
    level INTEGER,
    image TEXT);'''

create_mob_table = '''
CREATE TABLE
IF NOT EXISTS
mobs(
    i INTEGER,
    j INTEGER,
    level INTEGER,
    health INTEGER,
    mob_type TEXT);'''

insert_tile = '''
INSERT INTO
tiles
VALUES(?,?,?,?,?);'''

insert_mob = '''
INSERT INTO
mobs
VALUES(?,?,?,?,?);'''

select_level = '''
SELECT *
FROM tiles
WHERE level = ?'''

select_level_mobs = '''
SELECT *
FROM mobs
WHERE level = ?'''

def move_level_to_database(map_layer,mobs,num):
    with sqlite3.connect('map_save.db') as db:
        db.execute(create_tile_table)
        db.execute(create_mob_table)

        for i in range(0,len(map_layer.map)):
            for j in range(0,len(map_layer.map[0])): 
                db.execute(insert_tile,[i,j,map_layer[i][j],map_layer.level,
                                        map_layer.get_special_image(i,j)])
        for mob in mobs:
            i = mob.tile()['i']+len(map_layer.map)
            j = mob.tile()['j']
            db.execute(insert_mob,[i,j,map_layer.level,
                                   mob.health, mob.name])#we get the type from
                                                         #the name
        db.commit()#for now
        for tile in db.execute(select_level,[num]):
            print(tile)
        for mob in db.execute(select_level_mobs,[num]):
            print(mob) 
        
                                   
                                   
                                          
#TO DO: MAKE A LEVEL FROM   







