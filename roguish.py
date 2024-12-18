from rooms import *
from rich.console import Console
from rich.layout import Layout
from rich.align import Align
import os
import time


class Windowpane:
    """This class is built for managing text for rich layout areas"""
    def __init__(self, layout_label:str, layout_pane_height:int):
        self.label:str = layout_label
        self.pane_height = layout_pane_height
        self.text_blob:str = ""
        self.cache:list = []

    def clear_cache(self):
        self.cache = []
        self.print_cache()
        
    def add(self, new_text:str):
        self.cache.append(new_text)
        if len(self.cache) == self.pane_height:
            del self.cache [0]
        self.print_cache()

    def cache_out(self):
        self.text_blob=""
        for i in self.cache:
            self.text_blob=self.text_blob+i+"\n"

    def print_cache(self):
        self.cache_out()
        layout[self.label].update(self.text_blob)
        console.print(layout, height=layout_height)


# This will initialize the screen layout for the Game
console = Console()
term_height = os.get_terminal_size().lines
layout_height = term_height-1

layout = Layout()
layout.split(
    Layout(name="title_bar",size=2),
    Layout(name="status_bar", size=3),
    Layout(name="body"),
)
layout["status_bar"].split_row(
    Layout(name="room_name", size=54),
    Layout(name="header_buffer"),
    Layout(name="score_box", size=20)
)
layout["body"].split_row(
    Layout(name="main_window"),
    Layout(name="margin", size=2),
    Layout(name="char_window", size=24)
)
layout["title_bar"].update(Align("[green1]Roguish", align="center"))
layout["header_buffer"].update(" ")
layout["margin"].update(" ")
layout["room_name"].update(" ")
layout["score_box"].update(" ")
layout["char_window"].update(" ")
layout["main_window"].update(" ")

main_win = Windowpane("main_window", layout_height-5)

console.print(layout, height=layout_height)

def update_status_bar(room_name:str, player_score:int) -> None:
    """Updates status bar 
    Args:
        room_name (str): Name of current room.
        player_score (int): Score from player
    """
    layout["room_name"].update(f"[blue]{room_name}[/blue]")
    layout["score_box"].update("[green]Score:[/green] "+ 
                f"[bright green]{player_score: >5}[/bright green] ")
    console.print(layout, height=layout_height)


# def update_main_window(text_block) -> None:
#     layout["main_window"].update(text_block)
#     console.print(layout, height=layout_height)


def update_char_window(player:Hero, mob:Monster=None) -> None:
    c_win_blob:str=(f"[magenta]Name:[/magenta] "+
        f"[bright magenta]{player.name}[/bright magenta]\n"+
        f"     Level: {player.level}\n"+
        f"Experiance: {player.xp}\n"+
        f"    Health: {player.hp}/{player.max_hp}\n"+
        f"    Weapon: {player.weapon.name}\n"+
        f"   Potions: {player.potion_count}\n")
    if mob:
        c_win_blob = c_win_blob +("\n\n"+
            f"[orange]{mob.name}[/orange]\n"+
            f"    Health: {mob.hp}/{mob.max_hp}\n"+
            f"    Weapon: {mob.weapon}")
    layout["char_window"].update(c_win_blob)
    console.print(layout, height=layout_height)
    

def test_string(string) -> bool:
    for char in string:
        if not char.isalpha():
            return False
    return True


def get_name() -> str:
    '''Gets name from user and validates that it is a valid string,
    which is less than 16 characters'''
    name_valid = False
    while name_valid == False:
        h_name: str = input('Name your hero: ')
        if len(h_name) > 16:
            main_win.add("\nLet's keep it under 16 letters, shall we?\n")
            main_win.print_cache()
        else:
            name_valid = test_string(h_name)
            if name_valid == False:
                main_win.add("\nPlease, use letters only.\n\n")
                main_win.print_cache()
    return h_name


def get_build(h_name:str) -> tuple:
    '''Retuns tuple with int values for hp, aim, defense, dmg_bonus'''
    while True:
        t_string=(f"[gold3]Very well, [green1]{h_name}[/green1]. \n"+
                           "Do you want to...\n\n ([bright_cyan]F[/bright_cyan])"+
                           "loat like a butterfly [bright_magenta](High defense)"+
                           "[/bright_magenta]\n ([bright_cyan]S[/bright_cyan])"+
                           "ting like a bee [bright_magenta](High Damage)"+
                           "[/bright_magenta]")
        main_win.add(t_string)
        main_win.print_cache()
        build_choice = input("> ")
        if build_choice.lower() == "f":
            return 8, 6, 12, 0
        elif build_choice.lower() == "s":
            return 14, 2, 8, 2
        else:
            print("\nTry Again\n")


def make_hero() -> Hero:
    '''Calls the h_name and build functions then uses that data to
    instantiate the player Hero class which is returned as an object'''
    h_name = get_name()
    build = get_build(h_name)
    player = Hero(name=h_name, hp=build[0], aim=build[1], defence=build[2],
                  dmg_bonus=build[3])
    return player


def welcome():
    main_win.add('[gold3]Welcome to the[/gold3] [red1]dungeon[/red1]!\n'+
    '[gold3]How many rooms can you survive?[/gold3]\n'+
    'Before you go further you must make your hero.\n')
    main_win.print_cache()


def show_hero(player):
    print(f'Hero:\nName: {player.name}')


def start_room() -> Room:
    '''Creates the only defined room in the game as our starting room'''
    start=Room(name="Entryway", index=0, east=True, west=True)
    return start


def help() -> None:
    print('This game is played with text commands typed into the command')
    print('prompt. To move you type the keyword GO followed by a direction')
    print('NORTH, SOUTH,EAST, WEST). Some objects in a room can be picked up')
    print('with the keyword TAKE, followed by the name of the object. If the')
    print('object is a weapon it will automatically replace any current')
    print('weapon you are weilding.')


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
        

def parser(current_room:Room, player:Hero, user_action:str) -> tuple:
    if user_action[0:2].lower() == 'go':
        current_room = go(current_room, user_action[3:].strip(), player.level)
        return current_room, player
    elif user_action.strip().lower() in directions:
        current_room = go(current_room, user_action.strip(), player.level)
        return current_room, player
    else:
        main_win.add("I don't know what you mean.")
        return current_room, player


def go(current_room:Room, direction:str, player_level:int) -> Room:
    if not direction.lower() in directions:
        main_win.add(f"{direction} is not a valid direction.")
        return current_room
    elif getattr(current_room, 'index') == 0 and direction == 'west':
        main_win.add("\n")
        main_win.add("That's the way out, and I'm afraid you can't leave.")
        return current_room
    elif getattr(current_room, direction.lower()) == False:
        main_win.add(f"You can't go {direction.lower()}")
        return current_room
    else:
        if getattr(current_room, direction+'_closed') == True:
            setattr(current_room, direction+'_target', len(map))
            create_room(current_room.index, direction, player_level)
            setattr(current_room, direction+'_closed', False)
    return map[getattr(current_room, direction+'_target')]


def game_loop(current_room:Room, player:Hero) -> object:
    while player.alive == True:
        layout["room_name"].update(current_room.name)
        update_status_bar(current_room.name, player.score)
        if  current_room.name[0:1].lower() in ['a', 'e', 'i', 'o', 'u']:
            main_win.add(f'\nYou are in an {current_room.name}.')
        else:
            main_win.add(f'\nYou are in a {current_room.name}.')
        if current_room.monster:
            main_win.add(f"You see a {current_room.monster.name},"+
                                 " moving to attack you")
            fight(player, current_room.monster)
            if current_room.monster.alive == False:
                print(f'The {current_room.monster.name} falls dead.')
                player.collect_xp(current_room.monster.xp_val)
                         
        main_win.add(current_room.get_exits())
        user_action:str = input('> ')
        current_room, player = parser(current_room, player, user_action)
    return player

def main():
    welcome()
    player = make_hero()
    update_char_window(player=player)
    main_win.clear_cache()
    main_win.print_cache()
    main_win.add(f'[gold3]Good luck, [/gold3][green1]{player.name}')
    main_win.print_cache()
    time.sleep(2)
    current_room = start_room()
    game_loop(current_room, player)
    if player.alive == False:
        print('You dead')


if __name__ == "__main__":
    main()