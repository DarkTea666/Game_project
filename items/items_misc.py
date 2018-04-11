from items.items_base import Item

level_key_menu1 = "This level "
level_key_menu2 = " key has magical properties which "
level_key_menu3 = "enable you to unlock the next level"

norm_key_menu = "this key opens something on level"

#TODO: make chests, special interact_layer objects that are not items.
class Key(Item):#chest should check if key is in inventory
    def __init__(self, name, image, tile, level, chest_object):
        menu = norm_key_menu + level
        Item.__init__(self, name, image, tile, menu, {'Drop': self.Drop})

        self.inv_type = 'all'
        self.level = level
        self.object = chest_object

class Food(Item):
    def __init__(self, name, image, tile, level, menu, adds_hunger = 20):
        menu = menu + 'This ' + name + 'adds' + adds_hunger + 'hunger'
        tem.__init__(self, name, image, tile, menu, 
                {'Drop':self.Drop, 'Eat':self.Eat})
        self.adds_hunger = adds_hunger
        self.inv_type = 'all'

    def Eat(self):
        inv_layer = self.inv_layer
        player = self.inv_layer.play_layer.player
        now_hunger = player.hunger
        player.hunger += self.adds_hunger
        if player.hunger > player.max_hunger:
            player.hunger = player.max_hunger
        self.delete_from_inventory()
        print('You ate the ', self.name, ' and it gave you ', player.hunger - now_hunger, ' hunger')#to log
        

class LevelKey(Item):
    def __init__(self, name, image, tile, level):
        menu = [level_key_menu1 + str(level) + level_key_menu2, level_key_menu3]
        Item.__init__(self, name, image, tile, menu,
                      {'Drop': self.Drop, 'Unlock Level': self.Unlock_Level})

        self.inv_type = 'all'
        self.level = level
                

    def Unlock_Level(self):#TODO: in map: if tile.entrance == unlocked and player walks in: load next level scene
        play_layer = self.inv_layer.play_layer
        player = play_layer.player
        map_layer = play_layer.map_layer
        ip, jp = player.tile()['i']+len(map_layer.map), player.tile()['j']
        close_tiles = map_layer.neighbor_Tile_objs(ip,jp)
        door_is_here = False
        for tile in close_tiles:
            if tile.level == self.level:
                if tile.exit == 'locked':#maybe instead remove ths tile and relace it with another with an
                    print('You have unlocked the next level.')#appropriate image?
                    exit_image = 'Sprites/'
                    tile.exit = 'unlocked' 
                    #new_exit = Tile(exit_image, self.level, True, exit='unlocked')
                    door_is_here = True
                    #change the image too?
                elif tile.exit == 'unlocked':
                    door_is_here = True
                    print('This level has already been unlocked')
        if not door_is_here:
            print('This key is too far away to use.')






