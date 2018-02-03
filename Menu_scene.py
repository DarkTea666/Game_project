from pyglet.window.key import symbol_string
from pyglet.event import EventDispatcher


from cocos import layer, scene
from cocos.actions import MoveBy, MoveTo, CallFunc, RotateBy
from cocos.sprite import Sprite
from cocos.text import RichLabel

import starting_stats


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
        self.dispatch_event('switch_scene')

FirstLayer.register_event_type('switch_scene')
