from dataclasses import dataclass, field


@dataclass
class Weapon:
    """
    A dataclass to represent weapons or any object that deals damage,
    no methods.

    Attributes:
        name (str): Descriptive name of object 
        dmg (int): This number determines the top of the randrange used 
                    for deteriming damage, think d6 or d10 from TTRPGs
        bonus (int): value added to the damage after the random roll
        drop (bool): if true when the monster dies this weapon drops
                    to the room, and can be picked up by the player
    """
    name: str
    dmg: int
    bonus: int
    drop: bool


weapons_data = {
    'vicious teeth':{
        'dmg': 7,
        'bonus': 0,
        'drop': False,
    },
    'fists':{
        'dmg': 4,
        'bonus': 0,
        'drop': False
    },
    'dagger':{
        'dmg': 6,
        'bonus': 0,
        'drop': True
    },
    'short sword':{
        'dmg': 8,
        'bonus': 0,
        'drop': True
    },
    'long sword':{
        'dmg': 12,
        'bonus': 0,
        'drop': True
    },
    'magic sword':{
        'dmg': 16,
        'bonus': 4,
        'drop': True,
    }

}
def main():
    pass

if __name__ == '__main__':
    main()