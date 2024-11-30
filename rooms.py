from random import choice
from roomlib import adj as room_adj
from roomlib import sub as room_sub

class Room:
    def __init__(self, name:str, index:int, north:bool = False, east:bool = False,
                  south:bool = False, west:bool = False) -> None:
        self.name = name
        self.index = index
        self.north = north
        self.east = east
        self.south = south
        self.west = west
        self.north_closed = True
        self.south_closed = True
        self.east_closed = True
        self.west_closed = True
        self.north_target = -1
        self.south_target = -1
        self.east_target = -1
        self.west_target = -1

    def get_exits(self) -> str:
        self.exits=[]
        for dir in directions:
            if getattr(self, dir) == True: self.exits.append(dir)
        if len(self.exits) == 1: return (f'You see an exit to the {self.exits[0]}.')
        else:
            oxford = self.exits.pop()
            oxford = 'and '+oxford
            self.exits.append(oxford)
            self.e_str="You see exits to the "
            for dir in self.exits:
                self.e_str=self.e_str+dir
                if not 'and' in dir:self.e_str=self.e_str+', '
                else:self.e_str = self.e_str+'.'
            return self.e_str
        
map = []
directions = ['north', 'south', 'east', 'west']

mirror_directions = {
    'north': 'south',
    'south': 'north',
    'east': 'west',
    'west': 'east'
}

def create_room(entry_index:int, entry_direction:str) -> None:
    room_name = name_room()
    entry_door = mirror_directions[entry_direction]
    pos_exit_dirs = directions.copy()
    pos_exit_dirs.remove(entry_door)
    manditory_exit = choice(pos_exit_dirs)
    new_room = Room(room_name, len(map), north=choice([True, False]), 
                    south=choice([True, False]), east=choice([True, False]),
                    west=choice([True, False]))
    setattr(new_room, entry_door, True)
    setattr(new_room, manditory_exit, True)
    setattr(new_room, entry_door+"_closed", False)
    setattr(new_room, entry_door+"_target", entry_index)
    map.append(new_room)
    return

def name_room() -> str:
    room_name = (choice(room_adj))+' '+choice(room_sub)
    return room_name

def go(current_room:object, direction:str) -> object:
    if not direction.lower() in directions:
        print(f"{direction} is not a valid direction.")
        return current_room
    elif getattr(current_room, direction.lower()) == False:
        print(f"You can't go {direction.lower()}")
        return current_room
    else:
        if getattr(current_room, direction+'_closed') == True:
            setattr(current_room, direction+'_target', len(map))
            create_room(current_room.index, direction)
            setattr(current_room, direction+'_closed', False)
    return map[getattr(current_room, direction+'_target')]
