
class Weapon():
    #("Name", explosionRadius, amount, damage)
    def __init__(self, name, damage, amount, explosionRadius):
        self.name = name
        self.amount = amount
        self.damage = damage
        self.explosionRadius = explosionRadius
    
    def decrementAmount(self):
        self.amount -= 1
    
    def hasAmmoLeft(self):
        return self.amount > 0

    def getSmallMissile():
        return SmallMissile()
    
    def getVulcanoBomb():
        return VulcanoBomb()
    
    def getBall():
        return Ball()
    
    def getBigBall():
        return BigBall()


class SmallMissile(Weapon):
    def __init__(self):
        super().__init__(name="Small Missile", damage=10, amount=1000, explosionRadius=20)

class VulcanoBomb(Weapon):
    def __init__(self):
        super().__init__(name="VulcanoBomb", damage=50, amount=100, explosionRadius=50)

class Ball(Weapon):
    def __init__(self):
        super().__init__(name="Ball", damage=200, amount=50, explosionRadius=100)

class BigBall(Weapon):
    def __init__(self):
        super().__init__(name="Big Ball", damage=300, amount=10, explosionRadius=300)
        
