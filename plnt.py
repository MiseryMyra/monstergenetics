#module for defining the initial properties for all the different plant types
import libtcodpy as libtcod
import cfg

class Plant:
    def __init__(self, char=cfg.PLANT_CHAR, color=libtcod.desaturated_green, nutrition=cfg.BASE_PLANT_NUTRITION, health=cfg.HP_FROM_FOOD, fp=1, chances=1):
        self.char = char
        self.color = color
        self.nutrition = nutrition #nutritional content
        self.health = health    #fraction of hp gained from the nutrition of food eaten
        self.fp = fp            #points of fertility it costs to grow
        self.chances = chances  #chances plant will grow, assuming fp is met
        
properties = {
                'grass' : Plant(chances=50),
                'sweetgrass' : Plant(color=libtcod.desaturated_lime, nutrition=int(cfg.BASE_PLANT_NUTRITION*1.5), fp=2, chances=20),
                'bluegrass' : Plant(color=libtcod.desaturated_sky, health=0.2, fp=2, chances=20),
                'shrub' : Plant(char='*', nutrition=cfg.BASE_PLANT_NUTRITION*3, fp=3, chances=20),
                'beach fern' : Plant(char='*', color=libtcod.desaturated_sea, nutrition=int(cfg.BASE_PLANT_NUTRITION*2.5), health=0.2, fp=3, chances=10),
                'amethyst bush' : Plant(char='*', color=libtcod.desaturated_violet, nutrition=int(cfg.BASE_PLANT_NUTRITION*3.5), fp=3, chances=5),
                'sprout' : Plant(char='\'', color=libtcod.desaturated_chartreuse, nutrition=cfg.BASE_PLANT_NUTRITION/2, chances=10),
                'sun aloe' : Plant(char='\'', color=libtcod.desaturated_yellow,  health=0.3, chances=10),
                'bitter lavender' : Plant(char='\'', color=libtcod.desaturated_purple, nutrition=cfg.BASE_PLANT_NUTRITION/2,  health=0.8, chances=3),
                'celery' : Plant(char='`', nutrition=cfg.BASE_PLANT_NUTRITION/3, health=0, chances=15),
                'dawn bean' : Plant(char='`', color=libtcod.desaturated_amber, nutrition=cfg.BASE_PLANT_NUTRITION/2, health=0.3, fp=2, chances=10),
                'dusk pod' : Plant(char='`', color=libtcod.desaturated_magenta, nutrition=cfg.BASE_PLANT_NUTRITION/2, health=0.6, fp=2, chances=3),
                'moss' : Plant(char=',', nutrition=cfg.BASE_PLANT_NUTRITION/3, chances=10),
                'blood algae' : Plant(char=',', color=libtcod.desaturated_red, nutrition=cfg.BASE_PLANT_NUTRITION/3, health=0.5, fp=2, chances=10),
                'golden lichen' : Plant(char=',', color=libtcod.desaturated_amber, nutrition=cfg.BASE_PLANT_NUTRITION/3, health=1, fp=2, chances=3)
             }
