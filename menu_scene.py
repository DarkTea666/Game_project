from pyglet.window.key import symbol_string
from pyglet.event import EventDispatcher


from cocos import layer, scene
from cocos.actions import MoveBy, MoveTo, CallFunc, RotateBy
from cocos.sprite import Sprite
from cocos.text import RichLabel

import starting_stats
from cocos.director import director
from main_scene import MainScene

class FirstLayer(layer.Layer, EventDispatcher):
    is_event_handler = True
    def __init__(self):
        layer.Layer.__init__(self)
        EventDispatcher.__init__(self)

        self.start_button = RichLabel('Click on a race to choose it')

        self.race_selection_dict = {'Human': (starting_stats.Human,'image'),
                                  'Drwarf': (starting_stats.Dwarf,'image'),
                                    'Elf': (starting_stats.Elf,'image'),
                                    'Orc': (starting_stats.Orc,'image'),
                                    'Goblin': (starting_stats.Goblin,'image'),
                                    'Demon': (starting_stats.Demon,'image'),
                                    'Vampire': (starting_stats.Vampire,'image'),
                                    'Ghost': (starting_stats.Ghost,'image')}
        button_y = 750
        for race_name, race in self.race_selection_dict.items():
            button = RichLabel(race_name, position=(1000, button_y), font_size=20)
            button_y -= 100
            self.add(button)

    def on_mouse_press(self,x,y,buttons,modifiers):
        button_y = 750
        for button in self.race_selection_dict:
            if 1000<x<1250 and button_y-20<y<button_y+20:
                chosen_race = self.race_selection_dict[button][0]
                print(chosen_race)
                director.push(MainScene(chosen_race = chosen_race))
            button_y -= 100
                                  # later needs to be changed so the player and inventory_layer stay,
                                  #and the mobs and and the map get added to a database
