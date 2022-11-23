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
The game is round based. Meaning only one player can do actions at a time. A players turn ends as soon as he fires and the projectile either 
leaves the canvas or hits something. 

<p align="center">
    <img width="600" src="https://github.com/dersiwi/tanker/blob/main/images/gameDemo-23112022-2.png" alt="Gameplay Screenshot, 23.11.2022">
    <br>
    Gameplay Screenshot, 23.11.2022
</p>

### How to play
#### Check prerequisites
As of 23.11.2022, there is no executable version of the game. So you have to start the game either via commandline or by clicking on it.
First of all, make sure you have python installed;

```
/yourfolder$ python3 --version
Python 3.10.6
/yourfolder$ 
```
or 
```
/yourfolder$ python --verison
Python 3.10.6
/yourfolder$ 
```
Now, check if have pygame installed;
```
/yourfolder$ python3
Python 3.10.6 (main, Nov  2 2022, 18:53:38) [GCC 11.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import pygame
pygame 2.1.2 (SDL 2.0.16, Python 3.10.6)
Hello from the pygame community. https://www.pygame.org/contribute.html
>>> 

```
If your responses resemble the ones above, you are ready to go. As you can see the code snippets above 
are made in a linux console, they should however look the same in a windwos console.

#### Start playing
After you pulled the repository in a directory, either double click main.py or execute 
```
yourfolder$ python3 main.py
```
and the game should start.
