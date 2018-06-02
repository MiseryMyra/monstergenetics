import libtcodpy as libtcod
import random
import cfg
import object
import gui
import monst

#module used for handling map generation

class Tile:
    #a tile of the map and its properties
    def __init__(self, blocked, block_sight = None, hp = cfg.TILE_HP, fertile = cfg.LAND_FERTILITY):
        self.blocked = blocked
        self.max_hp = hp
        self.hp = hp
        self.fertile = fertile
 
        #all tiles start unexplored
        self.explored = False
 
        #by default, if a tile is blocked, it also blocks sight
        if block_sight is None: block_sight = blocked
        self.block_sight = block_sight

    def take_damage(self, damage):
        #apply damage if possible

        if damage > 0:
            self.hp -= damage
 
            #dig through wall
            if self.hp <= 0:
                self.blocked = False
                self.block_sight = False
                self.hp = self.max_hp
                gui.message('The wall crumbles!',libtcod.light_orange)

                #update map
                cfg.fov_recompute = True
                
    def leech(self):
        #reduce fertility level
        self.fertile -= 1
    
    def fertilize(self):
        #increase fertility level
        #possibly tie to nutritional value of decomposing corpse?
        self.fertile += 1
 
class Rect:
    #a rectangle on the map. used to characterize a room.
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h
 
    def center(self):
        center_x = (self.x1 + self.x2) / 2
        center_y = (self.y1 + self.y2) / 2
        return (center_x, center_y)
 
    def intersect(self, other):
        #returns true if this rectangle intersects with another one
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1) 
 
def is_blocked(x, y):
    #first test the map tile
    if x in range(cfg.MAP_WIDTH) and y in range(cfg.MAP_HEIGHT):
        if cfg.map[x][y].blocked:
            return True
    else:
        return True
 
    #now check for any blocking objects
    for obj in cfg.objects:
        if obj.blocks and obj.x == x and obj.y == y:
            return True
 
    return False
 
def is_occupied(x, y):
    #first test the map tile
    if x in range(cfg.MAP_WIDTH) and y in range(cfg.MAP_HEIGHT):
        if cfg.map[x][y].blocked:
            return True
    else:
        return True
 
    #now check for any objects
    for obj in cfg.objects:
        if obj.x == x and obj.y == y:
            return True
 
    return False

def create_room(room):
    #go through the tiles in the rectangle and make them passable
    for x in range(room.x1 + 1, room.x2):
        for y in range(room.y1 + 1, room.y2):
            cfg.map[x][y].blocked = False
            cfg.map[x][y].block_sight = False
 
def create_h_tunnel(x1, x2, y):
    #horizontal tunnel. min() and max() are used in case x1>x2
    for x in range(min(x1, x2), max(x1, x2) + 1):
        cfg.map[x][y].blocked = False
        cfg.map[x][y].block_sight = False
 
def create_v_tunnel(y1, y2, x):
    #vertical tunnel
    for y in range(min(y1, y2), max(y1, y2) + 1):
        cfg.map[x][y].blocked = False
        cfg.map[x][y].block_sight = False

def traverse_node(node, dat):
    global bsp_rooms
 
    #Create rooms
    if libtcod.bsp_is_leaf(node):
        minx = node.x + 1
        maxx = node.x + node.w - 1
        miny = node.y + 1
        maxy = node.y + node.h - 1
 
        if maxx == cfg.MAP_WIDTH - 1:
            maxx -= 1
        if maxy == cfg.MAP_HEIGHT - 1:
            maxy -= 1
 
        #If it's False the rooms sizes are random, else the rooms are filled to the node's size
        if cfg.FULL_ROOMS == False:
            minx = libtcod.random_get_int(None, minx, maxx - cfg.MIN_SIZE + 1)
            miny = libtcod.random_get_int(None, miny, maxy - cfg.MIN_SIZE + 1)
            maxx = libtcod.random_get_int(None, minx + cfg.MIN_SIZE - 2, maxx)
            maxy = libtcod.random_get_int(None, miny + cfg.MIN_SIZE - 2, maxy)
 
        node.x = minx
        node.y = miny
        node.w = maxx-minx + 1
        node.h = maxy-miny + 1
 
        #Dig room
        for x in range(minx, maxx + 1):
            for y in range(miny, maxy + 1):
                cfg.map[x][y].blocked = False
                cfg.map[x][y].block_sight = False
 
        #Add center coordinates to the list of rooms
        bsp_rooms.append(((minx + maxx) / 2, (miny + maxy) / 2))
 
    #Create corridors    
    else:
        left = libtcod.bsp_left(node)
        right = libtcod.bsp_right(node)
        node.x = min(left.x, right.x)
        node.y = min(left.y, right.y)
        node.w = max(left.x + left.w, right.x + right.w) - node.x
        node.h = max(left.y + left.h, right.y + right.h) - node.y
        if node.horizontal:
            if left.x + left.w - 1 < right.x or right.x + right.w - 1 < left.x:
                x1 = libtcod.random_get_int(None, left.x, left.x + left.w - 1)
                x2 = libtcod.random_get_int(None, right.x, right.x + right.w - 1)
                y = libtcod.random_get_int(None, left.y + left.h, right.y)
                vline_up(cfg.map, x1, y - 1)
                hline(cfg.map, x1, y, x2)
                vline_down(cfg.map, x2, y + 1)
 
            else:
                minx = max(left.x, right.x)
                maxx = min(left.x + left.w - 1, right.x + right.w - 1)
                x = libtcod.random_get_int(None, minx, maxx)
 
                # catch out-of-bounds attempts
                while x > cfg.MAP_WIDTH - 1:
                        x -= 1
 
                vline_down(cfg.map, x, right.y)
                vline_up(cfg.map, x, right.y - 1)
 
        else:
            if left.y + left.h - 1 < right.y or right.y + right.h - 1 < left.y:
                y1 = libtcod.random_get_int(None, left.y, left.y + left.h - 1)
                y2 = libtcod.random_get_int(None, right.y, right.y + right.h - 1)
                x = libtcod.random_get_int(None, left.x + left.w, right.x)
                hline_left(cfg.map, x - 1, y1)
                vline(cfg.map, x, y1, y2)
                hline_right(cfg.map, x + 1, y2)
            else:
                miny = max(left.y, right.y)
                maxy = min(left.y + left.h - 1, right.y + right.h - 1)
                y = libtcod.random_get_int(None, miny, maxy)
 
                # catch out-of-bounds attempts
                while y > cfg.MAP_HEIGHT - 1:
                         y -= 1
 
                hline_left(cfg.map, right.x - 1, y)
                hline_right(cfg.map, right.x, y)
 
    return True

def vline(map, x, y1, y2):
    if y1 > y2:
        y1,y2 = y2,y1
 
    for y in range(y1,y2+1):
        map[x][y].blocked = False
        map[x][y].block_sight = False
 
def vline_up(map, x, y):
    while y >= 0 and map[x][y].blocked == True:
        map[x][y].blocked = False
        map[x][y].block_sight = False
        y -= 1
 
def vline_down(map, x, y):
    while y < cfg.MAP_HEIGHT and map[x][y].blocked == True:
        map[x][y].blocked = False
        map[x][y].block_sight = False
        y += 1
 
def hline(map, x1, y, x2):
    if x1 > x2:
        x1,x2 = x2,x1
    for x in range(x1,x2+1):
        map[x][y].blocked = False
        map[x][y].block_sight = False
 
def hline_left(map, x, y):
    while x >= 0 and map[x][y].blocked == True:
        map[x][y].blocked = False
        map[x][y].block_sight = False
        x -= 1
 
def hline_right(map, x, y):
    while x < cfg.MAP_WIDTH and map[x][y].blocked == True:
        map[x][y].blocked = False
        map[x][y].block_sight = False
        x += 1
 
def make_map():
    #the list of objects with just the player
    cfg.objects = [cfg.player]
 
    #fill map with "blocked" tiles
    cfg.map = [[ Tile(True)
             for y in range(cfg.MAP_HEIGHT) ]
           for x in range(cfg.MAP_WIDTH) ]
 
    rooms = []
    num_rooms = 0
 
    for r in range(cfg.MAX_ROOMS):
        #random width and height
        w = libtcod.random_get_int(0, cfg.ROOM_MIN_SIZE, cfg.ROOM_MAX_SIZE)
        h = libtcod.random_get_int(0, cfg.ROOM_MIN_SIZE, cfg.ROOM_MAX_SIZE)
        #random position without going out of the boundaries of the map
        x = libtcod.random_get_int(0, 0, cfg.MAP_WIDTH - w - 1)
        y = libtcod.random_get_int(0, 0, cfg.MAP_HEIGHT - h - 1)
 
        #"Rect" class makes rectangles easier to work with
        new_room = Rect(x, y, w, h)
 
        #run through the other rooms and see if they intersect with this one
        failed = False
        for other_room in rooms:
            if new_room.intersect(other_room):
                failed = True
                break
 
        if not failed:
            #this means there are no intersections, so this room is valid
 
            #"paint" it to the map's tiles
            create_room(new_room)
 
            #center coordinates of new room, will be useful later
            (new_x, new_y) = new_room.center()
 
            if num_rooms == 0:
                #this is the first room, where the player starts at
                cfg.player.x = new_x
                cfg.player.y = new_y
            else:
                #all rooms after the first:
                #connect it to the previous room with a tunnel
 
                #center coordinates of previous room
                (prev_x, prev_y) = rooms[num_rooms-1].center()
 
                #draw a coin (random number that is either 0 or 1)
                if libtcod.random_get_int(0, 0, 1) == 1:
                    #first move horizontally, then vertically
                    create_h_tunnel(prev_x, new_x, prev_y)
                    create_v_tunnel(prev_y, new_y, new_x)
                else:
                    #first move vertically, then horizontally
                    create_v_tunnel(prev_y, new_y, prev_x)
                    create_h_tunnel(prev_x, new_x, new_y)
 
            #add some contents to this room, such as monsters
            place_objects(new_room)
 
            #finally, append the new room to the list
            rooms.append(new_room)
            num_rooms += 1
 
    #create stairs at the center of the last room
    if cfg.MAKE_STAIRS:
        cfg.stairs = object.Object(stairs_location[0], stairs_location[1], '>', 'stairs', libtcod.white, always_visible=True)
    else:
        cfg.stairs = object.Object(stairs_location[0], stairs_location[1], cfg.FLOOR_CHAR, ' ', cfg.color_light_ground, always_visible=False)
        
    cfg.objects.append(cfg.stairs)
    cfg.stairs.send_to_back()  #so it's drawn below the monsters

def make_bsp():
    global bsp_rooms
 
    cfg.objects = [cfg.player]
 
    cfg.map = [[Tile(True) for y in range(cfg.MAP_HEIGHT)] for x in range(cfg.MAP_WIDTH)]
 
    #Empty global list for storing room coordinates
    bsp_rooms = []
 
    #New root node
    bsp = libtcod.bsp_new_with_size(0, 0, cfg.MAP_WIDTH, cfg.MAP_HEIGHT)
 
    #Split into nodes
    libtcod.bsp_split_recursive(bsp, 0, cfg.DEPTH, cfg.MIN_SIZE + 1, cfg.MIN_SIZE + 1, 1.5, 1.5)
 
    #Traverse the nodes and create rooms                            
    libtcod.bsp_traverse_inverted_level_order(bsp, traverse_node)
 
    #Random room for the stairs
    stairs_location = random.choice(bsp_rooms)
    bsp_rooms.remove(stairs_location)
    if cfg.MAKE_STAIRS:
        cfg.stairs = object.Object(stairs_location[0], stairs_location[1], '>', 'stairs', libtcod.white, always_visible=True)
    else:
        cfg.stairs = object.Object(stairs_location[0], stairs_location[1], cfg.FLOOR_CHAR, ' ', cfg.color_light_ground, always_visible=False)
    cfg.objects.append(cfg.stairs)
    cfg.stairs.send_to_back()
 
    #Random room for player start
    player_room = random.choice(bsp_rooms)
    bsp_rooms.remove(player_room)
    cfg.player.x = player_room[0]
    cfg.player.y = player_room[1]
 
    #Add monsters and items
    for room in bsp_rooms:
        new_room = Rect(room[0] - cfg.MIN_SIZE/2, room[1] - cfg.MIN_SIZE/2, cfg.MIN_SIZE, cfg.MIN_SIZE)
        place_objects(new_room)
 
    initialize_fov()
 
def random_choice_index(chances):  #choose one option from list of chances, returning its index
    #the dice will land on some number between 1 and the sum of the chances
    dice = libtcod.random_get_int(0, 1, sum(chances))
 
    #go through all chances, keeping the sum so far
    running_sum = 0
    choice = 0
    for w in chances:
        running_sum += w
 
        #see if the dice landed in the part that corresponds to this choice
        if dice <= running_sum:
            return choice
        choice += 1
 
def random_choice(chances_dict):
    #choose one option from dictionary of chances, returning its key
    chances = chances_dict.values()
    strings = chances_dict.keys()
 
    return strings[random_choice_index(chances)]
 
def from_dungeon_level(table):
    #returns a value that depends on level. the table specifies what value occurs after each level, default is 0.
    for (value, level) in reversed(table):
        if cfg.dungeon_level >= level:
            return value
    return 0
 
def place_objects(room):
    #this is where we decide the chance of each monster or item appearing.
 
    #maximum number of monsters per room
    #max_monsters = from_dungeon_level([[4, 1], [5, 4], [6, 6]])
 
    #chance of each monster
    monster_chances = {}
    for name in monst.properties:
        if name != 'player':
            monster_chances[name] = monst.properties[name].chances
 
    #maximum number of items per room
    max_items = from_dungeon_level([[0, 1], [0, 4]])
 
    #chance of each item (by default they have a chance of 0 at level 1, which then goes up)
    item_chances = {}
    item_chances['heal'] = 35  #healing potion always shows up, even if all other items have 0 chance
    item_chances['lightning'] = from_dungeon_level([[25, 4]])
    item_chances['fireball'] =  from_dungeon_level([[25, 6]])
    item_chances['confuse'] =   from_dungeon_level([[10, 2]])
    item_chances['sword'] =     from_dungeon_level([[5, 4]])
    item_chances['shield'] =    from_dungeon_level([[15, 8]])
 
 
    #choose random number of monsters
    choice = random_choice(monster_chances)
    max_monsters = monst.properties[choice].group_size
    num_monsters = libtcod.random_get_int(0, 0, max_monsters)
    
    for i in range(num_monsters):
        #choose random spot for this monster
        x = libtcod.random_get_int(0, room.x1+1, room.x2-1)
        y = libtcod.random_get_int(0, room.y1+1, room.y2-1)
 
        #only place it if the tile is not blocked
        if not is_blocked(x, y):
            object.make_monster(x, y, choice, monst.properties[choice])
 
    #generate plants/food objects
    max_plants = cfg.MAX_STARTING_PLANTS
    num_plants = libtcod.random_get_int(0, 0, max_plants)
 
    for i in range(num_plants):
        #choose random spot for this plant
        x = libtcod.random_get_int(0, room.x1+1, room.x2-1)
        y = libtcod.random_get_int(0, room.y1+1, room.y2-1)
 
        #only place it if the tile is not blocked
        if not is_occupied(x, y):
            object.make_plant(x, y)

    #choose random number of items
    num_items = libtcod.random_get_int(0, 0, max_items)
 
    for i in range(num_items):
        #choose random spot for this item
        x = libtcod.random_get_int(0, room.x1+1, room.x2-1)
        y = libtcod.random_get_int(0, room.y1+1, room.y2-1)
 
        #only place it if the tile is not blocked
        if not is_blocked(x, y):
            choice = random_choice(item_chances)
            if choice == 'heal':
                #create a healing potion
                item_component = object.Item(use_function=cast_heal)
                item = object.Object(x, y, '!', 'healing potion', libtcod.violet, item=item_component)
 
            elif choice == 'lightning':
                #create a lightning bolt scroll
                item_component = object.Item(use_function=cast_lightning)
                item = object.Object(x, y, '#', 'scroll of lightning bolt', libtcod.light_yellow, item=item_component)
 
            elif choice == 'fireball':
                #create a fireball scroll
                item_component = object.Item(use_function=cast_fireball)
                item = object.Object(x, y, '#', 'scroll of fireball', libtcod.light_yellow, item=item_component)
 
            elif choice == 'confuse':
                #create a confuse scroll
                item_component = object.Item(use_function=cast_confuse)
                item = object.Object(x, y, '#', 'scroll of confusion', libtcod.light_yellow, item=item_component)
 
            elif choice == 'sword':
                #create a sword
                equipment_component = object.Equipment(slot='right hand', power_bonus=3)
                item = object.Object(x, y, '/', 'sword', libtcod.sky, equipment=equipment_component)
 
            elif choice == 'shield':
                #create a shield
                equipment_component = object.Equipment(slot='left hand', defense_bonus=1)
                item = object.Object(x, y, '[', 'shield', libtcod.darker_orange, equipment=equipment_component)
 
            cfg.objects.append(item)
            item.send_to_back()  #items appear below other objects
            item.always_visible = True  #items are visible even out-of-FOV, if in an explored area
            
def next_level():
    #advance to the next level
    gui.message('You take a moment to rest, and recover your strength.', libtcod.light_violet)
    cfg.player.fighter.heal(cfg.player.fighter.max_hp / 2)  #heal the player by 50%
 
    cfg.dungeon_level += 1
    gui.message('After a rare moment of peace, you descend deeper into the heart of the dungeon...', libtcod.red)
    make_bsp()  #create a fresh new level!
    initialize_fov()
 
def initialize_fov():
    cfg.fov_recompute = True
 
    #create the FOV map, according to the generated map
    cfg.fov_map = libtcod.map_new(cfg.MAP_WIDTH, cfg.MAP_HEIGHT)
    for y in range(cfg.MAP_HEIGHT):
        for x in range(cfg.MAP_WIDTH):
            libtcod.map_set_properties(cfg.fov_map, x, y, not cfg.map[x][y].block_sight, not cfg.map[x][y].blocked)

 
    libtcod.console_clear(cfg.con)  #unexplored areas start black (which is the default background color)
