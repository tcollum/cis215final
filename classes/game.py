from classes.world import World
from classes.player import Player

import os
import configparser

world = World()


class Game:
    def __init__(self):
        self.name = "Player"
        self.game_active = False


    def New_Game(self):
        self.name = input("What is your characters name: ")
        self.Start_Game("level1")

        # Create a user file with information
        # instantiate inventory class

    def Start_Game(self, map_name):
        world.Scan_Maps() # Scan maps directory to populate maps list.
        world.Load_Map(map_name) # Will have to move this to somewhere else...
        self.game_active = True # Very last line


    def Save_Game(self):
        if os.path.isfile(""):
            user_input = input("Would you like to overwrite the previous save file? [y/n]")

            if user_input in ['Y', 'y']:
                print("Overwriting game save...")
                ### WRITE STUFF TO GAME SAVE FILE.INI

            else:
                print("Nothing saved...")

    def Play_Game(self):
        player = Player(world) # instantiate new player by giving it the loaded world model so it has all the map information.
        print(player.x)

        # IMPLEMENT ACTION CODING

