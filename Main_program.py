from cocos import scene
from cocos.director import director

import menu_scene


if __name__ == '__main__':

    director.init(width=1250, height=800, autoscale=True, resizable=True)

    first_layer = menu_scene.FirstLayer()
    menu_scene = scene.Scene(first_layer)

    director.show_FPS = True

    #profile.run('director.run(main_scene)', sort='cumtime')
    director.run(menu_scene)

