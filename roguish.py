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

def start_room() -> object:
    start=Room(name="Entryway", index=0, east=True, west=True)
    return start

def parser(current_room:object, user_action:str) -> object:
    if user_action[0:2].lower() == 'go':
        current_room = go(current_room, user_action[3:].strip())
        return current_room
    elif user_action.strip().lower() in directions:
        current_room = go(current_room, user_action.strip())
        return current_room
    else:
        print("I don't know what you mean.")
        return current_room

def game_loop(current_room:object, player:object) -> object:
    while player.alive == True:
        if  current_room.name[0:1].lower() in ['a', 'e', 'i', 'o', 'u']:
            print(f'\nYou are in an {current_room.name}.')
        else:
            print(f'\nYou are in a {current_room.name}.')
        
        print(current_room.get_exits())
        user_action:str = input('> ')
        current_room = parser(current_room, user_action)


def main():
    welcome()
    player = make_hero()
    print(f'Good luck, {player.name}')
    current_room = start_room()
    player = game_loop(current_room, player)
    if player.alive == False:
        pass

if __name__ == "__main__":
    main()
