# tanker
Game Clone of a simple round-based tank-Game. The Idea of the game is to have a couple of tanks on a 2D plane, which can shoot each other. 
Simple interactions with the terrain, like destroying it, are possible.

### Prerequisites 
* pygame 2.1.2, or newer
* python3


### History and Development 
I started this project in my second year of uni. Back then i just cramped it all in one main.py and hoped it worked. Of course at some point 
there were so many bugs it took more time to scroll through the file than to just start from scratch. And two years later i did.

As of today the code is structured to the point where i feel comfortable in expanding and improving the project.

## Gameplay
The game is round based. Meaning only one player can take actions at a time. A players turn ends as soon as he fires and the projectile either 
leaves the canvas or hits something.

<p align="center">
    <img width="600" src="https://github.com/dersiwi/tanker/blob/main/images/gameDemo-23112022-2.png" alt="Gameplay Screenshot, 23.11.2022">
    <br>
    Gameplay Screenshot, 23.11.2022
</p>

### How to play
0. Start `main.py`
1. Choose terrain (no selected terrain -> random terrain)
2. Choose amont (default 2) and type of player (default human)
3. Click Play

#### Controls 
Functions like `change_weapon` and adjusting the force can only be done via the GUI. `fire` is possible both by pressing `space` or the red fire button in the GUI.

For all other controls press `h` while in game to get the latest documentation.


### Start the game
Clone the repository and execute `main.py`. Should work like this (exemplary on a bash-console):
```sh
~/somefolder$ git pull https://github.com/dersiwi/tanker.git
~/somefolder$ cd tanker
~/somefolder/tanker$ python3 main.py
```
and the game should start. Pygame and any other missing packages can be installed using `pip install [package_name]`.

To see start-options call `$ python3 main.py --help`.

## Necessray development

### Player types
As of 08.06. the only working player-types are `human` and `random`. What i want to add in the future is a more intelligent player type that actually is a valid bot to play against.

### Rewarwd system and shop
Although a shop exists in which a player can select his weapons for the new round i want to intrododuce a system in which a player gets points based on how much damage he dealt. The player can then use these points to buy items in the shop.

The shop (currenlty) only contains only things that the player can fire. I want to add shields and mines to the shop as well.

Computer-players also have to be able to interact with the shop.

## Further development

### Levels

I think a single-player campain would be a great addition to the game. This is less of a development project but rather just content creation.

#### Infinity-Level
A level where the map expands infinitely to the right and the player has to get as far as possible.

### Buildings
Either as leve-objects or just design objects in a terrain buildings like bunkers that can also shoot could be fun.


### Controls
Store a key->control mapping in `controls.json` and give user ability to change key-bindings.