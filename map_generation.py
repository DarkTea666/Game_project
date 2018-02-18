from cocos.sprite import Sprite
from cocos.layer import Layer
from cocos.batch import BatchNode

from random import randrange

from util import util_starting_stats as starting_stats
from observer_class import Observer

class Tile(Sprite):
    def __init__(self, image, level, passable,
                 water = False,void = False,
                 pillar = False,vegetation = False,
                 cracked = False,floor = False,
                 extend_dict = {'l':0, 'r':0, 'u':0, 'd':0},
                 exit = False, entrance = False):
        super(Tile, self).__init__(image)

        self.level = level
        self.exit = exit
        self.entrance = entrance

        self.passable = passable
        self.water = water
        self.void = void
        self.pillar = pillar
        self.vegetation = vegetation
        self.cracked = cracked
        self.floor = floor
        self.extend_dict = extend_dict


class LevelMap(Layer):#, Observer):
    def __init__(self, level, subject1 = False, subject2 = False):
        Layer.__init__(self)
        #Observer.__init__(self, subject1=player1, subject2=play_layer)

        self.map = []
        self.level = level
        self.special_images = []#for putting non-standart walls and floor
                                #in the level database
        batch1 = BatchNode()
        self.batch1 = batch1
        self.add(batch1)
        batch2 = BatchNode()
        self.batch2 = batch2
        self.add(batch2)

    def __getitem__(self, key):
        return self.map[key]

    def in_bounds(self,i,j):
        if 0 <= i < len(self.map) and 0 <= j < len(self[0]):
            return True
        else:
            return False

    def neighbors(self,i,j):#just returns the values 
        n = []
        directions = [(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]
        for x, y in directions:
            if self.in_bounds(i+y,j+x):
                n.append(self[i+y][j+x])
        return n

    def neighbor_tiles(self,i,j):#returns tuples of values and tile coords
        values = []              #example:(5,5,0)coords:5,5 value:0
        directions = [(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]
        for x,y in directions:
            if self.in_bounds(i+y,j+x):
                values.append((i+y,j+x,self[i+y][j+x]))
        return values 

    def get_special_image(self,i,j):#for database-storing maps
        result = 0
        for (p,q,image) in self.special_images:
            if (p,q) == (i,j):
                result = image
        return result
            
    
    def smooth(self):
        new_map = self.map
        for i in range(len(self.map)):
            for j in range(len(self[0])):
                if self[i][j] == 1:
                    if self.neighbors(i,j).count(0) > 5:
                        new_map[i][j] = 0
                if self[i][j] == 0:
                    if self.neighbors(i,j).count(0) < 3:
                        new_map[i][j] = 1
        self.map = new_map

    def mark(self): #for tests
        for i in range(len(self.map)):
            print(*self[i])

    def generate_map(self,draw_map=True):
        if self.level == 1:
            self.map = [[0 if randrange(100)>45 else 1 for j
                         in range(0,22)] for i in range(0,13)]
            for i in range(10):
                self.smooth()

            for i in range(0,len(self.map)):#wall borders
                self[i].insert(0,1)
                self[i].append(1)
            self.map.append([1 for x in range(0,len(self.map[0]))])
            self.map.insert(0,[1 for x in range(0,len(self.map[0]))])
            for i in range(5,11):#for better connectivity
                for j in range(8,14):
                    self[i][j] = 0
            
            T0 = Tile('Sprites/Temp_grass_floor.png',1,True,
                      extend_dict =  {'l':'Sprites/Right_ext_grass.png',
                                     'r':'Sprites/Left_ext_grass.png',
                                     'u':0,
                                     'd':0})
            T1 = Tile('Sprites/Forest_wall.png',1,False,
                      extend_dict = {'l':0,
                                     'r':0,
                                     'u':0,
                                     'd':0})
            if draw_map:
                self.draw_main_map(T0,T1,True,True)

            exit_key = True
            while exit_key:#make this a little bit better
                for i in range(0,len(self.map)):
                    for j in range(0,len(self.map[0])):
                        if self.neighbors(i,j).count(0) == 3 and self[i][j] == 1 and exit_key:
                            if randrange(10) == 5:
                                exit_key = False
                                image = Sprite('Sprites/Forest_exit_tile.png')
                                image.scale = 0.05
                                image.position = (j+1)*50, (len(self.map)-i)*50
                                self.add(image)#.batch1.add(image)
                                self.special_images.append((i,j,image))
                                self[i][j] = 'f'

            #extra stuff:
            for i in range(0,len(self.map)):
                for j in range(0,len(self.map[0])):
                    if self.neighbors(i,j) == [0,0,0,0,0,0,0,0] and \
                     self[i][j] == 0 and randrange(100)>90 and \
                     (i != 7 or j != 11) and (i != 6 or j != 12):
                        self[i][j] = 1
                        image = 'Sprites/Forest_Boulder_tile_decor.png'
                        self.special_images.append((i,j,image))
                        
                        boulder = Tile(image,1,False)
                        boulder.position = (j+1)*50, (len(self.map)-i)*50
                        boulder.scale = 0.049
                        self.add(boulder)#.batch1.add(boulder)

            
    def draw_main_map(self,T0,T1,overlays1,overlays0):
        extends = [[{'l':0, 'r':0, 'u':0, 'd':0}
                    for i in range(0,len(self.map[0]))]
                    for j in range(0,len(self.map))]
        d = {'l':(0, -1), 'r':(0, 1), 'd':(1, 0), 'u':(-1, 0)}

        for i in range(0,len(self.map)):
            for j in range(0,len(self.map[0])):
                
                if self[i][j] == 1:
                    tile = Tile(T1.image,T1.level,T1.passable,
                                extend_dict = T1.extend_dict)
                    if overlays1:#mark overlaying textures
                        for direction, displacement in d.items():
                            x, y = displacement
                            if T1.extend_dict[direction] != 0 and \
                               self.in_bounds(i+x,j+y) and \
                               self[i+x][j+y] == 0:
                                extends[i][j][direction] = \
                                       Sprite(T1.extend_dict[direction])
                                
                elif self[i][j] == 0:
                    tile = Tile(T0.image,T0.level,T0.passable,
                                extend_dict = T0.extend_dict)
                    if overlays0:#mark overlaying textures
                        for direction, displacement in d.items():
                            x, y = displacement
                            if T0.extend_dict[direction] != 0 and \
                               self.in_bounds(i+x,j+y) and \
                               self[i+x][j+y] == 1:
                                extends[i][j][direction] = \
                                       Sprite(T0.extend_dict[direction])
                #draw the tile
                tile.position = (j+1)*50, (len(self.map)-i)*50
                tile.scale = 0.049
                self.batch1.add(tile)

        #draw the overlays
        for i in range(0,len(self.map)):
            for j in range(0,len(self.map[0])):
                for direction, displacement in d.items():
                    x, y = displacement
                    if extends[i][j][direction] != 0:
                        ext = extends[i][j][direction]
                        ext.position = (j+1+y)*50, (len(self.map)-i-x)*50
                        ext.scale = 0.049
                        self.batch2.add(ext)
                    
                    
                    
                    
                    
                    
                    
                                   
            
        
            

    






