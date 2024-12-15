from random import randrange as rand
from random import choice
from weapons import *


class Character:
    """
    Base class for all in game creatures PC or NPC

    Attributes:
        name (str): name of the character/creature
        hp (int): health points, at initialization it is used to also 
                set max_hp attr. hp is used to track damage.
        aim (int): a value that is added to the randrange of 1-20 used
                to beat opponents defence score
        defence (int): value that is a comnination of armor or
                manuverability, this number must be beat to score a hit
        weapon (object): place to store Weapon class object, if none is
                provided it will default to 'fists' 
        dmg_bonus (int): additional damage bomus granted by the 
                character/creature beyond any weapon damage
        alive (bool): tells if the character/creature is alive, set to
                True at creation
    """
    def __init__(self, name: str, hp: int, aim: int, defence: int, 
                 weapon:str = 'fists', dmg_bonus: int=0) -> None:
        self.name = name 
        self.hp = hp
        self.max_hp = hp
        self.aim = aim
        self.defence = defence
        self.dmg_bonus = dmg_bonus
        self.weapon = Weapon(name=weapon, dmg=weapons_data[weapon]['dmg'],
                            bonus=weapons_data[weapon]['bonus'],
                            drop=weapons_data[weapon]['drop'])
        self.alive:bool = True

    def attack(self, target):
        print(f"\n{self.name} attacks {target.name} with {self.weapon.name}")
        hit = rand(1, 21)+self.aim
        damage = (rand(1, self.weapon.dmg))+self.dmg_bonus
        target.hit(self.name, hit, damage) 

    def hit(self, attacker, hit, damage):
        if hit > self.defence:
            self.hp = max(self.hp - damage, 0)
            print(f'{attacker} hits {self.name} for {damage} damage',
                  f' ({self.hp}/{self.max_hp})')
            if self.hp == 0:
                self.alive = False
        else:
            print(f"{attacker} misses\n")

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
    """
    Subclass of Character for NPC monsters

    Attributes:
        xp_val (int): experiance value given to Hero for defeating the 
                    monster
    """
    def __init__(
            self, name: str, hp: int, aim: int, defence: int,
            xp_val: int, weapon:str = 'fists', dmg_bonus: int=0) -> None:
        super().__init__(name, hp, aim, defence)
        self.xp_val = xp_val

class Hero(Character):
    """
    Subclass of Character for the player

    Attributes:
        xp (int): Players experience gaind thru surviving the dungeon
        level (int): Indicates the player's current level, used to 
                    determine which monsters are allowed to spawn and
                    may indicated other benefits from advancement
        potion (bool): Simple bool to check if player has, and thus can 
                    use healing potions
        potion_count (int): tracks how many potions the player has
        xp_level (dict): a built in dictionary to determine at what
                    experience count does the player level up
    """
    def __init__(
            self, name: str, hp: int, aim: int, defence: int, 
            dmg_bonus: int=0) -> None:
        super().__init__(name, hp, aim, defence)
        self.xp:int = 0
        self.level:int = 1
        self.potion = False
        self.potion_count = 0
        self.xp_level:dict = {
            1:49,
            2:99,
            3:199,
            4:399,
            5:799
        }

    def _level_up(self):
        while self.xp > self.xp_level[self.level]:
            print('\nYou gained a level!')
            self.level += 1
            # rewards for new level here
            self.hp += 8
            print(f'You gain 8 HP! ({self.hp} HP Total)')
            self.aim += 4
            print('Your accuracy increased!')
            self.defence += 4
            print('Your defense increased!')

    def collect_xp(self, xp_val:int):
        self.xp += xp_val
        print(f'You gain {xp_val} experience. ({self.xp} Total.)')
        if self.xp > self.xp_level[self.level]: self._level_up()


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
    1:['wolf', 'zombie', 'skeleton'],
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
                  dmg_bonus=enemy_data[picked_mob]['dmg_bonus'],
                  weapon=enemy_data[picked_mob]['weapon'])
    return mob


def fight(player:Hero, mob:Monster) -> tuple:
    while player.alive == True and mob.alive ==True:
        print(f'\nThe {mob.name} is attacking you!')
        action = input('Will you FIGHT or RUN?\n> ')
        if action.strip().lower() == 'run':
            pass
        elif action.strip().lower() == 'fight':
            player.attack(mob)
            mob.attack(player)
        else:
            print("I'm sorry you can't do that.")
    return player, mob
        

def main():
    pass


if __name__ == "__main__":
    main()