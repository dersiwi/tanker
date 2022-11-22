
class Weapon():
    #("Name", explosionRadius, amount, damage)
    def __init__(self,name, damage, amount, explosionRadius):
        self.name = name
        self.amout = amount
        self.damage = damage
        self.explosionRadius = explosionRadius

    def getSmallMissile():
        return SmallMissile()


class SmallMissile(Weapon(name="Small Missile", damage=10, amount=1000, explosionRadius=20)):
    pass

     