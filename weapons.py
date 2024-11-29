class Weapon:
    def __init__(self, name: str, dmg: int, value: int) -> None:
        self.name = name
        self.dmg = dmg
        self.value = value

bite = Weapon('vicious teeth', dmg=7, value=0)
unarmed = Weapon('fists', dmg=4, value=0)
dagger = Weapon('dagger', dmg=6, value=10)
short_sword = Weapon('short sword', dmg=8, value=20)
long_sword = Weapon('long sword', dmg=12, value=50)
magic_sword = Weapon('magic sword', dmg=20, value=100)

def main():
    pass

if __name__ == '__main__':
    main()