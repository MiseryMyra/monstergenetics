#module for defining the initial properties for all the different monsters
import libtcodpy as libtcod
import cfg

class Monster:
    def __init__(self, char, color, hp, pw, df, dx, sp, pr, lk, sc=1, ag=1, chances=1, group_size=1):
        self.char = char
        self.color = color
        self.hp = hp #hit points
        self.pw = pw #power
        self.df = df #defense
        self.dx = dx #dex
        self.sp = sp #speed
        self.pr = pr #perception
        self.lk = lk #luck
        self.sc = sc #social impulse
        self.ag = ag #aggression
        self.chances = chances
        self.group_size = group_size
        
properties = {
                'player' : Monster('@', libtcod.white, 100, 100, 100, 20, 100, 100, 100),
                'asmu' : Monster('a', libtcod.light_blue, 20, 3, 0, 3, 5, 5, 6, 8, 4, chances=300, group_size=5),
                'qunat' : Monster('q', libtcod.light_red, 25, 5, 1, 11, 6, 6, 4, 4, 10, chances=300, group_size=4),
                'jowiv' : Monster('j', libtcod.light_yellow, 30, 4, 7, 5, 2, 5, 3, 10, 7, chances=300, group_size=4),
                'zaeif' : Monster('Z', libtcod.light_cyan, 40, 10, 0, 4, 9, 5, 7, 2, 3, chances=200, group_size=3),
                'linorl' : Monster('L', libtcod.light_green, 45, 8, 3, 8, 7, 7, 9, 9, 10, chances=200, group_size=3),
                'miirloc' : Monster('M', libtcod.light_magenta, 60, 12, 5, 6, 3, 6, 2, 4, 2, chances=200, group_size=2),
                'wirqen\'kaak' : Monster('&', libtcod.lighter_violet, 80, 15, 7, 6, 10, 8, 1, 8, 10, chances=150),
                'aecix' : Monster(143, libtcod.lightest_grey, 150, 25, 10, 10, 20, 15, 10, 1, 10)
                }
