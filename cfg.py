import libtcodpy as libtcod

#module used for configuring settings and initializing globals

VERSION_NUMBER = '0.3.2'

ALL_SEEING = True #displays full map
IGNORE_PLAYER = True #monsters don't target player
XRAY_VISION = True #monsters see through walls
REAL_TIME = True #runs in real time instead of with turns, toggled with r key
CHEBYSHEV_METRIC = False #counts diagonals as a distance of 1 instead of sqrt(2)
DEATH_STATS = False #displays stats of monster upon death
REPRODUCTION_FAILURE = False #displays failed attempts at reproduction
MAKE_STAIRS = False #makes stairs to subsequent levels
PRINT_FPS = False #prints fps to console
 
#actual size of the window
SCREEN_WIDTH = 90
SCREEN_HEIGHT = 50
 
#size of the map
MAP_WIDTH = 90
MAP_HEIGHT = 37
 
#sizes and coordinates relevant for the GUI
BAR_WIDTH = 20
PANEL_HEIGHT = SCREEN_HEIGHT - MAP_HEIGHT
PANEL_Y = SCREEN_HEIGHT - PANEL_HEIGHT
MSG_X = BAR_WIDTH + 2
MSG_WIDTH = SCREEN_WIDTH - BAR_WIDTH - 2
MSG_HEIGHT = PANEL_HEIGHT - 1
INVENTORY_WIDTH = 50
CHARACTER_SCREEN_WIDTH = 30
LEVEL_SCREEN_WIDTH = 40
 
#parameters for dungeon generator
ROOM_MAX_SIZE = 8
ROOM_MIN_SIZE = 5
MAX_ROOMS = 50
DEPTH = 12
MIN_SIZE = 6
FULL_ROOMS = False

#tile properties
FLOOR_CHAR = 250 #looks like this: .
TILE_HP = 100
 
#spell values
HEAL_AMOUNT = 40
LIGHTNING_DAMAGE = 40
LIGHTNING_RANGE = 5
CONFUSE_RANGE = 8
CONFUSE_NUM_TURNS = 10
FIREBALL_RADIUS = 3
FIREBALL_DAMAGE = 25

#monster properties
MAX_TIMER = 24 #highly composite number for uniformity in action at most speeds
COOLDOWN_FACTOR = 1
MIN_COOLDOWN = 120
POPULATION_CAP = 100
OVERPOPULATION_PERCENT = 0.5 #percent of max population considered overpopulated
WANDER_ATTEMPTS = 5
START_NUTRITION = 0.5 #percentage of starting nutrition
CORPSE_MIN_NUTRITION = 0.3 #least percentage of max nutrition that remains in corpse after death
HP_FROM_FOOD = 0.1 #percentage of hp gained from the nutrition of food eaten
MAX_DEX = 20 #maximum dex for damage calculations
MAX_AGGRO = 20 #maximum aggro for scared calculation
CRIT_DIE = 20 #sides of a die used to roll against for crits

#mutations
REPRODUCTION_ATTEMPTS = 5
MUTATE_PROBABILITY = 1.0
MUTATE_FACTOR = 0.2
COLOR_MUTATE = 0.07

#resource properties
MAX_STARTING_PLANTS = 3 #maximum number of plants to initially sprout per room
BASE_PLANT_NUTRITION = 20
PLANT_GROWTH_RATE = 500 #how many turns it takes for a plant to grow larger
PLANT_GROWTH_PROBABILITY = 0.3 #probability that plants will sprout in a turn
NEW_PLANT_RATE = 2 #number of new plants that will sprout
PLANT_CHAR = '\"'
LAND_FERTILITY = 1 #how fertile the land is by default
DECOMPOSITION_RATE = 500 #how many turns it takes before a corpse decomposes
 
#experience and level-ups
LEVEL_UP_BASE = 200000000
LEVEL_UP_FACTOR = 150000000

 
FOV_ALGO = 0  #default FOV algorithm
FOV_LIGHT_WALLS = True  #light walls or not
TORCH_RADIUS = 7
 
LIMIT_FPS = 20  #20 frames-per-second maximum
 
 
color_dark_wall = libtcod.Color(90, 90, 90)
color_light_wall = libtcod.Color(150, 150, 150)
color_dark_ground = libtcod.Color(45, 45, 45)
color_light_ground = libtcod.Color(90, 90, 90)
color_fertile_ground = libtcod.darker_green * 0.7


con = libtcod.console_new(MAP_WIDTH, MAP_HEIGHT)
panel = libtcod.console_new(SCREEN_WIDTH, PANEL_HEIGHT)
 
mouse = libtcod.Mouse()
key = libtcod.Key()

#initialize globals
map = []
fov_map = []
objects = []
objects_map = []
player = []
stairs = []
inventory = []
game_msgs = []
game_state = ''
population = {}
max_population = {}
run_realtime = REAL_TIME
dungeon_level = 1
fov_recompute = True
