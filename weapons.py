class Weapon:
    def __init__(self, name: str, dmg: int, bonus: int, drop: bool) -> None:
        self.name = name
        self.dmg = dmg
        self.value = value

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