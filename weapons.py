import json


PATH = "data\\weapons.json"

class Weapon:
    TYPE_0 = 0
    TYPE_1 = 1
    def __init__(self, name, weapon_id, w_type, amount):
        self.name = name
        self.weapon_id = weapon_id
        self.amount = amount
        self.w_type = w_type

    def get_copy(self):
        pass

    def decrementAmount(self):
        self.amount -= 1

    def hasAmmoLeft(self):
        return self.amount >= 1

class TypeZeroWeapon(Weapon):
    def __init__(self, name, weapon_id, w_type, damage, amount, explosion_radius):
        super().__init__(name, weapon_id, w_type, amount)
        self.damage = damage
        self.explosion_radius = explosion_radius

    def get_copy(self):
        return TypeZeroWeapon(self.name, self.weapon_id, self.w_type, self.damage, self.amount, self.explosion_radius)


class TypeOneWeapon(Weapon):
    def __init__(self, name, weapon_id, w_type, amount, accuracy, weaponweapon_id_to_drop, n_drops, cooldown):
        super().__init__(name, weapon_id, w_type, amount)
        self.accuracy = accuracy
        self.weaponweapon_id_to_drop = weaponweapon_id_to_drop
        self.n_drops = n_drops
        self.cooldown = cooldown

    def get_copy(self):
        return TypeOneWeapon(self.name, self.weapon_id, self.w_type, self.amount, self.accuracy, self.weaponweapon_id_to_drop, self.n_drops, self.cooldown)

    
class WeaponsManager:

    instance = None


    def get_instance():
        if WeaponsManager.instance == None:
            WeaponsManager.instance = WeaponsManager(PATH)
        return WeaponsManager.instance

    def __init__(self, path) -> None:
        with open(path, "r") as file:
            data = json.load(file)

        self.weapons : dict[str, list[Weapon]] = {Weapon.TYPE_0 : [],
                                                  Weapon.TYPE_1 : []}
    
        for typezero in data[str(Weapon.TYPE_0)]:
            self.weapons[Weapon.TYPE_0].append(TypeZeroWeapon(name = typezero["name"],
                                                        weapon_id = typezero["weapon_id"],
                                                        w_type = typezero["weapon_type"],
                                                       damage = typezero["damage"],
                                                       amount = typezero["initial_amount"],
                                                       explosion_radius = typezero["explosion_radius"]))
        for typezero in data[str(Weapon.TYPE_1)]:
            self.weapons[Weapon.TYPE_1].append(TypeOneWeapon(name = typezero["name"],
                                            amount = typezero["initial_amount"],
                                            weapon_id = typezero["weapon_id"],
                                            w_type = typezero["weapon_type"],
                                            accuracy=typezero["accuracy"],
                                            weaponweapon_id_to_drop=typezero["weapon_id_to_drop"],
                                            n_drops=typezero["n_drops"],
                                            cooldown=typezero["cooldown"]))
            
    def get_initial_weapons(self) -> list[Weapon]:
        init_weapons = []
        for w_type in self.weapons:
            for weapon in self.weapons[w_type]:
                if weapon.amount > 0:
                    init_weapons.append(weapon.get_copy())
        return init_weapons
    
    def get_weapon_by_id(self, weaponid : int) -> Weapon:
        for w_type in self.weapons:
            for weapon in self.weapons[w_type]:
                if weapon.weapon_id == weaponid:
                    return weapon.get_copy()
        raise ValueError("Could not find weapon with weaponid %s"%weaponid)