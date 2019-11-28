"""
The world class gives functionality to the map the player is currently on.
Based on squares / tiles. These will then have a value as such:
    ** Example **
    tile_type = { "
        "ST" : StartingTile, -> Starting point of the map
        "BT" : BlankTile, -> Nothing happens, player just moves.
        "ET" : EventTile,    -> Something happens
        "MT" : MonsterTile, -> Player fights / flees a monster
        "FI" : FindItemTile, -> Player found a specific or random item
        "NL" : NextLevelTile,     -> Sends player to another map. (Will need to somehow depict which map player goes to.
                                * In this example it is labeled as D1 (Sends player to Map #1, another tile will be
                                labeled D2 and will send the player to map #2. *
        " " : None -> Does nothing. Is a wall / area the player can not walk through, has to go around.
                }

    The map will be loaded into a list, then parsed for further functionality.
    Need some sort of delimiter to separate tiles / squares. For example:
    the pipe character | or something else.

    map = {"
    |D1|MT|BT|  |  |  |
    |MT|  |MT|MT|MT|BT|
    |ET|  |ST|  |  |MT|
    |MT|MT|FI|ET|MT|BT|
    |  |MT|  |  |  |MT|
    |  |FT|MT|BT|MT|D2|
    "}
"""

import glob
import os
import configparser
import random

import classes.enemies as enemies


class MapTile:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def intro_text(self):
        raise NotImplementedError("Create a subclass instead!")

    def modify_player(self, player):
        pass


class StartTile(MapTile):
    def intro_text(self):
        return """
        INSERT INTRO TEXT HERE
        """

class EnemyTile(MapTile):
    def __init__(self, x, y):
        r = random.random()
        if r < 0.50:
            self.enemy = enemies.GiantSpider()
            self.alive_text = "A giant spider jumps down from " \
                              "its web in front of you!"
            self.dead_text = "The corpse of a dead spider " \
                             "rots on the ground."
        elif r < 0.80:
            self.enemy = enemies.Ogre()
            self.alive_text = "An ogre is blocking your path!"
            self.dead_text = "A dead ogre reminds you of your triumph."
        elif r < 0.95:
            self.enemy = enemies.BatColony()
            self.alive_text = "You hear a squeaking noise growing louder" \
                              "...suddenly you are lost in s swarm of bats!"
            self.dead_text = "Dozens of dead bats are scattered on the ground."
        else:
            self.enemy = enemies.RockMonster()
            self.alive_text = "You've disturbed a rock monster " \
                              "from his slumber!"
            self.dead_text = "Defeated, the monster has reverted " \
                             "into an ordinary rock."

        super().__init__(x, y)

    def intro_text(self):
        text = self.alive_text if self.enemy.is_alive() else self.dead_text
        return text

    def modify_player(self, player):
        if self.enemy.is_alive():
            player.hp = player.hp - self.enemy.damage
            print("Enemy does {} damage. You have {} HP remaining.".
                  format(self.enemy.damage, player.hp))


class EndGameTile(MapTile):
    def modify_player(self, player):
        player.world.game_active = False

    def intro_text(self):
        # Disable game_active
        return """
        Congratulations! You have beaten the game!
        """


class FindGoldTile(MapTile):
    def __init__(self, x, y):
        self.gold = random.randint(1, 50)
        self.gold_claimed = False
        super().__init__(x, y)

    def modify_player(self, player):
        if not self.gold_claimed:
            self.gold_claimed = True
            player.gold = player.gold + self.gold
            print("+{} gold added.".format(self.gold))

    def intro_text(self):
        if self.gold_claimed:
            return """
            Another unremarkable part of the cave. You must forge onwards.
            """
        else:
            return """
            Someone dropped some gold. You pick it up.
            """

class FindItem(MapTile):
    """ Find Item tile -> Use Random to generate """
    pass

class NextLevel(MapTile):
    """ Go to next Level -> Code functionality to pull information from World Class"""
    def __init__(self, x, y):
        super().__init__(x, y)

    def intro_text(self, *args):
        if len(args) > 0:
            return args[0]
        else:
            return """ """

    def modify_player(self, player):
        player.world.Load_Map("level" + player.world.map_information['next_level'])

        player.x = player.world.start_tile_location[0]
        player.y = player.world.start_tile_location[1]

        print(player.world.current_map)

class EventTile(MapTile):
    """ Event Tile -> Use random function to throw special events """
    pass

class World:
    def __init__(self):
        self.maps_directory = os.getcwd() + "/maps/"
        self.available_maps = dict()
        self.current_map = []
        self.map_information = None
        self.map_format = None
        self.start_tile_location = None

    def Scan_Maps(self):
        """ Scan map directory for .map files, load into a dictionary, key = maps_name (i.e: level1) """

        maps = glob.glob(self.maps_directory + "*.map")   # Scan /maps/ directory and collect all .map files
        map_names = [os.path.basename(scanned).strip(".map") for scanned in glob.glob(self.maps_directory + "*.map")]  # put into a list
        self.available_maps = dict(zip(map_names, maps))  #  combine two lists to create a dictionary, maps name is the key (i.e: level1)


    tile_types = {
        "EG": EndGameTile,
        "EN": EnemyTile,
        "ET": EventTile,
        "ST": StartTile,
        "FI": FindItem,
        "NL": NextLevel,
        "  ": None,
    }

    def Load_Map(self, map_name):
        """ Load map functionality into a list """
        self.current_map.clear()

        config = configparser.ConfigParser()
        config.read(self.available_maps[map_name])  # reads .map file

        self.map_information = config['information']
        if not self.Verify_Map(self.map_information, config.get('layout', 'design')):  # pass parameters -> [information] section and the map design
            raise SyntaxError("[ERROR] - Invalid map configuration on map \"%s\"" % map_name)

        map_lines = [i for i in config.get('layout', 'design').splitlines() if i]  # Checks for valid map lines / strips white spaces.

        for y, map_row in enumerate(map_lines):  # run through each row in the map, give it an index with enumerate.
            row = []
            map_tile = map_row.split("|")  # Get each tile in the given row.
            map_tile = [t for t in map_tile if t]  # removes unnecessary white spaces, adds to list.
            for x, map_tile in enumerate(map_tile):
                tile_type = self.tile_types[map_tile]

                if tile_type == StartTile:
                    self.start_tile_location = x, y

                row.append(tile_type(x, y) if tile_type else None)
            self.current_map.append(row)

    def Verify_Map(self, map_information, map_data):
        if int(map_information['next_level']) > -1:   # map has a next level
            pass
        elif (map_data.count("|EG|") == 1) and (int(map_information['next_level']) == -1): # Game ends
            pass
        else:   # there was an error in the map configuration file...
            raise SyntaxError("[ERROR] - Invalid map configuration. Please see map configuration notes.")

        if map_data.count("|ST|") != 1:  # all maps must have a starting tile.
            return False

        lines = map_data.splitlines()
        lines = [l for l in lines if l]
        pipe_count = [line.count("|") for line in lines]
        for count in pipe_count:
            if count != pipe_count[0]:
                return False

        ## The above code checks for the pipe character "|". If it is unequal or missing,
        ## it will throw an error.
        return True

    def Tile_At(self, x, y):
        if x < 0 or y < 0:
            return None

        try:
            return self.current_map[y][x]
        except IndexError:
            return None


