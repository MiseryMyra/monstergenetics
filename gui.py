import libtcodpy as libtcod
import textwrap
import math
import cfg
import describe

#module used for displaying graphics and messages

def get_names_under_mouse():
    #return a string with the names of all objects under the mouse
 
    (x, y) = (cfg.mouse.cx, cfg.mouse.cy)
 
    #create a list with the names of all objects at the mouse's coordinates and in FOV
    #names = [obj.name for obj in reversed(objects) if obj.x == x and obj.y == y and (libtcod.map_is_in_fov(cfg.fov_map, obj.x, obj.y) or cfg.ALL_SEEING)]
    names = []
    for obj in reversed(cfg.objects):
        if obj.x == x and obj.y == y and (libtcod.map_is_in_fov(cfg.fov_map, obj.x, obj.y) or cfg.ALL_SEEING):
            name = obj.name
            
            if obj.fighter and (name is not 'plant'):
                name = name.capitalize()
                mon = obj.fighter
                #stats = ' (HP:' + str(mon.hp) + '/' + str(mon.max_hp) + ' PW:' + str(mon.power) + ' DF:' + str(mon.defense) + ' DX:' + str(mon.dex) + ' SP:' + str(mon.speed) + ' PR:' + str(mon.perception) + ' LK:' + str(mon.luck) + ' SC:' + str(mon.social) + ' AG:' + str(mon.aggro) + ' XP:' + str(mon.xp) + ' NT:' + str(mon.nutrition) + '/' + str(mon.max_nutrition) + ')'
                stats = ' (HP:' + str(mon.hp) + '/' + str(mon.max_hp) + ' PW:' + str(mon.power) + ' DF:' + str(mon.defense) + ' DX:' + str(mon.dex) + ' SP:' + str(mon.speed) + ' PR:' + str(mon.perception) + ' LK:' + str(mon.luck) + ' XP:' + str(mon.xp) + ' NT:' + str(mon.nutrition) + '/' + str(mon.max_nutrition) + ')'
                name = name + stats
                
            names.append(name)
 
    names = ', '.join(names)  #join the names, separated by commas
    return names

def render_bar(x, y, total_width, name, value, maximum, bar_color=None, back_color=None):
    #render a bar (HP, experience, etc). first calculate the width of the bar
    if maximum != 0:
        bar_width = int(math.ceil(float(value) / maximum * total_width))
        
    #0/0 gives an empty bar
    else:
        bar_width = 0

    #automatic bar colors
    if bar_color == None:
        percent = float(value) / maximum

        if percent >= 1:
            bar_color = libtcod.desaturated_azure

        elif percent > 0.75:
            bar_color = libtcod.desaturated_green

        elif percent > 0.5:
            bar_color = libtcod.desaturated_yellow

        elif percent > 0.25:
            bar_color = libtcod.desaturated_orange

        elif percent > 0:
            bar_color = libtcod.desaturated_red

        else:
            bar_color = libtcod.desaturated_pink

    if back_color == None:
        back_color = bar_color * 0.5
 
    #render the background first
    libtcod.console_set_default_background(cfg.panel, back_color)
    libtcod.console_rect(cfg.panel, x, y, total_width, 1, False, libtcod.BKGND_SCREEN)
 
    #now render the bar on top
    libtcod.console_set_default_background(cfg.panel, bar_color)
    if bar_width > 0:
        libtcod.console_rect(cfg.panel, x, y, bar_width, 1, False, libtcod.BKGND_SCREEN)
 
    #finally, some centered text with the values
    libtcod.console_set_default_foreground(cfg.panel, libtcod.white)
    libtcod.console_print_ex(cfg.panel, x + total_width / 2, y, libtcod.BKGND_NONE, libtcod.CENTER,
                                 name + ': ' + str(value) + '/' + str(maximum))
                                 
def render_population_bars():
    #render bars representing population in the GUI panel
    y = 1 #initial y position of the bar

    #skips lines if there aren't too many bars
    if len(cfg.population) > 6:
        dy = 1
    else:
        dy = 2
    
    #sorts by descending population value
    for name in list_monsters():
        render_bar(1, y, cfg.BAR_WIDTH, name.capitalize(), cfg.population[name], cfg.max_population[name])
        y += dy
        
def list_monsters():
    #returns a list of monster names, sorted by population value
    names = []
    for key, value in sorted(cfg.population.iteritems(), key=lambda (k,v): (v,k), reverse=True):
        if key is not 'plant':
            names.append(key)

    return names
        
def render_all():
    if cfg.fov_recompute:
        #recompute FOV if needed (the player moved or something)
        cfg.fov_recompute = False
        libtcod.map_compute_fov(cfg.fov_map, cfg.player.x, cfg.player.y, cfg.TORCH_RADIUS, cfg.FOV_LIGHT_WALLS, cfg.FOV_ALGO)
 
        #go through all tiles, and set their background color according to the FOV
        for y in range(cfg.MAP_HEIGHT):
            for x in range(cfg.MAP_WIDTH):
                if cfg.ALL_SEEING:
                    visible = True
                else:
                    visible = libtcod.map_is_in_fov(cfg.fov_map, x, y)
                    
                wall = cfg.map[x][y].block_sight
                if not visible:
                    #if it's not visible right now, the player can only see it if it's explored
                    if cfg.map[x][y].explored:
                        if wall:
                            libtcod.console_put_char_ex(cfg.con, x, y, pick_wall_char(x, y), cfg.color_dark_wall, libtcod.black)
                        else:
                            libtcod.console_put_char_ex(cfg.con, x, y, cfg.FLOOR_CHAR, cfg.color_dark_ground, libtcod.black)
                else:
                    #it's visible
                    if wall:
                        libtcod.console_put_char_ex(cfg.con, x, y, pick_wall_char(x, y), cfg.color_light_wall, libtcod.black)
                    else:
                        if cfg.map[x][y].fertile > 0:
                            libtcod.console_put_char_ex(cfg.con, x, y, cfg.FLOOR_CHAR, cfg.color_fertile_ground, libtcod.black)
                        else:
                            libtcod.console_put_char_ex(cfg.con, x, y, cfg.FLOOR_CHAR, cfg.color_light_ground, libtcod.black)
                        #since it's visible, explore it
                    cfg.map[x][y].explored = True
 
    #draw all objects in the list, except the player. we want it to
    #always appear over all other objects! so it's drawn later.
    for object in cfg.objects:
        if object != cfg.player:
            object.draw()
    cfg.player.draw()
 
    #blit the contents of "con" to the root console
    libtcod.console_blit(cfg.con, 0, 0, cfg.MAP_WIDTH, cfg.MAP_HEIGHT, 0, 0, 0)
 
 
    #prepare to render the GUI panel
    libtcod.console_set_default_background(cfg.panel, libtcod.black)
    libtcod.console_clear(cfg.panel)
 
    #print the game messages, one line at a time
    y = 1
    for (line, color) in cfg.game_msgs:
        libtcod.console_set_default_foreground(cfg.panel, color)
        libtcod.console_print_ex(cfg.panel, cfg.MSG_X, y, libtcod.BKGND_NONE, libtcod.LEFT,line)
        y += 1
 
    #show the player's stats
    #render_bar(1, 1, cfg.BAR_WIDTH, 'HP', player.fighter.hp, player.fighter.max_hp, libtcod.light_red, libtcod.darker_red)
    #libtcod.console_print_ex(cfg.panel, 1, 3, libtcod.BKGND_NONE, libtcod.LEFT, 'Dungeon level ' + str(cfg.dungeon_level))
    render_population_bars()
 
    #display names of objects under the mouse
    libtcod.console_set_default_foreground(cfg.panel, libtcod.light_gray)
    libtcod.console_print_ex(cfg.panel, 1, 0, libtcod.BKGND_NONE, libtcod.LEFT, get_names_under_mouse())
 
    #blit the contents of "panel" to the root console
    libtcod.console_blit(cfg.panel, 0, 0, cfg.SCREEN_WIDTH, cfg.PANEL_HEIGHT, 0, 0, cfg.PANEL_Y)

def bitmask_walls(x, y):
    #returns a bitmask for the walls surrounding a given location, excluding itself
    bitmask = 0
    power = 0

    for dx in [-1,0,1]:
        for dy in [-1,0,1]:
            if x + dx in range(cfg.MAP_WIDTH) and y + dy in range(cfg.MAP_HEIGHT):
                if cfg.map[x + dx][y + dy].block_sight and (dx != 0 or dy != 0):
                    if dx == 0 or dy == 0:
                        bitmask += 2**power
                    #check for redundant diagonal pieces based on whether they have two adjacent neighbors
                    elif cfg.map[x][y + dy].block_sight and cfg.map[x + dx][y].block_sight:
                        bitmask += 2**power
            else:
                #treat off-screen areas as walls
                if dx == 0 or dy == 0:
                    bitmask += 2**power
                else:
                    adjacent_neighbors = 0

                    if x in range(cfg.MAP_WIDTH) and y + dy in range(cfg.MAP_HEIGHT):
                        if cfg.map[x][y + dy].block_sight:
                            adjacent_neighbors += 1
                    else:
                        adjacent_neighbors += 1

                    if x + dx in range(cfg.MAP_WIDTH) and y in range(cfg.MAP_HEIGHT):
                        if cfg.map[x + dx][y].block_sight:
                            adjacent_neighbors += 1
                    else:
                        adjacent_neighbors += 1

                    if adjacent_neighbors > 1:
                        bitmask += 2**power

            if dx != 0 or dy != 0:
                power += 1

    return bitmask

def pick_wall_char(x, y):
    #picks which wall tile should be rendered at the given position based on surrounding walls
    #single-line walls
    wall_map = {0 : libtcod.CHAR_HLINE, 2 : libtcod.CHAR_HLINE, 8 : libtcod.CHAR_VLINE, 10 : libtcod.CHAR_SE, 11 : libtcod.CHAR_SE, 16 : libtcod.CHAR_VLINE, 18 : libtcod.CHAR_NE, 22 : libtcod.CHAR_NE, 24 : libtcod.CHAR_VLINE, 26 : libtcod.CHAR_TEEW, 27 : libtcod.CHAR_TEEW, 30 : libtcod.CHAR_TEEW, 31 : libtcod.CHAR_VLINE, 64 : libtcod.CHAR_HLINE, 66 : libtcod.CHAR_HLINE, 72 : libtcod.CHAR_SW, 74 : libtcod.CHAR_TEEN, 75 : libtcod.CHAR_TEEN, 80 : libtcod.CHAR_NW, 82 : libtcod.CHAR_TEES, 86 : libtcod.CHAR_TEES, 88 : libtcod.CHAR_TEEE, 90 : libtcod.CHAR_CROSS, 91 : libtcod.CHAR_CROSS, 94 : libtcod.CHAR_CROSS, 95 : libtcod.CHAR_TEEE, 104 : libtcod.CHAR_SW, 106 : libtcod.CHAR_TEEN, 107 : libtcod.CHAR_HLINE, 120 : libtcod.CHAR_TEEE, 122 : libtcod.CHAR_CROSS, 123 : libtcod.CHAR_TEES, 126 : libtcod.CHAR_CROSS, 127 : libtcod.CHAR_NW, 208 : libtcod.CHAR_NW, 210 : libtcod.CHAR_TEES, 214 : libtcod.CHAR_HLINE, 216 : libtcod.CHAR_TEEE, 218 : libtcod.CHAR_CROSS, 219 : libtcod.CHAR_CROSS, 222 : libtcod.CHAR_TEEN, 223 : libtcod.CHAR_SW, 248 : libtcod.CHAR_VLINE, 250 : libtcod.CHAR_TEEW, 251 : libtcod.CHAR_NE, 254 : libtcod.CHAR_SE, 255 : ' '}
    
    #double-line walls
    #wall_map = {0 : libtcod.CHAR_DHLINE, 2 : libtcod.CHAR_DHLINE, 8 : libtcod.CHAR_DVLINE, 10 : libtcod.CHAR_DSE, 11 : libtcod.CHAR_DSE, 16 : libtcod.CHAR_DVLINE, 18 : libtcod.CHAR_DNE, 22 : libtcod.CHAR_DNE, 24 : libtcod.CHAR_DVLINE, 26 : libtcod.CHAR_DTEEW, 27 : libtcod.CHAR_DTEEW, 30 : libtcod.CHAR_DTEEW, 31 : libtcod.CHAR_DVLINE, 64 : libtcod.CHAR_DHLINE, 66 : libtcod.CHAR_DHLINE, 72 : libtcod.CHAR_DSW, 74 : libtcod.CHAR_DTEEN, 75 : libtcod.CHAR_DTEEN, 80 : libtcod.CHAR_DNW, 82 : libtcod.CHAR_DTEES, 86 : libtcod.CHAR_DTEES, 88 : libtcod.CHAR_DTEEE, 90 : libtcod.CHAR_DCROSS, 91 : libtcod.CHAR_DCROSS, 94 : libtcod.CHAR_DCROSS, 95 : libtcod.CHAR_DTEEE, 104 : libtcod.CHAR_DSW, 106 : libtcod.CHAR_DTEEN, 107 : libtcod.CHAR_DHLINE, 120 : libtcod.CHAR_DTEEE, 122 : libtcod.CHAR_DCROSS, 123 : libtcod.CHAR_DTEES, 126 : libtcod.CHAR_DCROSS, 127 : libtcod.CHAR_DNW, 208 : libtcod.CHAR_DNW, 210 : libtcod.CHAR_DTEES, 214 : libtcod.CHAR_DHLINE, 216 : libtcod.CHAR_DTEEE, 218 : libtcod.CHAR_DCROSS, 219 : libtcod.CHAR_DCROSS, 222 : libtcod.CHAR_DTEEN, 223 : libtcod.CHAR_DSW, 248 : libtcod.CHAR_DVLINE, 250 : libtcod.CHAR_DTEEW, 251 : libtcod.CHAR_DNE, 254 : libtcod.CHAR_DSE, 255 : ' '}

    bitmask = bitmask_walls(x, y)

    if bitmask in wall_map:
        return wall_map[bitmask]

    else:
        return '?'
 
def message(new_msg, color = libtcod.white):
    #split the message if necessary, among multiple lines
    new_msg_lines = textwrap.wrap(new_msg, cfg.MSG_WIDTH)
 
    for line in new_msg_lines:
        #if the buffer is full, remove the first line to make room for the new one
        if len(cfg.game_msgs) == cfg.MSG_HEIGHT:
            del cfg.game_msgs[0]
 
        #add the new line as a tuple, with the text and the color
        cfg.game_msgs.append( (line, color) )
        
def menu(header, options, width, numbers = False):
    if numbers:
        if len(options) > 9: raise ValueError('Cannot have a menu with more than 9 options.')
    else:
        if len(options) > 26: raise ValueError('Cannot have a menu with more than 26 options.')
 
    #calculate total height for the header (after auto-wrap) and one line per option
    header_height = libtcod.console_get_height_rect(cfg.con, 0, 0, width, cfg.SCREEN_HEIGHT, header)
    if header == '':
        header_height = 0
    height = len(options) + header_height
 
    #create an off-screen console that represents the menu's window
    window = libtcod.console_new(width, height)
 
    #print the header, with auto-wrap
    libtcod.console_set_default_foreground(window, libtcod.white)
    libtcod.console_print_rect_ex(window, 0, 0, width, height, libtcod.BKGND_NONE, libtcod.LEFT, header)
 
    #print all the options
    y = header_height

    if numbers:
        letter_index = ord('1')
    else:
        letter_index = ord('a')

    for option_text in options:
        text = '(' + chr(letter_index) + ') ' + option_text
        libtcod.console_print_ex(window, 0, y, libtcod.BKGND_NONE, libtcod.LEFT, text)
        y += 1
        letter_index += 1
 
    #blit the contents of "window" to the root console
    x = cfg.SCREEN_WIDTH/2 - width/2
    y = cfg.SCREEN_HEIGHT/2 - height/2
    libtcod.console_blit(window, 0, 0, width, height, 0, x, y, 1.0, 0.85)
 
    #compute x and y offsets to convert console position to menu position
    x_offset = x #x is the left edge of the menu
    y_offset = y + header_height #subtract the height of the header from the top edge of the menu
 
    while True:
        #present the root console to the player and check for input
        libtcod.console_flush()
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS|libtcod.EVENT_MOUSE,cfg.key,cfg.mouse)
 
        if (cfg.mouse.lbutton_pressed):
            (menu_x, menu_y) = (cfg.mouse.cx - x_offset, cfg.mouse.cy - y_offset)
            #check if click is within the menu and on a choice
            if menu_x >= 0 and menu_x < width and menu_y >= 0 and menu_y < height - header_height:
                return menu_y
 
        if cfg.mouse.rbutton_pressed or cfg.key.vk == libtcod.KEY_ESCAPE:
            return None #cancel if the player right-clicked or pressed Escape
 
        if cfg.key.vk == libtcod.KEY_ENTER and cfg.key.lalt:
            #Alt+Enter: toggle fullscreen
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
 
        #convert the ASCII code to an index; if it corresponds to an option, return it
        if numbers:
            index = cfg.key.c - ord('1')
        else:
            index = cfg.key.c - ord('a')

        if index >= 0 and index < len(options): return index
        #if they pressed a letter that is not an option, return None
        #also return none if the window gets closed
        if cfg.key.c >= 7 or libtcod.console_is_window_closed(): return None
 
def inventory_menu(header):
    #show a menu with each item of the inventory as an option
    if len(cfg.inventory) == 0:
        options = ['Inventory is empty.']
    else:
        options = []
        for item in cfg.inventory:
            text = item.name
            #show additional information, in case it's equipped
            if item.equipment and item.equipment.is_equipped:
                text = text + ' (on ' + item.equipment.slot + ')'
            options.append(text)
 
    index = menu(header, options, cfg.INVENTORY_WIDTH)
 
    #if an item was chosen, return it
    if index is None or len(cfg.inventory) == 0: return None
    return cfg.inventory[index].item
 
def msgbox(text, width=50):
    menu(text, [], width)  #use menu() as a sort of "message box"
    
def display_monster_stats():
    message = 'Monster Statistics'
    #stats in the official order
    stats_list = ['hp', 'pw', 'df', 'dx', 'sp', 'pr', 'lk', 'xp', 'nt', 'sc', 'ag']
    for name in list_monsters():
        if cfg.population[name] > 0:
            stats = total_monster_stats(name)
            avg_string = name.capitalize() + ' (avg): '
            max_string = name.capitalize() + ' (max): '
            min_string = name.capitalize() + ' (min): '

            for stat in stats_list:
                avg_string = avg_string + stat.upper() + ':' + str(stats[stat]['avg']) + ' '
                max_string = max_string + stat.upper() + ':' + str(stats[stat]['max']) + ' '
                min_string = min_string + stat.upper() + ':' + str(stats[stat]['min']) + ' '

            stats_string = '\n\n' + avg_string + '\n' + max_string + '\n' + min_string
            message = message + stats_string
    
    msgbox(message,86)
    
def total_monster_stats(name):
    #returns the average, min, and max stats for a given monster population
    hp = {'avg' : 0, 'min': -1, 'max' : 0}
    pw = {'avg' : 0, 'min': -1, 'max' : 0}
    df = {'avg' : 0, 'min': -1, 'max' : 0}
    dx = {'avg' : 0, 'min': -1, 'max' : 0}
    sp = {'avg' : 0, 'min': -1, 'max' : 0}
    pr = {'avg' : 0, 'min': -1, 'max' : 0}
    lk = {'avg' : 0, 'min': -1, 'max' : 0}
    xp = {'avg' : 0, 'min': -1, 'max' : 0}
    nt = {'avg' : 0, 'min': -1, 'max' : 0}
    sc = {'avg' : 0, 'min': -1, 'max' : 0}
    ag = {'avg' : 0, 'min': -1, 'max' : 0}
    stats = {'hp' : hp, 'pw' : pw, 'df' : df, 'dx' : dx, 'sp' : sp, 'pr' : pr, 'lk' : lk, 'xp' : xp, 'nt' : nt, 'sc' : sc, 'ag' : ag}
    pop = cfg.population[name]
    
    if pop < 1:
        #none exist, reset minimums
        for stat in stats:
            stats[stat]['min'] = 0

        return stats

    else:
        #iterate over all the monsters
        for obj in cfg.objects:
            if obj.fighter and obj.name == name:
                mon_stats = monster_stats(obj.fighter)

                #iterate over all the stats of each monster
                for key in mon_stats:
                    mon_stat = mon_stats[key]
                    stats[key]['avg'] += mon_stat

                    #get maximum stat
                    if mon_stat > stats[key]['max']:
                        stats[key]['max'] = mon_stat

                    #get minimum stat, initialized at -1
                    if stats[key]['min'] == -1 or mon_stat < stats[key]['min']:
                        stats[key]['min'] = mon_stat

        #compute averages
        for key in stats:
            stats[key]['avg'] = stats[key]['avg']/pop

        return stats
        
def monster_stats(monster):
    #returns the stats of a given monster in a dictionary
    stats = {'hp' : 0, 'pw' : 0, 'df' : 0, 'dx' : 0, 'sp' : 0, 'pr' : 0, 'lk' : 0, 'xp' : 0, 'nt' : 0, 'sc' : 0, 'ag' : 0}

    if monster.owner.fighter:
        stats['hp'] = monster.max_hp
        stats['pw'] = monster.power
        stats['df'] = monster.defense
        stats['dx'] = monster.dex
        stats['sp'] = monster.speed
        stats['pr'] = monster.perception
        stats['lk'] = monster.luck
        stats['xp'] = monster.xp
        stats['nt'] = monster.max_nutrition
        stats['sc'] = monster.social
        stats['ag'] = monster.aggro

    return stats
    
def display_description():
    #show monster descriptions
    names = list_monsters()
    capitalized_names = list_monsters()

    for i in range(len(capitalized_names)):
        capitalized_names[i] = names[i].capitalize()

    choice = menu('Describe which species?\nPress any other key to cancel.', capitalized_names, 36, numbers=True)

    if choice is not None:
        name = names[choice]
        description = describe.generate_description(name, cfg.population[name], total_monster_stats(name))
        msgbox(description)
        
def display_controls():
    controls = 'CONTROLS\n\n'
    controls = controls + 'Numpad or arrow keys: Move the player and attack\nNumpad 5 or space bar: Wait a turn in turn-based mode\nNumpad 0 or R: Toggle turn-based mode\nS: Display the monster statistics window\nD: Display the monster descriptions window\nESC or Q: Quit to main menu\nMouse: Click on menu options, hover over monsters to see stats\n/ or ?: Display controls'
    controls = controls + '\n\nPress any key to close this window.'
    msgbox(controls,70)
        
def display_main_menu(img):
    #show the background image, at twice the regular console resolution
    libtcod.image_blit_2x(img, 0, 0, 0)

    #show the game's title, and some credits!
    libtcod.console_set_default_foreground(0, libtcod.light_pink)
    libtcod.console_print_ex(0, cfg.SCREEN_WIDTH/2, cfg.SCREEN_HEIGHT/2-4, libtcod.BKGND_NONE, libtcod.CENTER,
                             'M O N S T E R   G E N E T I C S')
    libtcod.console_print_ex(0, cfg.SCREEN_WIDTH/2, cfg.SCREEN_HEIGHT-4, libtcod.BKGND_NONE, libtcod.CENTER, 'By MiseryMyra')
    libtcod.console_print_ex(0, cfg.SCREEN_WIDTH/2, cfg.SCREEN_HEIGHT-2, libtcod.BKGND_NONE, libtcod.CENTER, 'Version ' + cfg.VERSION_NUMBER)
