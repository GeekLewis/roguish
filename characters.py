from random import randrange as rand
from random import choice
from weapons import *


class Character:
    def __init__(self, name: str, hp: int, aim: int, defence: int, 
                 weapon:str = 'fists', dmg_bonus: int=0) -> None:
        self.aim = aim 
        self.name = name 
        self.hp = hp
        self.max_hp = hp
        self.defence = defence
        self.dmg_bonus = dmg_bonus
        self.weapon = Weapon(name=weapon, dmg=weapons_data[weapon]['dmg'],
                            bonus=weapons_data[weapon]['bonus'],
                            drop=weapons_data[weapon]['drop'])


    def attack(self, target):
        print(f"{self.name} attacks {target.name}\n")
        hit = rand(self.aim)+1
        damage = (rand(self.weapon.dmg)+1)+self.dmg_bonus
        target.hit(self.name, hit, damage) 

    def hit(self, attacker, hit, damage):
        if hit > self.defence:
            self.hp = max(self.hp - damage, 0)
            print(f"{attacker} hits {self.name} for {damage} damage\n\n")
        else:
            print(f"{attacker} misses\n\n")

    def check_health(self):
        print (f"{self.name} has {self.hp}/{self.max_hp} health")

    #def heal(self):
    #    print (f"{self.name} tries to heal")
    #    boost = rand(self.heal)+1
    #    self.hp = min(self.hp + boost, self.max_hp)
    #    print (f"{self.name} regains health")
    #    self.check_health()

    def block(self):
        pass


class Monster(Character):
    def __init__(
            self, name: str, hp: int, aim: int, defence: int, 
            xp_val: int, dmg_bonus: int=0) -> None:
        super().__init__(name, hp, aim, defence)
        self.xp_val = xp_val

class Hero(Character):
    def __init__(
            self, name: str, hp: int, aim: int, defence: int, 
            dmg_bonus: int=0) -> None:
        super().__init__(name, hp, aim, defence)
        self.xp:int = 0
        self.level:int = 1
        self.alive:bool = True
        self.potion = False
        self.potion_count = 0


enemy_data = {
    "wolf":{
        "name": "Wolf",
        "hp": 10,
        "aim": 2,
        "defence": 8,
        "xp_val": 8,
        "weapon": "vicious teeth",
        "dmg_bonus": 0
    },
    "zombie":{
        "name": "Lurching Zombie",
        "hp": 18,
        "aim": 0,
        "defence": 6,
        "xp_val": 8,
        "weapon": "fists",
        "dmg_bonus": 0
    },
    "skeleton":{
        "name": "Shambling Skeleton",
        "hp": 16,
        "aim": 2,
        "defence": 8,
        "xp_val": 10,
        "weapon": "short sword",
        "dmg_bonus": 0
    },
    "bandit":{
        "name": "Highway Bandit",
        "hp": 24,
        "aim": 6,
        "defence": 12,
        "xp_val": 18,
        "weapon": "dagger",
        "dmg_bonus": 0
    },
    "soldier":{
        "name": "Enemy Soldier",
        "hp": 28,
        "aim": 8,
        "defence": 14,
        "xp_val": 35,
        "weapon": "short sword",
        "dmg_bonus": 0
    },
    "barbarian":{
        "name": "Hulking Barbarian",
        "hp": 40,
        "aim": 5,
        "defence": 9,
        "xp_val": 60,
        "weapon": "long sword",
        "dmg_bonus": 4
    }
}


mob_difficulty = {
    1:['wolf', 'zombie', 'skelton'],
    2:['bandit', 'soldier'],
    3:['barbarian']
}


def random_monster(player_level:int) -> object:
    mob_list = mob_difficulty[player_level]
    picked_mob = choice(mob_list)
    mob = Monster(name=picked_mob, hp=enemy_data[picked_mob]['hp'],
                  aim=enemy_data[picked_mob]['aim'],
                  defence=enemy_data[picked_mob]['defence'],
                  xp_val=enemy_data[picked_mob]['xp_val'],
                  dmg_bonus=enemy_data[picked_mob]['dmg_bonus'])
    return mob

def fight(player:object, mob:object) -> tuple:
    pass

def main():
    pass


if __name__ == "__main__":
    main()