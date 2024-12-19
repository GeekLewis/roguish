from rooms import *
from rich.console import Console
from rich.layout import Layout
from rich.align import Align
import os
import time


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
        main_win.add(f"\n{self.name} attacks {target.name} with {self.weapon.name}")
        hit = rand(1, 21)+self.aim
        damage = (rand(1, self.weapon.dmg))+self.dmg_bonus
        target.hit(self.name, hit, damage) 

    def hit(self, attacker, hit, damage):
        if hit > self.defence:
            self.hp = max(self.hp - damage, 0)
            main_win.add(f'{attacker} hits {self.name} for {damage} damage',
                  f' ({self.hp}/{self.max_hp})')
            if self.hp == 0:
                self.alive = False
            
        else:
            main_win.add(f"{attacker} misses\n")

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
        xp (int): Players experience gained thru surviving the dungeon
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
        self.score = 0
        self.xp_level:dict = {
            1:49,
            2:99,
            3:199,
            4:399,
            5:799
        }

    def _level_up(self):
        while self.xp > self.xp_level[self.level]:
            main_win.add('\nYou gained a level!')
            self.level += 1
            # rewards for new level here
            self.hp += 8
            main_win.add(f'You gain 8 HP! ({self.hp} HP Total)')
            self.aim += 4
            main_win.add('Your accuracy increased!')
            self.defence += 4
            main_win.add('Your defense increased!')

    def collect_xp(self, xp_val:int):
        self.xp += xp_val
        self.add_score(xp_val)
        main_win.add(f'You gain {xp_val} experience.')
        if self.xp > self.xp_level[self.level]: self._level_up()

    def add_score(self, points:int):
        """
        method takes an integer value and adds it to the player's score
        """
        self.score += points


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
        f"Experience: {player.xp}\n"+
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
    time.sleep(2)
    update_char_window(player=player, mob=mob)
    while player.alive == True and mob.alive ==True:
        main_win.add(f'\nThe {mob.name} is attacking you!')
        action = input('Will you FIGHT or RUN?\n> ')
        if action.strip().lower() == 'run':
            pass
        elif action.strip().lower() == 'fight':
            player.attack(mob)
            mob.attack(player)
        else:
            main_win.add("I'm sorry you can't do that.")
        update_char_window(player=player, mob=mob)
    return player, mob


def create_room(entry_index:int, entry_direction:str, player_level:int) -> None:
    room_name = name_room()
    entry_door = mirror_directions[entry_direction]
    pos_exit_dirs = directions.copy()
    pos_exit_dirs.remove(entry_door)
    manditory_exit = choice(pos_exit_dirs)
    new_room = Room(
                    room_name, len(map), north=choice([True, False]), 
                    south=choice([True, False]), east=choice([True, False]),
                    west=choice([True, False])
                    )
    setattr(new_room, entry_door, True)
    setattr(new_room, manditory_exit, True)
    setattr(new_room, entry_door+"_closed", False)
    setattr(new_room, entry_door+"_target", entry_index)
    if choice(['yes', 'no']) == 'yes':
        new_room.monster = random_monster(player_level)
    map.append(new_room)
    return


def name_room() -> str:
    room_name = (choice(room_adj))+' '+choice(room_sub)
    return room_name


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
            #add 1 to player score here
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