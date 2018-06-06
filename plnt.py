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
                'grass' : Plant(chances=5),
                'sweetgrass' : Plant(color=libtcod.desaturated_lime, nutrition=cfg.BASE_PLANT_NUTRITION*1.5, fp=2, chances=10),
                'bluegrass' : Plant(color=libtcod.desaturated_sky, health=0.2, fp=2, chances=10),
                'shrub' : Plant(char='*', nutrition=cfg.BASE_PLANT_NUTRITION*3, fp=3, chances=10)
             }
