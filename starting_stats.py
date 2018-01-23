from collections import namedtuple

#----------------------------Race-----------------------------------------------
Race = namedtuple('Race',
                  ['max_health', 'strength', 'speed', 'level_rate',
                   'regen',
                   'hunger', 'gold_hunger', 'blood_thirst', 'race_sprite'])

Human = Race(100,10,1,'level_rate',0.2,100,'none','none','Sprites/Human.png')
Dwarf = Race(150,15,1,'level_rate',0,250,100,'none','img')
Elf = Race(80,8,2,'level_rate',0.3,100,'none','none','Sprites/Human.png')
Ork = Race(90,13,1,'level_rate',0.1,100,'none','none','Sprites/Ork_Warlock.png')
Goblin = Race(60,7,3,'level_rate',0.4,150,150,150,'img')
Demon = Race(130,13,1,'level_rate',0.2,'none','none','none','img')
Vampire = Race(60,6,2,'level_rate',0,'none','none',100,'Sprites/Vampire_Warlock.png')
Ghost = Race(25,10,1,'level_rate',0,'none','none','none','img')

vampire_dict = {'blood_level':0, 'blood_regen':0, 'blood_strength':0}
ghost_dict = {'soul_level':0, 'soul_strength':0, 'soul_decay':0,
              'decay_key':True,'possessing':False}

#------------------------------Class--------------------------------------------
Class = namedtuple('Class',
                   ['pref_weapon_type','pref_armour_type',
                    'max_energy','energy_regen','intellect',
                    'class_dict','class_sprite'])
#if you use an ability: energy -= 1
wizard_dict = 0 #TO DO
warlock_dict = {'max_mana':500, 'mana_regen':10, 'mana':500}#........
elementalist_dict = 0
necromancer_dict = 0
healer_dict = 0

slinger_dict = 0
archer_dict = 0
ninga_dict = 0
crossbow_man_dict = 0

knigth_dict = 0
barbarian_dict = 0
gladiator_dict = 0
paladin_dict = 0
assasin_dict = 0

adventurer_dict = 0
thief_dict = 0
alchemist_dict = 0
herbalist_dict = 0

Wizard = Class('Staff','Cloth',
               5,0.01, 10, wizard_dict,'img')
Warlock = Class('Staff','Light_Leather',
                3, 0.005, 6, warlock_dict,'Sprites/Warlock.png')
Elementalist = Class('Staff','Light_Leather',
                     8, 0.015, 6, elementalist_dict,'img')
Necromancer = Class('Sythe','Cloth',
                    3, 0.01, 7, necromancer_dict,'img')
Healer = Class('Sythe','Cloth',
               4, 0.01, 7, healer_dict,'img')

Slinger = Class('Sling','Heavy_Leather',
                3, 0.01, 3, slinger_dict,'dict')
Archer = Class('Bow','Light_Leather',
               3, 0.01, 4, archer_dict,'img')
Ninga = Class('Shuriken','Light_Leather',
              4, 0.01, 5, ninga_dict,'img')
Crossbow_man = Class('Crossbow','Heavy_Leather',
                     3, 0.01, 3, crossbow_man_dict,'img')

Knigth = Class('Sword','Heavy_Chainmail',
               2, 0.015, 3, knigth_dict, 'img')
Barbarian = Class('Axe','Light_Chainmail',
                  3, 0.01, 1, barbarian_dict, 'img')
Gladiator = Class('Spear','Heavy_Leather',
                  2, 0.01, 2, gladiator_dict, 'img')
Paladin = Class('Hammer','Platemail',
                2, 0.01, 1, paladin_dict, 'img')
Assasin = Class('Dagger','Heavy_Leather',
                3, 0.015, 4, assasin_dict, 'img')

Adventurer = Class('Sword','Light_Chainmail',
                   2, 0.015, 3, adventurer_dict, 'img')
Thief = Class('Dagger','Light_Leather',
              4, 0.01, 4, thief_dict, 'img')
Alchemist = Class('Dagger','Light_Leather',
                  3, 0.01, 6, alchemist_dict, 'img')
Herbalist = Class('Staff','Cloth',
                  3, 0.01, 5, herbalist_dict, 'img')

#--------------------------Monsters---------------------------------------------

Monster_type = namedtuple('Monster_type',
                          ['max_health', 'defence', 'speed', 'damage',
                           'spectral', 'undead', 'flying', 'ranged',
                           'monster_sprite', 'name'])# +special_behaviour?

gnoll_ranged_dict = {'ranged_damage':3,'range':4,'ammunition':10}

Giant_spider = Monster_type(35,3,1,5,False,False,False,False,
                            'Sprites/enemy.png','Giant_spider')
Gnoll_hunter = Monster_type(31,2,1,4,False,False,False,gnoll_ranged_dict,
                            'Sprites/Gnoll_hunter.png','Gnoll_hunter')
Gnoll_warrior = Monster_type(51,5,1,6,False,False,False,False,
                             'img','Gnoll_warrior')


#TO DO: MAKE MORE

#------------------------Items--------------------------------------------------
Weapon = namedtuple('Weapon',
                    ['name','weapon_type','base_damage', 'miss_chance',
                     'req_strength', 'image', 'menu'])

short_sword_menu = ['''This is a plain, but reliable sword.''',
                    '''It doesn't require much strength or skill to wield''']

long_sword_menu = ['''This long, sharp sword is nothing out of the ordinary,''',
                   '''but it can be deadly in the right hands.''']

broad_sword_menu = ['''This sword is very large and deals''',
                    '''huge amounts of damage, but it's''',
                    '''size sometimes makes it miss it's target''']

great_sword_menu = ['''This legendary sword requres enormous amounts''',
                    '''of strength to wield it, but is very''', 
                    '''precise and can cut nearly any foe in two''']

Short_sword = Weapon('Short sword','sword',10, 0.05, 8,
                     'Sprites/Item_short_sword.png', short_sword_menu)
Long_sword = Weapon('Longsword', 'sword', 15, 0.06, 10,
                    'Sprites/Item_long_sword.png', long_sword_menu)
Broad_sword = Weapon('Greatsword', 'sword', 30, 0.1, 15,
                    'Sprites/Item_broad_sword.png', broad_sword_menu)
Great_sword = Weapon('Greatsword', 'sword', 32, 0.03, 18,
                    'Sprites/Item_great_sword.png', great_sword_menu)
#---Sceptres-----
Sceptre = namedtuple('Staff',
                   ['name','base_damage','req_intelligence','max_ammo',
                    'image','menu','strike_effect'])
bluefire_sceptre_menu = ['''This rather ordinary bluefire sceptre does not requre''',
                         '''a lot of inteligence to use. It can hold quite a bit''',
                         '''of charges''']



Bluefire_sceptre = Sceptre('Bluefire sceptre', 5, 3, 5,
                           'Sprites/Item_bluefire_sceptre.png', bluefire_sceptre_menu,
                           [])







                  






              
                    




