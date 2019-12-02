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
        self.map_intro = None
        self.map_name = None

    @property
    def intro_text(self):
        return self.map_intro

    @intro_text.setter
    def intro_text(self, text):
        self.map_intro = text

    @property
    def level_name(self):
        return self.map_name

    @level_name.setter
    def level_name(self, name):
        self.map_name = name

    def modify_player(self, player):
        pass


class StartTile(MapTile):
    def intro_text(self):
        return MapTile.intro_text

    def modify_player(self, player):
        MapTile.level_name = player.world.map_information['name']
        MapTile.intro_text = player.world.map_information['intro']

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
            
class SpecialRoom(MapTile):
    def __init__(self, x, y):
        """Creates rewards for the player that are chosen based on the random
           number generator function once the player enters the special room.
           Built into the function are found/missing text statements that will
           populate if the reward has already been claimed if the player has
           visited the room."""
           
        r = random.random()
        if r < 0.60:
            self.reward = reward.ChestOfChuckECheeseTokens()
            self.found_text = "You found a chest of Chuck E. Cheese Tokens. " \
                              "You can use these to buy much needed supplies!"

            self.missing_text = "An empty chest indicates someone beat you " \
                                "this room."

        elif r < 0.75:
            self.reward = reward.MonopolyMoney()
            self.found_text = "You find a Monopoly game set overflowing with" \
                              "Monopoly money, a Monopoly game board, and a" \
                              "few game pieces. Congrats on your lucky find!" \
                              "Use this Monopoly Money to buy supplies from" \
                              "the vending machine."

            self.missing_text = "You find a Monopoly game set containing a" \
                                "Monopoly game board and a few game pieces" \
                                "but all of the Monopoly money has been taken." \
                                "Better luck next time."
        elif r < 0.85 :
            self.reward = reward.VisaGiftCard()
            self.found_text = "Lucky you, you stumbled across a wallet" \
                              "containing a visa gift card. Use this visa" \
                              "gift card to stock up on supplies at your" \
                              "neighborhood vending machine."

            self.missing_text = "You discover a wallet with a driver's" \
                                "license, a photo of happy family, a Sam's" \
                                "club membership card, and a Blockbuster" \
                                "Video rental card. One slot in the wallet" \
                                "is missing a rather valuable card."
        else:
            self.reward = reward.TwentyCasesOfRedBull()
            self.found_text = "Upon clearing the cobwebs off a very dirty" \
                              "set of bookshelves you discover, much to your" \
                              "delight, twenty cases of Red Bull. Use these" \
                              "to restore your strength between battles with" \
                              "enemies."

            self.missing_text = "Nearing a set of bookshelves that look" \
                                "conspicously clean compared to the rest of" \
                                "the room, you find a few empty cans of Red" \
                               "Bull and the outline of what appears to" \
                               "have been a stockpile of the delicious" \
                               "drink. Sadly, it looks like someone beat" \
                               "you to whatever was stockpiled there."
    super().__init__(x, y)
    
    def intro_text(self):
       text = self.found_text if self.reward.is_found() else self.missing_text
       return text

   def assigningRewardValues(self, player): # function that uses if else statements to break down points into categories
      if self.reward.is_found():
         if self.reward == monopoly_money:
            monopoly_money += self.reward.value
         elif self.reward == chuck_e_cheese_token:
            chuck_e_cheese_token += self.reward.value
         elif self.reward == visa_gift_card:
            visa_gift_card += self.reward.value
         elif self.reward == twenty_cases_red_bull:
            twenty_cases_of_red_bull += self.reward.value
         else:
            pass
            return monopoly_money, chuck_e_cheese_token, visa_gift_card, twenty_cases_of_red_bull

   def returningRewardsAsCredit(self, player): #function to return points as credit
      if self.reward.is_found():
         player.credit += self.reward.value
         print("Congratulations! You have found a reward worth {} in credit. You now" \
               "have {} in credit.".
               format(self.reward.value, player.credit))
               return player.credit 
         
class EndGameTile(MapTile):
    """
     Player lands on |EG| Tile, ends the game
    Current Status: Not working.
    """
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
    def __init__(self, x, y):
        """Creates a tile that enables the player to find an item
           (thingsToEat, reward, weapon, etc.) based on a random number generator."""

        r = random.random()
        if r < 0.20:
            self.findItem = findItem.TwoBottlesOfAspirin()
            self.found_text = "After clearing the cobwebs off a dark and dank corner" \
                               "of the room, you notice two bottles lying on the ground." \
                               "You pick them up and wipe the sludge from the front of them" \
                               "so you can read their labels. Much to your surprise and sheer" \
                               "delight you find yourself with teo bottles of aspirin in hand."

            self.missing_text = "One corner of the room you notice the ground is remarkably free" \
                                "cobweb-free compared to the rest of the room. Two clear round" \
                                "impressions have been left in the sludge on the ground as if something" \
                                "or perhaps some things had once been there."

            elif r < 0.45:
                self.findItem = findItem.SixCasesOfRedBull()
                self.found_text = "You make your way further into the dark room" \
                                  "and nearly trip over something in your path." \
                                  "You look down to see what has caused you to" \
                                  "stumble and nearly do a happy dance. There at" \
                                  "your feet, lay six cases of Red Bull energy" \
                                  "drink. Now there's something that will come" \
                                  "in handy after a long day of doing battle" \
                                  "with your enemies you think to yourself as you" \
                                  "start to make room in your pack for them."

                self.missing_text = "As you make your way further into the dark" \
                                    "room, you come to a clearing in the road," \
                                    "which you find odd. There seems to have been" \
                                    "something stored in the middle of the road" \
                                    "at one point. The outline in the dust on the" \
                                    "road reflects it to be sure. Shrugging, you" \
                                    "make your way on down the road."

            elif r < .70:
                self.findItem = findItem.BottleOfRum()
                self.found_text = "You come across a rocky outcropping along your" \
                                  "path. Strewn across the rocks are glass shards" \
                                  "and broken bottles. You start to go around the" \
                                  "rocky outcropping in hopes of avoiding cutting" \
                                  "yourself on any glass, when something catches" \
                                  "your eye and you stop. There, lying among the" \
                                  "rocky terrain and littered remains of what" \
                                  "looked to be a small distillery, is one lone" \
                                  "intact bottle of rum. You slowly pick your way" \
                                  "through the minefield of broken glass and pluck it up."

                self.missing_text = "Your journey through this strange room brings" \
                                    "you to a rocky outcropping that is strewn" \
                                    "with glass shards and broken bottles. As you" \
                                    "make your way around this minefield of broken" \
                                    "glass, you notice in the middle of it, a" \
                                    "strange spot of bare earth that nearly" \
                                    "resembles a bottle. You make a mental note" \
                                    "of this discrepancy and continue on your way."

            else:
                self.findItem = findItem.TwentyChuckECheeseTokens()
                self.found_text = "Following the path forward into the room a bit" \
                                  "more, you find yourself looking up at a rather" \
                                  "large tree. How a tree of this size and magnitude" \
                                  "could grow in a room this average sized confounds" \
                                  "you, but so do so many other things you have" \
                                  "seen on your journey here. As you begin to return" \
                                  "to the path, something red catches your eye" \
                                  "up in a hole in the trunk of the tree." \
                                  "Standing up on your tiptoes and reaching as" \
                                  "high as you can, you are just barely able to" \
                                  "grasp a tightly wrapped bundle of cloth that" \
                                  "has been jammed up in a hole in the tree trunk." \
                                  "Gently, you bring the bundle down and begin to" \
                                  "unwrap it, and as you do you are shocked to" \
                                  "find twenty Chuck E Cheese Tokens glimmering" \
                                  "in the dimly-lit room."

                self.missing_text = "Your journey down the path brings you to a" \
                                    "rather large tree. You wonder at the size of" \
                                    "the tree and how it could possibly continue" \
                                    "to grow in such an average sized room. As" \
                                    "you turn back to the path you notice at the" \
                                    "foot of the tree a red scrap of cloth tied" \
                                    "with a length of rope that looks to have held" \
                                    "something at one time. Whatever it held you" \
                                    "will never know, as there is a large cut in" \
                                    "the fabric from what you assume is the blade" \
                                    "of a knife."
    super().__init__(x, y)                                
   
   def intro_text(self):
       text = self.found_text if self.findItem.is_found() else self.missing_text
       return text
   
   def modify_player(self, player):
        if self.findItem.is_found():
            player.credit = player.credit + self.findItem.value
            print("You found an item. The item you found has {} much credit value.".
                  format(self.findItem.value, player.credit))
   
class NextLevel(MapTile):
    """
    When the player lands on a |NL| Tile, this functionality will pull the map configuration
    "next_level" parameters, load the next level into memory, then reset player actions.
    This is also passed back into the Play_Game function in game.py.

    - Chadwick
    """
    def __init__(self, x, y):
        super().__init__(x, y)

    def modify_player(self, player):
        player.world.Load_Map("level" + player.world.map_information['next_level'])

        player.x = player.world.start_tile_location[0]
        player.y = player.world.start_tile_location[1]

        MapTile.intro_text = player.world.map_information['intro']
        MapTile.level_name = player.world.map_information['name']

    def intro_text(self):
        text = """
            You feel a small shock. Everything flashes white. Your eyes adjust; you have been teleported to %s
            """ % MapTile.level_name
        return text

class World:
    """
    The World class handles map processing;
    * Scanning Map Directory
    * Loading Maps
    * Providing map configuration settings
    * Map validation
    * Tile Location
    """
    def __init__(self):
        self.maps_directory = os.getcwd() + "/maps/"
        self.available_maps = dict()
        self.current_map = []
        self.map_information = None
        self.map_format = None
        self.start_tile_location = None

    def Scan_Maps(self):
        """
        Scan map directory for .map files, load into a dictionary, key = maps_name (i.e: level1)
        - Chadwick
        """

        maps = glob.glob(self.maps_directory + "*.map")   # Scan /maps/ directory and collect all .map files
        map_names = [os.path.basename(scanned).strip(".map") for scanned in glob.glob(self.maps_directory + "*.map")]  # put into a list
        self.available_maps = dict(zip(map_names, maps))  #  combine two lists to create a dictionary, maps name is the key (i.e: level1)


    tile_types = {
        "EG": EndGameTile,
        "EN": EnemyTile,
        "ST": StartTile,
        "FI": FindItem,
        "FG": FindGoldTile,
        "NL": NextLevel,
        "  ": None,
    }

    def Load_Map(self, map_name):
        """
        Loads given map name into self.current_map
        Original Philip Johnson, modifications by Chadwick.
        """

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
        """
        Verifies:
        * Map Integrity
        * Next Level / End Game is properly implemented.

        - Original by Philip Johnson, modifications by Chadwick.
        """

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

    def tile_at(self, x, y):
        """
        Provides specific tile object by x and y coordinates
        - Philip Johnson
        """
        if x < 0 or y < 0:
            return None

        try:

            return self.current_map[y][x]
        except IndexError:
            return None


