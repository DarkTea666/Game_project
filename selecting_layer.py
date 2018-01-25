from cocos.layer import Layer
from cocos.sprite import Sprite

class SelectLayer(Layer):
    is_event_handler = True
    def __init__(self, inv_layer, function):
        Layer.__init__(self)

        self.inv_layer = inv_layer
        self.function = function
        self.selecter = Sprite('Sprites/Selecter.png')
        self.selecter.scale = 0.05
        self.selecter.position = 400,400#temporary, delete later

    def on_mouse_press(self,x,y,buttons,modifiers):
        map_layer = self.inv_layer.play_layer.map_layer
        for i in range(len(map_layer.map)):
            for j in range(len(map_layer[0])):
                if self.selecter.position == ((j+1)*50, (len(map_layer.map)-i)*50):
                    function(i,j)#first make sure the function takes that


