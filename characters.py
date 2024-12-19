from random import randrange as rand
from random import choice
from weapons import *


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


def main():
    pass


if __name__ == "__main__":
    main()