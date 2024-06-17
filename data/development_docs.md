

Code & Workings

# GUI-Elements
## Menus
Menu-Configurations like height, color width are defined in `data/menus.json`. Attributes :
 - `width` and `height` are float-values, because they represent multipliers of the screen-width and screen-height respectively 

### Menus
Menus and globals are partly in `data/menus.json` and partly hardcoded in the python files. Todo is to just move them all into .json files.


# Terrain
Terrains are created using mathematical functions, that are defined in an interval from `[0, screen_width]`. The function value `f(x)` relates to the terrain-height at pixel `x`. Where the 0th pixel is the left most pixel of the screeen.

# Weapons
Weapons are loaded and stored in `data/weapons.json`. There exist multiple weapons-types, that also have different attributes;
All Weapons have these attributes in common : 

- `name` : Name of the 
- `weapon_id` : integer that unambiguously identifies this weapon
- `weapon_type` : can be one of the types ( as of 01.02.2024 either 0 or 1)
- `initial_amount` : initial amount the player posesses 

## Workings 
There are many different classes related to weapons, here a quick overview:
- `Weapon` :
- `TypeNWeapon` : Subclass of Weapon. Implement the return of different WEapons
- `Weapon_Executor` : Each weapon-type has it's own Weapon_Executor. As soon as a weapon is fired by the player, it creates an instance of it's Weapon_Executor, whoose most important function is to implement a gameloop-iteration, which is called by the gameloop.

## Weapon-types
Weapon types are used to differentiate how a weapon behaves, most importantly after firing. For example, a projectile is just fired and explodes. A airstrike however is planned by the user after firing. The implemented types are : 

 - type 0 - Regular projectile; choose a force and an angle and shoot your projectile
    - `damage` : that is dealt to a player if he is in exlposion radius
    - `explosion_radius` : radius when the projectile collides


-  type 1 - Airstrikes; choose a location with your mouse. Unique types for thisweapons-type 
    - `accuracy` : Determines how accurate the bombs are being dropped on target
    - `weapon_id_to_drop` : an ID of a type 0 weapon that will be dropped by the airplane
    - `n_drops` : the amount of weapons that will be dropped by the airplane

- type 2 - Vulcano bombs

### How to add a weapon-type

1. Add the weapon class to the weapons.json
2. Add variable `Weapon.TYPE_N = N` and add it to the `Weapon.TYPES`-list
3. Implement class `TypeNWeapon` and a `Weapon_Executor` for this class
4. Add TYPE_N-Clause to elif-statements in Constructor of `WeaponManager`.