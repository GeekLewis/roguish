from rooms import *


def test_string(string) -> bool:
    for char in string:
        if not char.isalpha():
            return False
    return True


def get_name() -> str:
    name_valid = False
    while name_valid == False:
        h_name: str = input('Name your hero: ')
        if len(h_name) > 16:
            print("\nLet's keep it under 16 letters, shall we?\n\n")
        else:
            name_valid = test_string(h_name)
            if name_valid == False:
                print("\nUse letters only.\n\n")
    return h_name


def get_build() -> tuple:
    while True:
        print("\n\n")
        print("Do you want to \n",
              "\n (F)loat like a butterfly\n (S)ting like a bee")
        build_choice = input("> ")
        if build_choice.lower() == "f":
            return 8, 6, 12, 0
        elif build_choice.lower() == "s":
            return 14, 2, 8, 2
        else:
            print("\nTry Again\n")


def make_hero() -> object:
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


def help() -> None:
    print('This game is played with text commands typed into the command prompt.')
    print('To move you type the keyword GO followed by a direction (NORTH, SOUTH')
    print('EAST, WEST). Some objects in a room can be picked up with the keyword')
    print('TAKE, followed by the name of the object. If the object is a weapon')
    print('it will automatically replace any current weapon you are weilding.')


def parser(current_room:object, player:object, user_action:str) -> object:
    if user_action[0:2].lower() == 'go':
        current_room = go(current_room, user_action[3:].strip(), player.level)
        return current_room, player
    elif user_action.strip().lower() in directions:
        current_room = go(current_room, user_action.strip(), player.level)
        return current_room, player
    else:
        print("I don't know what you mean.")
        return current_room, player


def game_loop(current_room:object, player:object) -> object:
    while player.alive == True:
        if  current_room.name[0:1].lower() in ['a', 'e', 'i', 'o', 'u']:
            print(f'\nYou are in an {current_room.name}.')
        else:
            print(f'\nYou are in a {current_room.name}.')
        if current_room.monster:
            print(f'You see a {current_room.monster.name}, moving to attack you')
            player, current_room.monster = fight(player, current_room.monster)
        print(current_room.get_exits())
        user_action:str = input('> ')
        current_room, player = parser(current_room, player, user_action)


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