=============================
|  MONSTER GENETICS 0.3.2   |
|       By MiseryMyra       |
| Last revision: 06/11/2018 |
=============================

-------------
|  Premise  |
-------------

Monster Genetics is a genetic simulation game based on a traditional roguelike engine.
Different species of monsters compete with each other for space and food. The survivors
reproduce with each other, passing down their traits with a random chance of mutations.
Over time, they may evolve different traits than their ancestors, making them better
suited for their environment. The more powerful they are, though, the slower they
reproduce, so they have to find the right balance to be successful.

The player (@) exists primarily to observe the evolution of these species, but they may
have limited interactions with them as well. The ultimate outcome of these simulations
is largely random, and different games may have different results.


--------------
|  Controls  |
--------------

Numpad or arrow keys: Move the player and attack

Numpad 5 or space bar: Wait a turn in turn-based mode

Numpad 0 or R: Toggle turn-based mode

S: Display the monster statistics window

D: Display the monster descriptions window

ESC or Q: Quit to main menu

Mouse: Click on menu options, hover over monsters to see stats

/ or ?: Display controls


-------------
|   Stats   |
-------------

Each monster has a set of stats that determine their abilities. When two monsters
reproduce, their offspring has has the average stats of their two parents. However,
these stats may be randomly mutated to be higher or lower than the simple average.

Hit Points (HP)
The health of a monster. Once it reaches zero, the monster dies.

Power (PW)
Governs the maximum attack power of a monster.

Defense (DF)
Governs the maximum defense power of a monster.

Dexterity (DX)
Governs the minimum attack and defense power of a monster.

Speed (SP)
Governs how often monsters can take a turn.

Perception (PR)
The radius of sight a monster has.

Luck (LK)
Governs critical hit chances.

Experience (XP)
A measure of how strong a monster is overall. Governs the reproduction rate.

Nutrition (NT)
How much food a monster has. Once it reaches zero, the monster begins to starve!

Social (SC)
Governs how much monsters interact with members of their own species.

Aggression (AG)
Governs whether or not monsters fight or run away from enemies.

Color
Purely cosmetic. Still subject to mutations.


-------------
|   Notes   |
-------------

The game automatically saves every time you quit. You can load this save at the main
menu, but starting a new game replaces the save, so be careful!

The player and the monsters can dig through walls by moving into them, but monsters
generally don't try unless they want to get at something behind a wall, and they cannot
find another path to it.

Hungry monsters will eat monsters of another species, but starving monsters will eat
any available food.

Reproduction always has a chance to fail, but it is more likely in densely populated
areas or enclosed spaces.

Any two monsters of the same species can reproduce, provided that they are both able to, 
and they each have an equal and symmetric involvement in the process.

The population bars in the lower left give the current population out of the maximum
population reached, which is capped at 100 per species, and they are sorted by
current population levels.


---------------------
|  Acknowledgments  |
---------------------

This game was built using libtcod, "The Doryen Library," which is an invaluable resource
for developing traditional roguelikes or similar games.

In particular, this game was built up from the python libtcod tutorial written by
João F. Henriques (a.k.a. Jotaf), which is available here:
http://www.roguebasin.com/index.php?title=Complete_Roguelike_Tutorial,_using_python%2Blibtcod

Additional contributions were made by Inspector Caracal.


---------------------
|  libtcod License  |
---------------------

libtcod 1.6.4 Python wrapper
Copyright (c) 2008,2009,2010,2012,2013,2016,2017 Jice & Mingos & rmtew
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * The name of Jice or Mingos may not be used to endorse or promote products
      derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY JICE, MINGOS AND RMTEW ``AS IS'' AND ANY
EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL JICE, MINGOS OR RMTEW BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
