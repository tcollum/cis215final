from classes.world import World, EnemyTile
from classes.player import Player
from collections import OrderedDict

import os

world = World()


class Game:
    def __init__(self):
        self.name = "Player"
        self.game_active = False


    def New_Game(self):
        """
        Initialize a new game.
        - Chadwick
        """
        self.name = input("What is your characters name: ")
        self.Start_Game("level1")

        # Create a user file with information
        # instantiate inventory class

    def Start_Game(self, map_name):
        """
        Starts a playable game
        - Chadwick
        """
        world.Scan_Maps() # Scan maps directory to populate maps list.
        world.Load_Map(map_name) # Will have to move this to somewhere else...
        self.game_active = True # Very last line


    def Save_Game(self):
        """
         Saves game to a configuration file in order to load.
        Current Status: Not working.
        """
        if os.path.isfile(""):
            user_input = input("Would you like to overwrite the previous save file? [y/n]")

            if user_input in ['Y', 'y']:
                print("Overwriting game save...")
                ### WRITE STUFF TO GAME SAVE FILE.INI

            else:
                print("Nothing saved...")

    def Play_Game(self):
        """
        Plays current game!
        original by Philip Johnson, modifications by Chadwick.
        """
        player = Player(world) # instantiate new player by giving it the loaded world model so it has all the map information.

        while player.is_alive() and self.game_active:
            room = world.tile_at(player.x, player.y) # Get current tile / room
            room.modify_player(player)

            if player.is_alive() and self.game_active:
                if room != world.tile_at(player.x, player.y): # On NL, room was not being updated to fix this, we check to see if there are any updates.
                    room = world.tile_at(player.x, player.y)

                room_strip = str(world.tile_at(player.x, player.y)).split()[0].strip('<')  # checks current tile player is on, strips away unnecessary information.
                if room_strip == "classes.world.StartTile":
                    print(room.level_name)

                print(room.intro_text())
                self.choose_action(room, player)

            elif not player.is_alive():
                print("%s has died! Game Over." % self.name)

    def choose_action(self, room, player):
        """ Choose an available action to modify player."""

        action = None
        while not action:
            available_actions = self.get_available_actions(room, player)
            action_input = input("Action: ")
            action = available_actions.get(action_input)
            print("")
            if action:
                action()
            else:
                print("Invalid action!")

    def get_available_actions(self, room, player):
        """ Scans tiles around the player and provides available actions. """

        actions = OrderedDict()
        print("Choose an action: ")
        if player.inventory:
            self.action_adder(actions, 'i', player.print_inventory, "Print inventory")
        if isinstance(room, EnemyTile) and room.enemy.is_alive():
            self.action_adder(actions, 'a', player.attack, "Attack")
        else:
            if world.tile_at(room.x, room.y - 1):
                self.action_adder(actions, 'n', player.move_north, "Go north")
            if world.tile_at(room.x, room.y + 1):
                self.action_adder(actions, 's', player.move_south, "Go south")
            if world.tile_at(room.x + 1, room.y):
                self.action_adder(actions, 'e', player.move_east, "Go east")
            if world.tile_at(room.x - 1, room.y):
                self.action_adder(actions, 'w', player.move_west, "Go west")
        if player.hp < 100:
            self.action_adder(actions, 'h', player.heal, "Heal")

        return actions

    def action_adder(self, action_dict, hotkey, action, name):
        action_dict[hotkey.lower()] = action
        action_dict[hotkey.upper()] = action
        print("{}: {}".format(hotkey, name))

        # IMPLEMENT ACTION CODING

