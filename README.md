# Monster Genetics
A genetic life simulation game built from a traditional roguelike engine by MiseryMyra.

## Premise
Monster Genetics is a genetic simulation game based on a traditional roguelike engine. Different species of monsters compete with each other for space and food. The survivors reproduce with each other, passing down their traits with a random chance of mutations. Over time, they may evolve different traits than their ancestors, making them better suited for their environment. The more powerful they are, though, the slower they reproduce, so they have to find the right balance to be successful.

The player (@) exists primarily to observe the evolution of these species, but they may have limited interactions with them as well. The ultimate outcome of these simulations is largely random, and different games may have different results.

### Screenshots

![Screenshot1](https://i.imgur.com/X0w3hpn.png)

![Screenshot2](https://i.imgur.com/RQcibqi.png)


## Code
**main.py**:
Runs the game

**cfg.py**:
Module used for configuring settings and initializing globals

**describe.py**:
Module used for generating descriptions of monster species based on their average stats and population

**game.py**:
Module used for main gameplay functions

**gui.py**:
Module used for displaying graphics and messages

**mapgen.py**:
module used for handling map generation

**monst.py**:
Module for defining the initial properties for all the different monsters

**object.py**:
Module for object classes and related functions

**run_py2exe**:
Generates binary with py2exe


## Controls
**Numpad or arrow keys**:
Move the player and attack

**Numpad 5 or space bar**:
Wait a turn in turn-based mode

**Numpad 0 or R**:
Toggle turn-based mode

**S**:
Display the monster statistics window

**D**:
Display the monster descriptions window

**ESC or Q**:
Quit to main menu

**Mouse**:
Click on menu options, hover over monsters to see stats

**/ or ?**:
Display controls


## Stats
Each monster has a set of stats that determine their abilities. When two monsters reproduce, their offspring has has the average stats of their two parents. However, these stats may be randomly mutated to be higher or lower than the simple average.

**Hit Points (HP)**:
The health of a monster. Once it reaches zero, the monster dies.

**Power (PW)**:
Governs the maximum attack power of a monster.

**Defense (DF)**:
Governs the maximum defense power of a monster.

**Dexterity (DX)**:
Governs the minimum attack and defense power of a monster.

**Speed (SP)**:
Governs how often monsters can take a turn.

**Perception (PR)**:
The radius of sight a monster has.

**Luck (LK)**:
Governs critical hit chances.

**Experience (XP)**:
A measure of how strong a monster is overall. Governs the reproduction rate.

**Nutrition (NT)**:
How much food a monster has. Once it reaches zero, the monster begins to starve!

**Social (SC)**:
Governs how much monsters interact with members of their own species.

**Aggression (AG)**:
Governs whether or not monsters fight or run away from enemies.

**Color**:
Purely cosmetic. Still subject to mutations.


## Notes
The game automatically saves every time you quit. You can load this save at the main menu, but starting a new game replaces the save, so be careful!

The player and the monsters can dig through walls by moving into them, but monsters generally don't try unless they want to get at something behind a wall, and they cannot find another path to it.

Hungry monsters will eat monsters of another species, but starving monsters will eat any available food.

Reproduction always has a chance to fail, but it is more likely in densely populated areas or enclosed spaces.

Any two monsters of the same species can reproduce, provided that they are both able to, and they each have an equal and symmetric involvement in the process.

The population bars in the lower left give the current population out of the maximum population reached, which is capped at 100 per species, and they are sorted by current population levels.


## To-do
Here is a list of features that I would like to incorporate in future versions:

- More varied monster behavior based on genetic traits

- More interaction between monsters of the same species

- A better "run away" and "wander" algorithm

- Expanded species descriptions, especially based on behavior

- Different environments, including hazards and resources

- An options menu for changing parameters

- More player interaction, including spawning and possibly designing monsters

- Adjusted room generation to make more interesting shapes

- A better looking and more readable statistics window


## Acknowledgments

This game was built using libtcod, "The Doryen Library," which is an invaluable resource for developing traditional roguelikes or similar games.

In particular, this game was built up from the python libtcod tutorial written by João F. Henriques (a.k.a. Jotaf), which is available [here](http://www.roguebasin.com/index.php?title=Complete_Roguelike_Tutorial,_using_python%2Blibtcod).

Additional contributions were made by [Inspector Caracal](https://tootplanet.space/@InspectorCaracal).
