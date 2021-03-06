from pyglet.event import EventDispatcher

from cocos import layer
from cocos.text import RichLabel

from util import util_starting_stats
from cocos.director import director
from main_scene import PlayScene
from create_character import Player

class FirstLayer(layer.Layer, EventDispatcher):
    is_event_handler = True
    def __init__(self):
        layer.Layer.__init__(self)
        EventDispatcher.__init__(self)

        self.start_button = RichLabel('Click on a race to choose it')

        self.race_selection_dict = {'Human': (util_starting_stats.Human, 'image'),
                                  'Drwarf': (util_starting_stats.Dwarf, 'image'),
                                    'Elf': (util_starting_stats.Elf, 'image'),
                                    'Orc': (util_starting_stats.Orc, 'image'),
                                    'Goblin': (util_starting_stats.Goblin, 'image'),
                                    'Demon': (util_starting_stats.Demon, 'image'),
                                    'Vampire': (util_starting_stats.Vampire, 'image'),
                                    'Ghost': (util_starting_stats.Ghost, 'image')}
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
                chosen_class = util_starting_stats.Warlock#for now
                player1 = Player(chosen_race, chosen_class)
                first_scene = PlayScene(player1)
                director.push(first_scene)
            button_y -= 100







