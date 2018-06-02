import libtcodpy as libtcod
import shelve
import cfg
import object
import mapgen
import monst
import gui
import random

#module used for main gameplay functions
 
def handle_keys():
    if cfg.key.vk == libtcod.KEY_ENTER and cfg.key.lalt:
        #Alt+Enter: toggle fullscreen
        libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
 
    elif cfg.key.vk == libtcod.KEY_ESCAPE or libtcod.console_is_window_closed():
        return 'exit'  #exit game
 
    if cfg.game_state == 'playing':
        #movement keys
        if cfg.key.vk == libtcod.KEY_UP or cfg.key.vk == libtcod.KEY_KP8:
            object.player_move_or_attack(0, -1)
        elif cfg.key.vk == libtcod.KEY_DOWN or cfg.key.vk == libtcod.KEY_KP2:
            object.player_move_or_attack(0, 1)
        elif cfg.key.vk == libtcod.KEY_LEFT or cfg.key.vk == libtcod.KEY_KP4:
            object.player_move_or_attack(-1, 0)
        elif cfg.key.vk == libtcod.KEY_RIGHT or cfg.key.vk == libtcod.KEY_KP6:
            object.player_move_or_attack(1, 0)
        elif cfg.key.vk == libtcod.KEY_HOME or cfg.key.vk == libtcod.KEY_KP7:
            object.player_move_or_attack(-1, -1)
        elif cfg.key.vk == libtcod.KEY_PAGEUP or cfg.key.vk == libtcod.KEY_KP9:
            object.player_move_or_attack(1, -1)
        elif cfg.key.vk == libtcod.KEY_END or cfg.key.vk == libtcod.KEY_KP1:
            object.player_move_or_attack(-1, 1)
        elif cfg.key.vk == libtcod.KEY_PAGEDOWN or cfg.key.vk == libtcod.KEY_KP3:
            object.player_move_or_attack(1, 1)
        elif cfg.key.vk == libtcod.KEY_KP5 or cfg.key.vk == libtcod.KEY_SPACE:
            pass  #do nothing ie wait for the monster to come to you
        elif cfg.key.vk == libtcod.KEY_INSERT or cfg.key.vk == libtcod.KEY_KP0:
            #toggle real time mode
            cfg.run_realtime = not cfg.run_realtime
        else:
            #test for other keys
            key_char = chr(cfg.key.c) # use for alphabetical keys
            # use key.text for symbolic keys
            '''
            if key_char == 'g':
                #pick up an item
                for obj in objects:  #look for an item in the player's tile
                    if obj.x == cfg.player.x and obj.y == cfg.player.y and obj.item:
                        obj.item.pick_up()
                        break
 
            if key_char == 'i':
                #show the inventory; if an item is selected, use it
                chosen_item = inventory_menu('Press the key next to an item to use it, or any other to cancel.\n')
                if chosen_item is not None:
                    chosen_item.use()
 
            if key_char == 'd':
                #show the inventory; if an item is selected, drop it
                chosen_item = inventory_menu('Press the key next to an item to drop it, or any other to cancel.\n')
                if chosen_item is not None:
                    chosen_item.drop()
            
            if key_char == 'c':
                #show character information
                level_up_xp = cfg.LEVEL_UP_BASE + cfg.player.level * cfg.LEVEL_UP_FACTOR
                gui.msgbox('Character Information\n\nLevel: ' + str(cfg.player.level) + '\nExperience: ' + str(cfg.player.fighter.xp) +
                       '\nExperience to level up: ' + str(level_up_xp) + '\n\nMaximum HP: ' + str(cfg.player.fighter.max_hp) +
                       '\nAttack: ' + str(cfg.player.fighter.power) + '\nDefense: ' + str(cfg.player.fighter.defense), cfg.CHARACTER_SCREEN_WIDTH)
            '''
            if key_char == 's':
                #show monster stats
                gui.display_monster_stats()

            if key_char == 'd':
                #show monster descriptions
                gui.display_description()
                
            if key_char == '/' or key_char == '?':
                #show monster descriptions
                gui.display_controls()
            
            if key_char == 'r':
                #toggle real time mode
                cfg.run_realtime = not cfg.run_realtime
            
            if key_char == 'q':
                #quit game while running
                return 'exit'
            '''
            if cfg.key.text == '>' or cfg.key.text == '+':
                #go down stairs, if the player is on them
                if cfg.stairs.x == cfg.player.x and cfg.stairs.y == cfg.player.y:
                    next_level()
            '''
            if cfg.run_realtime:
                return 'wait'
                
            else:
                return 'didnt-take-turn'
 
def save_game():
    #open a new empty shelve (possibly overwriting an old one) to write the game data
    file = shelve.open('savegame', 'n')
    file['map'] = cfg.map
    file['objects'] = cfg.objects
    file['player_index'] = cfg.objects.index(cfg.player)  #index of player in objects list
    file['stairs_index'] = cfg.objects.index(cfg.stairs)  #same for the stairs
    file['inventory'] = cfg.inventory
    file['game_msgs'] = cfg.game_msgs
    file['game_state'] = cfg.game_state
    file['population'] = cfg.population
    file['max_population'] = cfg.max_population
    file['run_realtime'] = cfg.run_realtime
    file['dungeon_level'] = cfg.dungeon_level
    file.close()
 
def load_game():
    #open the previously saved shelve and load the game data
    file = shelve.open('savegame', 'r')
    cfg.map = file['map']
    cfg.objects = file['objects']
    cfg.player = cfg.objects[file['player_index']]  #get index of player in objects list and access it
    cfg.stairs = cfg.objects[file['stairs_index']]  #same for the stairs
    cfg.inventory = file['inventory']
    cfg.game_msgs = file['game_msgs']
    cfg.game_state = file['game_state']
    cfg.population = file['population']
    cfg.max_population = file['max_population']
    cfg.run_realtime = file['run_realtime']
    cfg.dungeon_level = file['dungeon_level']
    file.close()
 
    mapgen.initialize_fov()
 
def new_game():
    #create object representing the player
    object.make_monster(0, 0, 'player', monst.properties['player'])
 
    cfg.player.level = 1
 
    #generate map (at this point it's not drawn to the screen)
    cfg.dungeon_level = 1
    mapgen.make_bsp()
    mapgen.initialize_fov()
 
    cfg.game_state = 'playing'
    cfg.run_realtime = cfg.REAL_TIME
    cfg.inventory = []
 
    #create the list of game messages and their colors, starts empty
    cfg.game_msgs = []
    
    #create dictionaries of populations for monsters
    cfg.population = {}
    cfg.max_population = {}
    object.initialize_population()
 
    #a warm welcoming message!
    gui.message('Beginning genetic simulation.', libtcod.light_red * 0.7)
 
    #initial equipment: a dagger
    #equipment_component = object.Equipment(slot='right hand', power_bonus=2)
    #obj = object.Object(0, 0, '-', 'dagger', libtcod.sky, equipment=equipment_component)
    #cfg.inventory.append(obj)
    #equipment_component.equip()
    #obj.always_visible = True
 
def play_game():
    player_action = None
 
    #main loop
    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, cfg.key, cfg.mouse)
        #render the screen
        gui.render_all()
 
        libtcod.console_flush()
 
        #level up if needed
        object.check_level_up()
 
        #erase all objects at their old locations, before they move
        for obj in cfg.objects:
            obj.clear()
 
        #handle keys and exit game if needed
        player_action = handle_keys()
        if player_action == 'exit':
            save_game()
            break
 
        #let monsters take their turn
        if cfg.game_state == 'playing' and player_action != 'didnt-take-turn':
            for obj in cfg.objects:
                if obj.ai:
                    obj.ai.take_turn()
                    
                if obj.item:
                    obj.item.age_up()

                    
            if random.random() < cfg.PLANT_GROWTH_PROBABILITY:
                #grow PLANT_GROWTH_RATE number of plants
                for i in range(cfg.NEW_PLANT_RATE):
                    #choose random tile
                    x = libtcod.random_get_int(0, 1, cfg.MAP_WIDTH)
                    y = libtcod.random_get_int(0, 1, cfg.MAP_HEIGHT)
                    #if the tile is unoccupied, grow plant
                    occupant = object.is_occupied(x, y)
                    if not occupant:
                        object.make_plant(x, y)
                    
                    elif type(occupant) is not bool:
                        if occupant.name == 'plant':
                            occupant.item.grow()

                
            #update population counts
            #update_population()
            object.update_max_population()
 
def main_menu():
    libtcod.console_set_custom_font('terminal8x12_gs_ro.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_ASCII_INROW)
    libtcod.console_init_root(cfg.SCREEN_WIDTH, cfg.SCREEN_HEIGHT, 'Monster Genetics', False)
    libtcod.sys_set_fps(cfg.LIMIT_FPS)
    img = libtcod.image_load('menu_background.png')
 
    while not libtcod.console_is_window_closed():
        gui.display_main_menu(img)
 
        #show options and wait for the player's choice
        choice = gui.menu('', ['Play a new game', 'Continue last game', 'Display controls', 'Quit'], 24)
 
        if choice == 0:  #new game
            new_game()
            play_game()
        elif choice == 1:  #load last game
            try:
                load_game()
            except:
                gui.msgbox('\n No saved game to load.\n', 24)
                continue
            play_game()
        elif choice == 2: #controls, will eventually be options menu
            gui.display_controls()
        elif choice == 3:  #quit
            break

