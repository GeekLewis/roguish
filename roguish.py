from characters import *
from rooms import *

def test_string(string) ->bool:
    for char in string:
        if not char.isalpha():
            return False
    return True

def get_name() -> str:
    name_valid = False
    while name_valid == False:
        h_name: str = input('Name your hero: ')
        name_valid = test_string(h_name)
        if name_valid == False:
            print("\nUse letters only.\n\n")
    return h_name

def get_build() ->tuple:
    while True:
        print("\n\n")
        print("Do you want to \n",
              "\n (F)loat like a butterfly\n (S)ting like a bee")
        build_choice = input("?")
        if build_choice.lower() == "f":
            return 8, 6, 12, 0
        elif build_choice.lower() == "s":
            return 14, 2, 8, 2
        else:
            print("\nTry Again\n")

def make_hero() ->object:
    h_name = get_name()
    build = get_build()
    player = Hero(h_name, build[0], build[1], build[2], build[3])
    return player

def welcome():
    print('Welcome to the dungeon!\n',
          'How many rooms can you survive?\n',
          'Before you go further you must make your hero.\n')

def show_hero(player):
    print(f'Hero:\nName: {player.name}')

def main():
    welcome()
    player = make_hero()
    print(player.name)

if __name__ == "__main__":
    main()
