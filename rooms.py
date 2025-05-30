from random import choice
from typing import Optional, TYPE_CHECKING
from roomlib import adj as room_adj
from roomlib import sub as room_sub
from characters import *

if TYPE_CHECKING:
    from roguish import Monster

class Room:
    """
    A class representing a room in the dungeon.

    Attributes:
        name (str): Name of the room
        index (int): index number for refencing the rooms locatoin in
                    the map list
        north, south, east, west (bool): True indicated an exit
        _closed (bool): tells if player has passed thru that exit
        _target (int): set to the index number of the room that exit 
                    connects to. Value of -1 by default indicates that 
                    exit has not been assigned a room yet
        monster (object): if a room contains a monster that object will 
                    be stored here, but evaluates to False if empty.
        loot (object): if a room contains loot that object will be 
                    stored here, but evaluate False if empty
        item (object): if a room contains an item the player can pick up 
                    that object is stored here, but evaluates to False 
                    if empty 
    """
    def __init__(
                self, name:str, index:int, north:bool = False, 
                east:bool = False, south:bool = False,
                west:bool = False
                ) -> None:
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
        self.monster:Optional[Monster] = None
        self.loot:Optional[Weapon] = None
        self.item:Optional[Weapon] = None

    def get_exits(self) -> str:
        """
        Method to check and list the possible exit directions from this room
        """
        self.exits=[]
        for dir in directions:
            if getattr(self, dir) == True: self.exits.append(dir)
        if len(self.exits) == 1: 
            return (f'You see an exit to the {self.exits[0]}.')
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
