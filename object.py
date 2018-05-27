import libtcodpy as libtcod
import math
import random
import cfg
import monst
import gui

#module for object classes and related functions

class Object:
    #this is a generic object: the player, a monster, an item, the stairs...
    #it's always represented by a character on screen.
    def __init__(self, x, y, char, name, color, blocks=False, always_visible=False, corpse=False, fighter=None, ai=None, item=None, equipment=None):
        self.x = x
        self.y = y
        self.char = char
        self.name = name
        self.color = color
        self.blocks = blocks
        self.always_visible = always_visible
        self.corpse = corpse
        self.fighter = fighter
        if self.fighter:  #let the fighter component know who owns it
            self.fighter.owner = self
 
        self.ai = ai
        if self.ai:  #let the AI component know who owns it
            self.ai.owner = self
 
        self.item = item
        if self.item:  #let the Item component know who owns it
            self.item.owner = self
 
        self.equipment = equipment
        if self.equipment:  #let the Equipment component know who owns it
            self.equipment.owner = self
 
            #there must be an Item component for the Equipment component to work properly
            self.item = Item()
            self.item.owner = self
 
    def move(self, dx, dy):
        #move by the given amount, if the destination is not blocked
        #no moving off screen
        if self.x + dx in range(cfg.MAP_WIDTH) and self.y + dy in range(cfg.MAP_HEIGHT):
            if not is_blocked(self.x + dx, self.y + dy):
                self.x += dx
                self.y += dy

            #try digging
            elif cfg.map[self.x + dx][self.y + dy].blocked:
                gui.message(self.name.capitalize() + ' digs at the wall.',libtcod.light_grey)
                if self.fighter:
                    cfg.map[self.x + dx][self.y + dy].take_damage(max(self.fighter.power,1))
                else:
                    cfg.map[self.x + dx][self.y + dy].take_damage(1)

                if not cfg.map[self.x + dx][self.y + dy].blocked:
                    #clear the tile once it's dug out
                    if libtcod.map_is_in_fov(cfg.fov_map, self.x + dx, self.y + dy) or cfg.ALL_SEEING:
                        libtcod.console_put_char_ex(cfg.con, self.x + dx, self.y + dy, cfg.FLOOR_CHAR, cfg.color_light_ground, libtcod.black)
 
    def move_towards(self, target_x, target_y):
        #vector from this object to the target, and distance
        dx = target_x - self.x
        dy = target_y - self.y
        
        if cfg.CHEBYSHEV_METRIC:
            distance = max(abs(dx), abs(dy))
        else:
            distance = math.sqrt(dx ** 2 + dy ** 2)
 
        #normalize it to length 1 (preserving direction), then round it and
        #convert to integer so the movement is restricted to the map grid
        dx = int(round(dx / distance))
        dy = int(round(dy / distance))
        self.move(dx, dy)
        
    def move_away(self, target_x, target_y):
        #vector from this object to the target, and distance
        dx = -target_x + self.x
        dy = -target_y + self.y
        
        if cfg.CHEBYSHEV_METRIC:
            distance = max(abs(dx), abs(dy))
        else:
            distance = math.sqrt(dx ** 2 + dy ** 2)
 
        #normalize it to length 1 (preserving direction), then round it and
        #convert to integer so the movement is restricted to the map grid
        dx = int(round(dx / distance))
        dy = int(round(dy / distance))
        self.move(dx, dy)
        
    def move_astar(self, target):
        #Create a FOV map that has the dimensions of the map
        fov = libtcod.map_new(cfg.MAP_WIDTH, cfg.MAP_HEIGHT)
 
        #Scan the current map each turn and set all the walls as unwalkable
        for y1 in range(cfg.MAP_HEIGHT):
            for x1 in range(cfg.MAP_WIDTH):
                libtcod.map_set_properties(fov, x1, y1, not cfg.map[x1][y1].block_sight, not cfg.map[x1][y1].blocked)
 
        #Scan all the objects to see if there are objects that must be navigated around
        #Check also that the object isn't self or the target (so that the start and the end points are free)
        #The AI class handles the situation if self is next to the target so it will not use this A* function anyway   
        for obj in cfg.objects:
            if obj.blocks and obj != self and obj != target:
                #Set the tile as a wall so it must be navigated around
                libtcod.map_set_properties(fov, obj.x, obj.y, True, False)
 
        #Allocate a A* path
        #The 1.41 is the normal diagonal cost of moving, it can be set as 0.0 if diagonal moves are prohibited
        if cfg.CHEBYSHEV_METRIC:
            my_path = libtcod.path_new_using_map(fov, 1)
        else:
            my_path = libtcod.path_new_using_map(fov, 1.41)
 
        #Compute the path between self's coordinates and the target's coordinates
        libtcod.path_compute(my_path, self.x, self.y, target.x, target.y)
 
        #Check if the path exists, and in this case, also the path is shorter than 100 tiles
        #The path size matters if you want the monster to use alternative longer paths (for example through other rooms) if for example the player is in a corridor
        #It makes sense to keep path size relatively low to keep the monsters from running around the map if there's an alternative path really far away        
        if not libtcod.path_is_empty(my_path) and libtcod.path_size(my_path) < 100:
            #Find the next coordinates in the computed full path
            x, y = libtcod.path_walk(my_path, True)
            if x or y:
                #Set self's coordinates to the next path tile
                self.x = x
                self.y = y
        else:
            #Keep the old move function as a backup so that if there are no paths (for example another monster blocks a corridor)
            #it will still try to move towards the player (closer to the corridor opening)
            self.move_towards(target.x, target.y)  
 
        #Delete the path to free memory
        libtcod.path_delete(my_path)
        
    def move_astar_pos(self, pos_x, pos_y):
        #Create a FOV map that has the dimensions of the map
        fov = libtcod.map_new(cfg.MAP_WIDTH, cfg.MAP_HEIGHT)
 
        #Scan the current map each turn and set all the walls as unwalkable
        for y1 in range(cfg.MAP_HEIGHT):
            for x1 in range(cfg.MAP_WIDTH):
                libtcod.map_set_properties(fov, x1, y1, not cfg.map[x1][y1].block_sight, not cfg.map[x1][y1].blocked)
 
        #Scan all the objects to see if there are objects that must be navigated around
        #Check also that the object isn't self or the target (so that the start and the end points are free)
        #The AI class handles the situation if self is next to the target so it will not use this A* function anyway   
        for obj in cfg.objects:
            if obj.blocks and obj != self:
                #Set the tile as a wall so it must be navigated around
                libtcod.map_set_properties(fov, obj.x, obj.y, True, False)
 
        #Allocate a A* path
        #The 1.41 is the normal diagonal cost of moving, it can be set as 0.0 if diagonal moves are prohibited
        if cfg.CHEBYSHEV_METRIC:
            my_path = libtcod.path_new_using_map(fov, 1)
        else:
            my_path = libtcod.path_new_using_map(fov, 1.41)
 
        #Compute the path between self's coordinates and the target's coordinates
        libtcod.path_compute(my_path, self.x, self.y, pos_x, pos_y)
 
        #Check if the path exists, and in this case, also the path is shorter than 100 tiles
        #The path size matters if you want the monster to use alternative longer paths (for example through other rooms) if for example the player is in a corridor
        #It makes sense to keep path size relatively low to keep the monsters from running around the map if there's an alternative path really far away        
        if not libtcod.path_is_empty(my_path) and libtcod.path_size(my_path) < 100:
            #Find the next coordinates in the computed full path
            x, y = libtcod.path_walk(my_path, True)
            if x or y:
                #Set self's coordinates to the next path tile
                self.x = x
                self.y = y
        else:
            #Keep the old move function as a backup so that if there are no paths (for example another monster blocks a corridor)
            #it will still try to move towards the player (closer to the corridor opening)
            self.move_towards(pos_x, pos_y)  
 
        #Delete the path to free memory
        libtcod.path_delete(my_path)
        
    def run_away(self, target):
        #moves away from target
        max_distance = 0
        positions = []
        
        #check all available positions one can move to
        #make a list of all the best positions one can move to
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if not is_blocked(self.x + dx, self.y + dy):
                    if positions == []:
                        positions.append((self.x + dx, self.y + dy))
                    else:
                        dist = distance_between(self.x + dx, self.y + dy, target.x, target.y)
                        if dist > max_distance:
                            positions = [(self.x + dx, self.y + dy)]
                            max_distance = dist
                        elif dist == max_distance:
                            positions.append((self.x + dx, self.y + dy))
                            
        if positions != []:
            #pick a random position as they are all equally good
            (x, y) = random.choice(positions)
            self.move(x - self.x, y - self.y)
            
        else:
            #no viable moves, revert to backup
            self.move_away(target.x, target.y)
 
    def distance_to(self, other):
        #return the distance to another object
        dx = other.x - self.x
        dy = other.y - self.y
        
        if cfg.CHEBYSHEV_METRIC:
            distance = max(abs(dx), abs(dy))
        else:
            distance = math.sqrt(dx ** 2 + dy ** 2)
        
        return distance
 
    def distance(self, x, y):
        #return the distance to some coordinates
        dx = x - self.x
        dy = y - self.y
        
        if cfg.CHEBYSHEV_METRIC:
            distance = max(abs(dx), abs(dy))
        else:
            distance = math.sqrt(dx ** 2 + dy ** 2)
            
        return distance
        
    def look_around(self, radius):
        #return a list of visible objects in a given radius
        found = []
                
        #compute fov
        if not cfg.XRAY_VISION:
            #Create a FOV map that has the dimensions of the map
            fov = libtcod.map_new(cfg.MAP_WIDTH, cfg.MAP_HEIGHT)
            
            #Scan the current map each turn and set all the walls as unwalkable
            for y1 in range(cfg.MAP_HEIGHT):
                for x1 in range(cfg.MAP_WIDTH):
                    libtcod.map_set_properties(fov, x1, y1, not cfg.map[x1][y1].block_sight, not cfg.map[x1][y1].blocked)
            
            libtcod.map_compute_fov(fov, self.x, self.y, radius, cfg.FOV_LIGHT_WALLS, cfg.FOV_ALGO)
        
        #make a list of objects in fov besides self
        for obj in cfg.objects:
            if not cfg.XRAY_VISION:
                if libtcod.map_is_in_fov(fov, obj.x, obj.y) and obj != self:
                    #ignore player
                    if not cfg.IGNORE_PLAYER or obj != cfg.player:
                        found.append(obj)
                    
            elif self.distance_to(obj) <= radius and obj != self:
                #ignore player
                if not cfg.IGNORE_PLAYER or obj != cfg.player:
                    found.append(obj)
                
        return found
        
    def nearest_object(self, radius, near_objects, fighter, item, name, different):
        #return the nearest visible object matching given parameters
        #near_objects: list of visible objects
        #fighter: is a fighter, item: is an item
        #name: matches name, blank name matches all
        #different: is a different name than self
        nearest_obj = None
        nearest_distance = radius + 1
        
        for obj in near_objects:
            #if fighter and item are both true, it must be both
            if fighter == (obj.fighter != None) or (item and (obj.item != None)):
                if name == obj.name or name == '':
                    if ((not different) or obj.name != self.name):
                        dist = self.distance_to(obj)
                        if dist < nearest_distance:
                            nearest_obj = obj
                            nearest_distance = dist
                            
        return nearest_obj
 
    def send_to_back(self):
        #make this object be drawn first, so all others appear above it if they're in the same tile.
        cfg.objects.remove(self)
        cfg.objects.insert(0, self)
 
    def draw(self):
        #only show if it's visible to the player; or it's set to "always visible" and on an explored tile
        if (libtcod.map_is_in_fov(cfg.fov_map, self.x, self.y) or
                (self.always_visible and cfg.map[self.x][self.y].explored) or cfg.ALL_SEEING):
            #set the color and then draw the character that represents this object at its position
            libtcod.console_set_default_foreground(cfg.con, self.color)
            libtcod.console_put_char(cfg.con, self.x, self.y, self.char, libtcod.BKGND_NONE)
 
    def clear(self):
        #erase the character that represents this object
        if libtcod.map_is_in_fov(cfg.fov_map, self.x, self.y) or cfg.ALL_SEEING:
            libtcod.console_put_char_ex(cfg.con, self.x, self.y, cfg.FLOOR_CHAR, cfg.color_light_ground, libtcod.black)
 
 
class Fighter:
    #combat-related properties and methods (monster, player, NPC).
    def __init__(self, properties, death_function=None):
        self.base_max_hp = properties.hp
        self.hp = properties.hp
        self.base_defense = properties.df
        self.base_power = properties.pw
        self.base_dex = properties.dx
        self.base_speed = properties.sp
        self.timer = libtcod.random_get_int(0, 0, cfg.MAX_TIMER) #initially desynced timers
        self.base_perception = properties.pr
        self.base_luck = properties.lk
        self.xp = calculate_xp(properties.hp, properties.df, properties.pw, properties.dx, properties.sp, properties.pr, properties.lk)
        self.death_function = death_function
        self.max_cooldown = calculate_cooldown(properties.hp, properties.df, properties.pw, properties.dx, properties.sp, properties.pr, properties.lk)
        self.cooldown = self.max_cooldown
        self.max_nutrition = calculate_nutrition(properties.hp, properties.df, properties.pw, properties.dx, properties.sp, properties.pr, properties.lk)
        self.nutrition = int(self.max_nutrition*cfg.START_NUTRITION)
        self.calories = calculate_hunger(properties.hp, properties.df, properties.pw, properties.dx, properties.sp, properties.pr, properties.lk)
        self.starving = False
        self.social = properties.sc
        self.aggro = properties.ag
        self.carry = None
 
    @property
    def power(self):  #return actual power, by summing up the bonuses from all equipped items
        bonus = sum(equipment.power_bonus for equipment in get_all_equipped(self.owner))
        return self.base_power + bonus
 
    @property
    def defense(self):  #return actual defense, by summing up the bonuses from all equipped items
        bonus = sum(equipment.defense_bonus for equipment in get_all_equipped(self.owner))
        return self.base_defense + bonus
 
    @property
    def max_hp(self):  #return actual max_hp, by summing up the bonuses from all equipped items
        bonus = sum(equipment.max_hp_bonus for equipment in get_all_equipped(self.owner))
        return self.base_max_hp + bonus

    @property
    def dex(self):  #return actual dexterity, by summing up the bonuses from all equipped items
        bonus = sum(equipment.dex_bonus for equipment in get_all_equipped(self.owner))
        return self.base_dex + bonus
        
    @property
    def speed(self):  #return actual speed, by summing up the bonuses from all equipped items
        bonus = sum(equipment.speed_bonus for equipment in get_all_equipped(self.owner))
        return self.base_speed + bonus

    @property
    def perception(self):  #return actual perception, by summing up the bonuses from all equipped items
        bonus = sum(equipment.perception_bonus for equipment in get_all_equipped(self.owner))
        return self.base_perception + bonus

    @property
    def luck(self):  #return actual luck, by summing up the bonuses from all equipped items
        bonus = sum(equipment.luck_bonus for equipment in get_all_equipped(self.owner))
        return self.base_luck + bonus
        
    @property
    def scared(self): #return true if monster is scared based on remaining hp and aggro
        hp_percent = float(self.hp) / self.max_hp
        scared_threshhold = float(cfg.MAX_AGGRO - self.aggro) / cfg.MAX_AGGRO
        if hp_percent <= scared_threshhold:
            return True
        else:
            return False
        
    def wait(self):
        #wait until timer is up to make a move and reduce cooldown
        self.timer = self.timer - (self.speed + 1) #zero speed still moves
        #cooldown
        if self.cooldown > 0:
            self.cooldown -= 1
            
    def wander(self):
        position = random_nearby_tile(self.owner.x, self.owner.y, cfg.WANDER_ATTEMPTS)
        
        if position:
            (x, y) = position
            
            dx = x - self.owner.x
            dy = y - self.owner.y
            
            self.owner.move(dx, dy)
 
    def attack(self, target):
        #a simple formula for attack damage

        #critical hit
        if libtcod.random_get_int(0, 0, self.luck) > libtcod.random_get_int(0, 0, cfg.CRIT_DIE):
            crit = 2
        else:
            crit = 1

        min_power = int(float(min(self.dex, cfg.MAX_DEX))/cfg.MAX_DEX * self.power)
        min_defense = int(float(min(target.fighter.dex, cfg.MAX_DEX))/cfg.MAX_DEX * target.fighter.defense)
        damage = libtcod.random_get_int(0, min_power * crit, self.power * crit) - libtcod.random_get_int(0, min_defense, target.fighter.defense)
 
        if damage > 0:
            #make the target take some damage
            #plural
            if damage > 1:
                if crit > 1:
                    gui.message(self.owner.name.capitalize() + ' critically attacks ' + target.name + ' for ' + str(damage) + ' hit points!')
                else:
                    gui.message(self.owner.name.capitalize() + ' attacks ' + target.name + ' for ' + str(damage) + ' hit points.')

            #singular
            else:
                if crit > 1:
                    gui.message(self.owner.name.capitalize() + ' critically attacks ' + target.name + ' for ' + str(damage) + ' hit point!')
                else:
                    gui.message(self.owner.name.capitalize() + ' attacks ' + target.name + ' for ' + str(damage) + ' hit point.')

            target.fighter.take_damage(damage)
        else:
            #lucky last chance at nonzero damage
            if crit > 1 or libtcod.random_get_int(0, 0, self.luck) > libtcod.random_get_int(0, 0, target.fighter.luck):
                gui.message(self.owner.name.capitalize() + ' barely attacks ' + target.name + ' for 1 hit point.')
                target.fighter.take_damage(1)
            else:
                gui.message(self.owner.name.capitalize() + ' attacks ' + target.name + ' but it has no effect!')
 
    def take_damage(self, damage):
        #apply damage if possible
        if damage > 0:
            self.hp -= damage
 
            #check for death. if there's a death function, call it
            if self.hp <= 0:
                function = self.death_function
                if function is not None:
                    function(self.owner)
 
                #if self.owner != cfg.player:  #yield experience to the player
                    #cfg.player.fighter.xp += self.xp
                    
    def hunger(self):
        #lose nutrition, lose health if starving
        if self.nutrition > 0:
            self.nutrition -= self.calories
            
        else:
            #displays message when first starts starving
            if not self.starving:
                self.starving = True
                gui.message(self.owner.name.capitalize() + ' is starving!', libtcod.light_amber)

            self.take_damage(1)
 
    def heal(self, amount):
        #heal by the given amount, without going over the maximum
        self.hp += amount
        if self.hp > self.max_hp:
            self.hp = self.max_hp
            
    def eat(self, food):
        #eat some food, recover nutrition (no more than max) and some health
        self.nutrition += food.item.nutrition
        
        health = int(food.item.nutrition * cfg.HP_FROM_FOOD)
        self.heal(health)
        
        if self.nutrition > self.max_nutrition:
            self.nutrition = self.max_nutrition
            
        #no longer starving
        if self.starving:
            self.starving = False
            
        gui.message(self.owner.name.capitalize() + ' eats the ' + food.name + ' for ' + str(food.item.nutrition) + ' nutrition.', libtcod.light_azure)
            
        #remove food after being eaten
        if food in cfg.objects:
            cfg.objects.remove(food)
            
        if food == self.carry:
            self.carry = None
            
    def take(self, food):
        #pick up the food, if not already carrying some
        if not self.carry:
            self.carry = food
            gui.message(self.owner.name.capitalize() + ' picks up the ' + self.carry.name + '.', libtcod.light_azure * 0.7)
            
            #remove food after being picked up
            cfg.objects.remove(food)
            
    def give(self, friend):
        #gives food to friend
        friend.carry = self.carry
        gui.message(self.owner.name.capitalize() + ' gives the ' + self.carry.name + ' to ' + self.owner.name + '.', libtcod.light_azure * 0.7)

        #remove food from inventory
        self.carry = None
        
    def reproduce(self, mate):
        #make another instance of the fighter with properties from self and mate
        #properties are randomly mutated as well
        monster = self.owner
        location = random_nearby_tile(monster.x, monster.y, cfg.REPRODUCTION_ATTEMPTS)
        
        #more likely to fail if in a cramped area
        if location:
            (x, y) = location
            #calculate average between partners, then mutate
            hp = mutate((self.max_hp + mate.max_hp)/2, cfg.MUTATE_PROBABILITY, cfg.MUTATE_FACTOR)
            defense = mutate((self.defense + mate.defense)/2, cfg.MUTATE_PROBABILITY, cfg.MUTATE_FACTOR)
            power = mutate((self.power + mate.power)/2, cfg.MUTATE_PROBABILITY, cfg.MUTATE_FACTOR)
            dex = mutate((self.dex + mate.dex)/2, cfg.MUTATE_PROBABILITY, cfg.MUTATE_FACTOR)
            speed = mutate((self.speed + mate.speed)/2, cfg.MUTATE_PROBABILITY, cfg.MUTATE_FACTOR)
            perception = mutate((self.perception + mate.perception)/2, cfg.MUTATE_PROBABILITY, cfg.MUTATE_FACTOR)
            luck = mutate((self.luck + mate.luck)/2, cfg.MUTATE_PROBABILITY, cfg.MUTATE_FACTOR)
            social = mutate((self.social + mate.social)/2, cfg.MUTATE_PROBABILITY, cfg.MUTATE_FACTOR)
            aggro = mutate((self.aggro + mate.aggro)/2, cfg.MUTATE_PROBABILITY, cfg.MUTATE_FACTOR)
            
            #set new color
            color = color_mutate(monster.color, mate.owner.color, cfg.MUTATE_PROBABILITY, cfg.COLOR_MUTATE)
            
            properties = monst.Monster(monster.char, color, hp, power, defense, dex, speed, perception, luck, social, aggro)
            
            #always created with maxed out stats
            make_monster(x, y, monster.name, properties)
            
            #update population
            update_population(monster.name)
            
            gui.message(self.owner.name.capitalize() + ' reproduced!', libtcod.light_green)
            
        else:
            gui.message(self.owner.name.capitalize() + ' tried to reproduce, but failed.', libtcod.light_green * 0.7)


class Food:
    #food properties
    def __init__(self, nutrition=10):
        self.nutrition = nutrition
        self.age = 1
        
    def increase_nutrition(self, nutrition):
        self.nutrition += mutate(nutrition,1,0.2)
    
    def decrease_nutrition(self, nutrition):
        self.nutrition -= mutate(nutrition,1,0.2)
    
    #plants grow over time
    def grow(self):
        self.increase_nutrition(cfg.BASE_PLANT_NUTRITION)
        self.owner.color = self.owner.color*1.2
        self.age = 1
    
    #corpses rot over time
    def decompose(self):
        cfg.objects.remove(self.owner)
        
    def age_up(self):
        self.age += 1
        if self.owner.corpse == True:
            if self.age >= cfg.DECOMPOSITION_RATE:
                self.decompose()
        else:
            if self.age >= cfg.PLANT_GROWTH_RATE:
                self.grow()

        
                    
 
class BasicMonster:
    #AI for a basic monster.
    def take_turn(self):
        #a basic monster takes its turn. sight based on perception
        monster = self.owner
        
        #wait until timer is out
        if monster.fighter.timer > 0:
            monster.fighter.wait()
            
        else:
            radius = monster.fighter.perception
            near_objects = monster.look_around(radius)
            enemy = monster.nearest_object(radius, near_objects, fighter=True, item=False, name='', different=True)
            friend = monster.nearest_object(radius, near_objects, fighter=True, item=False, name=monster.name, different=False)
            food = monster.nearest_object(radius, near_objects, fighter=False, item=True, name='', different=False)
            
            #food is priority when starving
            if monster.fighter.starving:
                if monster.fighter.carry:
                    monster.fighter.eat(monster.fighter.carry)
                
                #don't cannibalize if very high social
                elif food and (monster.name not in food.name or monster.fighter.social <10):
                    #move toward food if far away
                    if monster.distance_to(food) >= 2:
                        monster.move_astar(food)
     
                    #close enough, eat
                    else:
                        monster.fighter.eat(food)

                #low social and very high aggro will try to kill and eat each other when starving
                elif friend and (monster.fighter.social <= 4 or monster.fighter.aggro >=10):
                    if monster.distance_to(friend) >=2:
                        monster.move_astar(friend)
                    
                    #close enough, attack
                    elif friend.fighter.hp > 0:
                        monster.fighter.attack(friend)
                
			#fight enemies that are literally right next to you
            elif enemy and (monster.distance_to(enemy) < 2 and enemy.fighter.hp > 0):
                monster.fighter.attack(enemy)
			
            #choose enemy over friend
            elif enemy and friend and monster.fighter.aggro >= monster.fighter.social:
            
                #if high aggression, move toward enemy
                if monster.distance_to(enemy) >= 2 and not monster.fighter.scared:
                    monster.move_astar(enemy)

                #if low aggression, run from enemy
                else:
                    monster.run_away(enemy)

                    
            #only friend, or choose friend over enemy
            elif friend and ((friend.fighter.starving and monster.fighter.carry != None) or (friend.fighter.cooldown == 0 and cfg.population[monster.name] < cfg.POPULATION_CAP)):
            
                #move toward friend if far away
                if monster.distance_to(friend) >= 2:
                    monster.move_astar(friend)
                    
                #close enough, share food
                elif friend.fighter.starving and monster.fighter.carry:
                    monster.fighter.give(friend.fighter)
     
                #close enough, mate
                elif not friend.fighter.starving:
                    monster.fighter.reproduce(friend.fighter)
                    monster.fighter.cooldown = monster.fighter.max_cooldown
                    friend.fighter.cooldown = friend.fighter.max_cooldown
                
            elif enemy:
     
                #if high aggression, move toward enemy
                if monster.distance_to(enemy) >= 2 and not monster.fighter.scared:
                    monster.move_astar(enemy)

                #if low aggression, run from enemy
                else:
                    monster.run_away(enemy)

            #get food, does not cannibalize corpses unless starving
            elif food and monster.name not in food.name:
                if (monster.fighter.nutrition < monster.fighter.max_nutrition/2) or (monster.fighter.carry == None and food.name != 'plant'):
            
                    #move toward food if far away
                    if monster.distance_to(food) >= 2:
                        monster.move_astar(food)
     
                    #close enough, eat
                    elif monster.fighter.carry == None and food.name != 'plant':
                        monster.fighter.take(food)

                    else:
                        monster.fighter.eat(food)
                        
                else:
                    monster.fighter.wander()

            else:
                #randomly wander otherwise
                monster.fighter.wander()
                
            #cooldown
            if monster.fighter.cooldown > 0:
                monster.fighter.cooldown -= 1
                
            #reset timer
            monster.fighter.timer += cfg.MAX_TIMER
            #lose hunger or starve
            monster.fighter.hunger()

 
class ConfusedMonster:
    #AI for a temporarily confused monster (reverts to previous AI after a while).
    def __init__(self, old_ai, num_turns=cfg.CONFUSE_NUM_TURNS):
        self.old_ai = old_ai
        self.num_turns = num_turns
 
    def take_turn(self):
        if self.num_turns > 0:  #still confused...
            #move in a random direction, and decrease the number of turns confused
            self.owner.move(libtcod.random_get_int(0, -1, 1), libtcod.random_get_int(0, -1, 1))
            self.num_turns -= 1
 
        else:  #restore the previous AI (this one will be deleted because it's not referenced anymore)
            self.owner.ai = self.old_ai
            gui.message('The ' + self.owner.name + ' is no longer confused!', libtcod.red)
 
class Item:
    #an item that can be picked up and used.
    def __init__(self, use_function=None):
        self.use_function = use_function
 
    def pick_up(self):
        #add to the player's inventory and remove from the map
        if len(cfg.inventory) >= 26:
            gui.message('Your inventory is full, cannot pick up ' + self.owner.name + '.', libtcod.red)
        else:
            cfg.inventory.append(self.owner)
            cfg.objects.remove(self.owner)
            gui.message('You picked up a ' + self.owner.name + '!', libtcod.green)
 
            #special case: automatically equip, if the corresponding equipment slot is unused
            equipment = self.owner.equipment
            if equipment and get_equipped_in_slot(equipment.slot) is None:
                equipment.equip()
 
    def drop(self):
        #special case: if the object has the Equipment component, dequip it before dropping
        if self.owner.equipment:
            self.owner.equipment.dequip()
 
        #add to the map and remove from the player's inventory. also, place it at the player's coordinates
        cfg.objects.append(self.owner)
        cfg.inventory.remove(self.owner)
        self.owner.x = cfg.player.x
        self.owner.y = cfg.player.y
        gui.message('You dropped a ' + self.owner.name + '.', libtcod.yellow)
 
    def use(self):
        #special case: if the object has the Equipment component, the "use" action is to equip/dequip
        if self.owner.equipment:
            self.owner.equipment.toggle_equip()
            return
 
        #just call the "use_function" if it is defined
        if self.use_function is None:
            gui.message('The ' + self.owner.name + ' cannot be used.')
        else:
            if self.use_function() != 'cancelled':
                cfg.inventory.remove(self.owner)  #destroy after use, unless it was cancelled for some reason
 
class Equipment:
    #an object that can be equipped, yielding bonuses. automatically adds the Item component.
    def __init__(self, slot, power_bonus=0, defense_bonus=0, max_hp_bonus=0, speed_bonus=0, dex_bonus=0, perception_bonus=0, luck_bonus=0):
        self.power_bonus = power_bonus
        self.defense_bonus = defense_bonus
        self.max_hp_bonus = max_hp_bonus
        self.speed_bonus = speed_bonus
        self.dex_bonus = dex_bonus
        self.perception_bonus = perception_bonus
        self.luck_bonus = luck_bonus
 
        self.slot = slot
        self.is_equipped = False
 
    def toggle_equip(self):  #toggle equip/dequip status
        if self.is_equipped:
            self.dequip()
        else:
            self.equip()
 
    def equip(self):
        #if the slot is already being used, dequip whatever is there first
        old_equipment = get_equipped_in_slot(self.slot)
        if old_equipment is not None:
            old_equipment.dequip()
 
        #equip object and show a message about it
        self.is_equipped = True
        gui.message('Equipped ' + self.owner.name + ' on ' + self.slot + '.', libtcod.light_green)
 
    def dequip(self):
        #dequip object and show a message about it
        if not self.is_equipped: return
        self.is_equipped = False
        gui.message('Dequipped ' + self.owner.name + ' from ' + self.slot + '.', libtcod.light_yellow)
        
def get_equipped_in_slot(slot):  #returns the equipment in a slot, or None if it's empty
    for obj in cfg.inventory:
        if obj.equipment and obj.equipment.slot == slot and obj.equipment.is_equipped:
            return obj.equipment
    return None
 
def get_all_equipped(obj):  #returns a list of equipped items
    if obj == cfg.player:
        equipped_list = []
        for item in cfg.inventory:
            if item.equipment and item.equipment.is_equipped:
                equipped_list.append(item.equipment)
        return equipped_list
    else:
        return []  #other objects have no equipment
        
def calculate_xp(max_hp, defense, power, dex, speed, perception, luck):
    #return xp of a monster for given stats
    solo = max_hp + defense**2 + power**2 + int(10*math.log(speed + 1, 2)) + perception**2/5 + luck**2/7
    synergy = [(dex + int(10*math.log(speed + 1, 2)))*(defense + power) / 3, defense*power*speed*dex/10]
    
    return solo + sum(synergy)
    
def calculate_cooldown(max_hp, defense, power, dex, speed, perception, luck):
    #return max cooldown of a monster for given stats, no smaller than the minimum
    return max(cfg.MIN_COOLDOWN, int(cfg.COOLDOWN_FACTOR*calculate_xp(max_hp, defense, power, dex, speed, perception, luck)))
    
def calculate_nutrition(max_hp, defense, power, dex, speed, perception, luck):
    #return max nutrition of a monster for given stats
    return 20*max_hp + luck

def calculate_hunger(max_hp, defense, power, dex, speed, perception, luck):
    #return how quickly a monster loses nutrition for given stats
    return max(1, int(0.1*(power + speed)))

    
def target_tile(max_range=None):
    #return the position of a tile left-clicked in player's FOV (optionally in a range), or (None,None) if right-clicked.
    while True:
        #render the screen. this erases the inventory and shows the names of objects under the mouse.
        libtcod.console_flush()
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, cfg.key, cfg.mouse)
        render_all()
 
        (x, y) = (cfg.mouse.cx, cfg.mouse.cy)
 
        if cfg.mouse.rbutton_pressed or cfg.key.vk == libtcod.KEY_ESCAPE:
            return (None, None)  #cancel if the player right-clicked or pressed Escape
 
        #accept the target if the player clicked in FOV, and in case a range is specified, if it's in that range
        if (cfg.mouse.lbutton_pressed and libtcod.map_is_in_fov(cfg.fov_map, x, y) and
                (max_range is None or cfg.player.distance(x, y) <= max_range)):
            return (x, y)
            
def random_nearby_tile(x0, y0, attempts, free=False):
    #return the position of a random unblocked adjacent tile with a probabilistic failure rate
    while attempts > 0:
        x = x0 + libtcod.random_get_int(0, -1, 1)
        y = y0 + libtcod.random_get_int(0, -1, 1)
        
        if free and not is_occupied(x, y):
            return (x, y)
        
        elif not is_blocked(x, y):
            return (x, y)
            
        attempts -= 1
        
    return None
        
def mutate(value, probability, percent):
    #return a random (both in amount and in probability) mutation of an integer, always positive
    if random.random() < probability:
        max_mutation = max(int(round(value*percent)), 1) # at least 1
        mutation = value + libtcod.random_get_int(0, -max_mutation, max_mutation)
    else:
        mutation = value
    
    if mutation > 0:
        return mutation
    else:
        return -mutation
        
def color_mutate(color1, color2, probability, percent):
    #return the average of two colors with a random hue mutation
    
    #get the average hue
    color = libtcod.color_lerp(color1, color2, 0.5)
    hsv = libtcod.color_get_hsv(color)
    hue = hsv[0]
    
    #retain the saturation and vibrancy from the first parent
    hsv = libtcod.color_get_hsv(color1)
    sat = hsv[1]
    vib = hsv[2]
    
    #add mutation with probability
    if random.random() < probability:
        max_mutation = int(percent*360)
        hue += libtcod.random_get_int(0, -max_mutation, max_mutation)
        hue = hue % 360
        
    libtcod.color_set_hsv(color, hue, sat, vib)
    
    return color
 
def target_monster(max_range=None):
    #returns a clicked monster inside FOV up to a range, or None if right-clicked
    while True:
        (x, y) = target_tile(max_range)
        if x is None:  #player cancelled
            return None
 
        #return the first clicked monster, otherwise continue looping
        for obj in cfg.objects:
            if obj.x == x and obj.y == y and obj.fighter and obj != cfg.player:
                return obj
 
def closest_monster(max_range):
    #find closest enemy, up to a maximum range, and in the player's FOV
    closest_enemy = None
    closest_dist = max_range + 1  #start with (slightly more than) maximum range
 
    for obj in cfg.objects:
        if obj.fighter and not obj == cfg.player and libtcod.map_is_in_fov(cfg.fov_map, obj.x, obj.y):
            #calculate distance between this object and the player
            dist = cfg.player.distance_to(obj)
            if dist < closest_dist:  #it's closer, so remember it
                closest_enemy = obj
                closest_dist = dist
    return closest_enemy
 
def cast_heal():
    #heal the player
    if cfg.player.fighter.hp == cfg.player.fighter.max_hp:
        gui.message('You are already at full health.', libtcod.red)
        return 'cancelled'
 
    gui.message('Your wounds start to feel better!', libtcod.light_violet)
    cfg.player.fighter.heal(cfg.HEAL_AMOUNT)
 
def cast_lightning():
    #find closest enemy (inside a maximum range) and damage it
    monster = closest_monster(cfg.LIGHTNING_RANGE)
    if monster is None:  #no enemy found within maximum range
        gui.message('No enemy is close enough to strike.', libtcod.red)
        return 'cancelled'
 
    #zap it!
    gui.message('A lighting bolt strikes the ' + monster.name + ' with a loud thunder! The damage is '
            + str(cfg.LIGHTNING_DAMAGE) + ' hit points.', libtcod.light_blue)
    monster.fighter.take_damage(cfg.LIGHTNING_DAMAGE)
 
def cast_fireball():
    #ask the player for a target tile to throw a fireball at
    gui.message('Left-click a target tile for the fireball, or right-click to cancel.', libtcod.light_cyan)
    (x, y) = target_tile()
    if x is None: return 'cancelled'
    gui.message('The fireball explodes, burning everything within ' + str(cfg.FIREBALL_RADIUS) + ' tiles!', libtcod.orange)
 
    for obj in cfg.objects:  #damage every fighter in range, including the player
        if obj.distance(x, y) <= cfg.FIREBALL_RADIUS and obj.fighter:
            gui.message('The ' + obj.name + ' gets burned for ' + str(cfg.FIREBALL_DAMAGE) + ' hit points.', libtcod.orange)
            obj.fighter.take_damage(cfg.FIREBALL_DAMAGE)
 
def cast_confuse():
    #ask the player for a target to confuse
    gui.message('Left-click an enemy to confuse it, or right-click to cancel.', libtcod.light_cyan)
    monster = target_monster(cfg.CONFUSE_RANGE)
    if monster is None: return 'cancelled'
 
    #replace the monster's AI with a "confused" one; after some turns it will restore the old AI
    old_ai = monster.ai
    monster.ai = ConfusedMonster(old_ai)
    monster.ai.owner = monster  #tell the new component who owns it
    gui.message('The eyes of the ' + monster.name + ' look vacant, as he starts to stumble around!', libtcod.light_green)
 
def player_move_or_attack(dx, dy):
    #the coordinates the player is moving to/attacking
    x = cfg.player.x + dx
    y = cfg.player.y + dy
 
    #try to find an attackable object there
    target = None
    for obj in cfg.objects:
        if obj.fighter and obj.name != 'plant' and obj.x == x and obj.y == y:
            target = obj
            break
 
    #attack if target found, move otherwise
    if target is not None:
        cfg.player.fighter.attack(target)
    else:
        cfg.player.move(dx, dy)
        cfg.fov_recompute = True
        
def check_level_up():
    #see if the player's experience is enough to level-up
    level_up_xp = cfg.LEVEL_UP_BASE + cfg.player.level * cfg.LEVEL_UP_FACTOR
    if cfg.player.fighter.xp >= level_up_xp:
        #it is! level up and ask to raise some stats
        cfg.player.level += 1
        cfg.player.fighter.xp -= level_up_xp
        gui.message('Your battle skills grow stronger! You reached level ' + str(cfg.player.level) + '!', libtcod.yellow)
 
        choice = None
        while choice == None:  #keep asking until a choice is made
            choice = gui.menu('Level up! Choose a stat to raise:\n',
                          ['Constitution (+20 HP, from ' + str(cfg.player.fighter.max_hp) + ')',
                           'Strength (+1 attack, from ' + str(cfg.player.fighter.power) + ')',
                           'Agility (+1 defense, from ' + str(cfg.player.fighter.defense) + ')'], cfg.LEVEL_cfg.SCREEN_WIDTH)
 
        if choice == 0:
            cfg.player.fighter.base_max_hp += 20
            cfg.player.fighter.hp += 20
        elif choice == 1:
            cfg.player.fighter.base_power += 1
        elif choice == 2:
            cfg.player.fighter.base_defense += 1
    
def player_death(player):
    #the game ended!
    gui.message('You died!', libtcod.red)
    cfg.game_state = 'dead'
 
    #for added effect, transform the player into a corpse!
    player.char = '%'
    player.color = libtcod.dark_red
 
def monster_death(monster):
    #transform it into a nasty corpse! it doesn't block, can't be
    #attacked and doesn't move
    if cfg.DEATH_STATS:
        gui.message(monster.name.capitalize() + ' is dead! HP:' + str(monster.fighter.max_hp) + ' DEF:' + str(monster.fighter.defense) + ' POW:' + str(monster.fighter.power) + ' SPD:' + str(monster.fighter.speed) + ' PER:' + str(monster.fighter.perception) + ' XP:' + str(monster.fighter.xp) + ' NUT:' + str(monster.fighter.max_nutrition), libtcod.light_red)
    else:
        gui.message(monster.name.capitalize() + ' is dead!', libtcod.light_red)
    
    monster.char = '%'
    monster.color = monster.color * 0.7
    monster.item = Food(monster.fighter.nutrition)
    monster.item.owner = monster.fighter.owner
    monster.blocks = False
    monster.fighter = None
    monster.corpse = True
    monster.ai = None
    old_name = monster.name
    monster.name = 'remains of ' + old_name
    monster.send_to_back()

    #update population
    update_population(old_name)
    
    #extinction
    if cfg.population[old_name] < 1:
        gui.message('The ' + old_name + ' is now extinct...', libtcod.light_magenta)
        
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
            return obj
 
    return False

def distance_between(x0, y0, x1, y1):
    #return the distance between two points
    dx = x0 - x1
    dy = y0 - y1
    
    if cfg.CHEBYSHEV_METRIC:
        distance = max(abs(dx), abs(dy))
    else:
        distance = math.sqrt(dx ** 2 + dy ** 2)
        
    return distance

    
def object_count(name):
    #returns a count of objects that match a given name
    count = 0
    
    for obj in cfg.objects:
        if obj.name == name:
            count += 1
            
    return count
    
def initialize_population():
    #adds the names and populations of the monsters currently generated to the population dictionaries
    for obj in cfg.objects:
        if obj.fighter and obj.name not in cfg.max_population:
            if obj.name is not 'player' and obj.name is not 'plant':
                cfg.population[obj.name] = object_count(obj.name)
                cfg.max_population[obj.name] = object_count(obj.name)
    
def update_max_population():
    #finds max population for each monster type currently in the max_population dictionary
    
    for name in cfg.max_population:
        current_population = cfg.population[name]
        if current_population > cfg.max_population[name]:
            cfg.max_population[name] = current_population
    
def update_population(name=None):
    #finds population for each monster type or a specified monster type currently in the population dictionary
    
    if name:
        cfg.population[name] = object_count(name)
    
    else:
        for key in cfg.population:
            cfg.population[key] = object_count(key)
            
def make_monster(x, y, name, properties):
    #makes a fighter at a given position with a given name
    character = properties.char
    color = properties.color
    
    if name == 'player':
        fighter_component = Fighter(properties, death_function=player_death)
        cfg.player = Object(x, y, character, name, color, blocks=True, fighter=fighter_component)
    else:
        fighter_component = Fighter(properties, death_function=monster_death)
        ai_component = BasicMonster()
        monster = Object(x, y, character, name, color, blocks=True, fighter=fighter_component, ai=ai_component)
        cfg.objects.append(monster)

def make_plant(x, y):
    #makes a plant at a given position
    character = cfg.PLANT_CHAR
    color = libtcod.desaturated_green
    color = color_mutate(color, color, cfg.MUTATE_PROBABILITY, cfg.COLOR_MUTATE)
    
    nutri_component = mutate(cfg.BASE_PLANT_NUTRITION, 0.5, 0.2)
    item_component = Food(nutri_component)
    plant = Object(x, y, character, 'plant', color, blocks=False, corpse=False, item=item_component)
    cfg.objects.append(plant)
    plant.send_to_back()
