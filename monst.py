#module for defining the initial properties for all the different monsters
import libtcodpy as libtcod
import cfg

class Monster:
    def __init__(self, char, name, color, hp, pw, df, dx, sp, pr, lk, chances = 0):
        self.char = char
        self.name = name
        self.color = color
        self.hp = hp
        self.pw = pw
        self.df = df
        self.dx = dx
        self.sp = sp
        self.pr = pr
        self.lk = lk
        self.chances = chances
        
properties = {
                'asmu' : Monster('a', 'asmu', libtcod.light_blue, 20, 3, 0, 3, 5, 5, libtcod.random_get_int(0,0,10)),
                'qunat' : Monster('q', 'qunat', libtcod.light_red, 25, 5, 1, 11, 6, 6, libtcod.random_get_int(0,0,10)),
                'qunat' : Monster('q', 'qunat', libtcod.light_red, 25, 5, 1, 11, 6, 6, libtcod.random_get_int(0,0,10)),
                'qunat' : Monster('q', 'qunat', libtcod.light_red, 25, 5, 1, 11, 6, 6, libtcod.random_get_int(0,0,10)),
                'qunat' : Monster('q', 'qunat', libtcod.light_red, 25, 5, 1, 11, 6, 6, libtcod.random_get_int(0,0,10)),
                'qunat' : Monster('q', 'qunat', libtcod.light_red, 25, 5, 1, 11, 6, 6, libtcod.random_get_int(0,0,10)),
                'qunat' : Monster('q', 'qunat', libtcod.light_red, 25, 5, 1, 11, 6, 6, libtcod.random_get_int(0,0,10))
                }