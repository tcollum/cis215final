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
import pickle

import classes.enemies as enemies
import classes.boss as boss
import classes.reward as reward
import classes.npc as npc
import classes.items as items


class MapTile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.name = "Player"
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

    @property
    def player_name(self):
        return self.name

    @player_name.setter
    def player_name(self, player):
        self.name = player.name

class StartTile(MapTile):
    def intro_text(self):
        return MapTile.intro_text

    def modify_player(self, player):
        MapTile.level_name = player.world.map_information['name']
        MapTile.intro_text = player.world.map_information['intro']


class EnemyTile(MapTile):
    """ Enemies that you will encounter throughout the game
    - Nick
    """
    def __init__(self, x, y):
        r = random.random()
        if r < 0.20:
            self.enemy = enemies.Parasite()
            self.alive_text = """
                A parasitic lifeform rushes toward you!
            """

            self.dead_text = """
                The corpse of a Parasite lies motionless on the ground.
                It looks rather crab-like and might be tasty if boiled and
                served with some garlic butter, but
                there's time to think about food later. Onward!
                """
        elif r < 0.60:
            self.enemy = enemies.ParasiteZ()
            self.alive_text = """
                A Parasite... no, a Parasite Zombie emerges from the darkness!
                """

            self.dead_text = """
                The Parasite has lost its grip, and
                the form underneath is revealed to be
                human. It seems like others have crash
                landed here. They were either ambushed
                or voluntarily coupled with it in a
                desperate attempt to stay warm. Some fool probably
                even found a sleeping one and put
                it on like a fancy hat.
                """

        elif r < 0.70:
            self.enemy = enemies.GhostMonkey()
            self.alive_text = """
                An unerving feeling shivers down your spine.
                A Chimpanzee's Shadow materializes
                """

            self.dead_text = """
                The Shadow disappeared from this spot,
                although a faint scent of bananas permeates the area.
                There's a small, abondoned space suit,
                decades old, covered in moss nearby.
                """
        elif r < 0.95:
            self.enemy = enemies.Slime()
            self.alive_text = """
                You hear a slurping, goopy noise ahead.
                ...suddenly you ambushed by a Slimy Blob!
                """

            self.dead_text = """
                Chunks of translucent, slimy parts are scattered
                about the area. There is a strawberry aroma
                exuding from the chunks. But you shouldn't risk
                eating something that could be poisonous... right?
                """
        else:
            self.enemy = enemies.SJGolem()
            self.alive_text = """
                A Slimy Blob attaches itself to chunks of abandoned machinery and spacecraft!
                A Space Junk Golem forms!
                """

            self.dead_text = """
                The unknown slimy substance has dissapated,
                and the once monstrous form has reverted to space junk.
                All of the equipment that merged with the
                Blob has become sticky and unusable, like spilling soda on
                an ancient desktop computer. Today's just not your day.
                """

        super().__init__(x, y)

    def intro_text(self):
        text = self.alive_text if self.enemy.is_alive() else self.dead_text
        return text

    def modify_player(self, player):
        if self.enemy.is_alive():
            player.hp = player.hp - self.enemy.damage
            print("Enemy does {} damage. You have {} HP remaining.".
                  format(self.enemy.damage, player.hp))


class BossTile(MapTile):
    """ Handles encountering a boss enemy
    - Nick
    """
    ##edited version of enemytile class, but guaranteed encounter with 1 boss- Nick
    def __init__(self, x, y):
        r = random.random()
        if 0 < r < 1:
            self.boss = boss.TrashMan()
            self.alive_text = """
            Suddenly, the signal rushes toward you! Out of nowhere,
            a mass of malicious, murderous machinery
            (say that 3 times fast!)crashes into your path.
            Hey! It's gripping the transmitter from your ship!
            And it seems very interested in your undelivered packages.
            """

            self.dead_text = """
                The scrambled remains of the hulking garbage disposal
                lays before you. What caused it to make your ship crash?
                Why was it so insistant on leaving you stranded?
                Why did it want your mail?
                Do robots even get mail?
                """
        super().__init__(x, y)

    def intro_text(self):
        text = self.alive_text if self.boss.is_alive() else self.dead_text
        return text

    def modify_player(self, player):
        if self.boss.is_alive():
            player.hp = player.hp - self.boss.damage
            print("Boss does {} damage. You have {} HP remaining.".
                  format(self.boss.damage, player.hp))

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
        You finally find the source of the electronic signal: a single working outlet
        that a broken toaster has been plugged into. You unplug it and witness a miracle: 2 burnt halves
        of a bagel preserved in ice pop out! 
        You plug in your transmitter and send out a distress signal, with a nagging feeling in the back
        of your mind that something still doesn't seem right. Wanting to kill some time, you sort through your mail
        to get it ready before you're picked up. You notice one package that didn't catch your eye before now:
        a small, rectangular box with gold wrapping with way too many "Urgent!" labels on it.
        You don't remember seeing it at all before. You decide to leave it alone for now,
        relieved that you'll finally get out of here.
        Congratulations for beating the game! The End!
        """
    ##some epilogue text-Nick

class FindItem(MapTile):
    def __init__(self, x, y):
        """Creates a tile that enables the player to find an item
           (thingsToEat, reward, weapon, etc.) based on a random number generator."""
        self.is_found = False
        r = random.random()

        if r < 0.20:
            self.findItem = items.TwoBottlesOfAspirin()
            self.found_text = """After clearing the cobwebs off a dark and dank corner 
                               of the room, you notice two bottles lying on the ground. 
                               You pick them up and wipe the sludge from the front of them 
                               so you can read their labels. Much to your surprise and sheer
                               delight you find yourself with teo bottles of aspirin in hand."""

            self.missing_text = """One corner of the room you notice the ground is remarkably free
                                cobweb-free compared to the rest of the room. Two clear round
                                impressions have been left in the sludge on the ground as if something
                                or perhaps some things had once been there."""

        elif r < 0.45:
            self.findItem = items.SixCasesOfRedBull()
            self.found_text = """You make your way further into the dark room
                                  and nearly trip over something in your path.
                                  You look down to see what has caused you to
                                  stumble and nearly do a happy dance. There at
                                  your feet, lay six cases of Red Bull energy
                                  drink. Now there's something that will come
                                  in handy after a long day of doing battle
                                  with your enemies you think to yourself as you
                                  start to make room in your pack for them."""

            self.missing_text = """As you make your way further into the dark
                                    room, you come to a clearing in the road,
                                    which you find odd. There seems to have been
                                    something stored in the middle of the road
                                    at one point. The outline in the dust on the
                                    road reflects it to be sure. Shrugging, you
                                    make your way on down the road."""

        elif r < 0.70:
            self.findItem = items.BottleOfRum()
            self.found_text = """
                You come across a rocky outcropping along your
                path. Strewn across the rocks are glass shards
                and broken bottles. You start to go around the
                rocky outcropping in hopes of avoiding cutting
                yourself on any glass, when something catches
                your eye and you stop. There, lying among the
                rocky terrain and littered remains of what
                looked to be a small distillery, is one lone
                intact bottle of rum. You slowly pick your way
                through the minefield of broken glass and pluck it up.
                """

            self.missing_text = """
                Your journey through this strange room brings
                you to a rocky outcropping that is strewn
                with glass shards and broken bottles. As you
                make your way around this minefield of broken
                glass, you notice in the middle of it, a
                strange spot of bare earth that nearly
                resembles a bottle. You make a mental note
                of this discrepancy and continue on your way.
            """

        else:
            self.findItem = items.TwentyChuckECheeseTokens()
            self.found_text = """
                Following the path forward into the room a bit
                more, you find yourself looking up at a rather
                large tree. How a tree of this size and magnitude
                could grow in a room this average sized confounds
                you, but so do so many other things you have
                seen on your journey here. As you begin to return
                to the path, something red catches your eye
                up in a hole in the trunk of the tree.
                Standing up on your tiptoes and reaching as
                high as you can, you are just barely able to
                grasp a tightly wrapped bundle of cloth that
                has been jammed up in a hole in the tree trunk.
                Gently, you bring the bundle down and begin to
                unwrap it, and as you do you are shocked to
                find twenty Chuck E Cheese Tokens glimmering
                in the dimly-lit room.
                """

            self.missing_text = """
            Your journey down the path brings you to a
            rather large tree. You wonder at the size of
            the tree and how it could possibly continue
            to grow in such an average sized room. As
            you turn back to the path you notice at the
            foot of the tree a red scrap of cloth tied
            with a length of rope that looks to have held
            something at one time. Whatever it held you
            will never know, as there is a large cut in
            the fabric from what you assume is the blade
            of a knife.
            """
        super().__init__(x, y)


    def intro_text(self):
        text = self.found_text if self.is_found else self.missing_text
        return text


    def modify_player(self, player):
        if not self.is_found:
            self.is_found = True
            player.credit = player.credit + self.findItem.value
            print("You found an item. The item you found has {} much credit value.".
                  format(self.findItem.value, player.credit))


class AlienTraderTile(MapTile):
    def _init_(self, x, y):
        self.alienTrader = npc.AlienTrader()
        self.item_bought = False
        super().__init__(x, y)

    def willing_to_trade(self, player):
        while True:
            print("""
            Come see what I have for sell. Let's make a deal. All
            purchases must be made using Monopoly Money. Enter P to
            purchase something you like, T to trade me something I
            might like, or R to return to the previous room.
            """)
            player_response = input()
            if player_response in ['R', 'r']:
                return
            elif player_response in ['P', 'p']:
                print("Here's the list of what I'm selling: ")
                self.make_the_trade(buyer=player, seller=self.alienTrader)
            elif player_response in ['T', 't']:
                print("Here's the list of what I'm willing to trade for: ")
                self.make_the_trade(buyer=self.alienTrader, seller=player)
            else:
                print("Wrong choice bucko!!")

    def make_the_trade(self, buyer, seller):
        for i, item in enumerate(seller.inventory, 1):
            print("{}. {] - {} Credit Total".format(i, item.name, item.value))
            while True:
                player_response = input("Choose an item or press R to return to previous room: ")
                if player_response in ['R', 'r']:
                    return
                else:
                    try:
                        player_choice = int(player_response)
                        make_the_swap = seller.inventory[player_choice - 1]
                        self.make_the_swap(seller, buyer, make_the_swap)
                    except ValueError:
                        print("Wrong choice bucko!!")

    def make_the_swap(self, seller, buyer, item):
        if item.value > buyer.monopoly_money:
            print("I don't have enough money.")
            return
        else:
            seller.inventory.remove(item)
            buyer.inventory.append(item)
            seller.monopoly_money = seller.monopoly_money + item.value
            buyer.monopoly_money = buyer.monopoly_money - item.value
            print("Thanks for trading with me! Come back soon!")
            buyer.CreditTotal = buyer.monopoly_money

    def alien_trader_tile_intro_text(self):
        return """
            A slithering, hunchbacked creature with a single eye in the middle
            of his forehead pushes a cart with supplies you recognize as items
            you might find back on your home planet. As you gather the courage
            to approach him, his eye tracks your every move. You see a sign on
            his cart announcing that he only sells his wares for top dollar,
            there is no haggling, and his currency is Monopoly Money. You stifle
            a laugh as you consider the absurd conditions you find yourself in.
            He does, after all, have items you are in desperate need of..."""

    def alien_trader_tile_modify_player(self, player):
        if not self.item_bought:
            self.item_bought = True
            player.CreditTotal = player.CreditTotal - self.item.value
            print("You have purchased an item. The item you purchased has {} much credit value."
                  "You now have {} in total credit.".format(self.item.value, player.CreditTotal))


class HiLineVendingMachineTile(MapTile):
 
    """Class that makes the HiLineVendingMachineTile.

       Includes functions that enable the HiLineVendingMachine to make a
       sales pitch to the player and sell items to the player.

       -Treasure"""

    def __init__(self, x, y):
        self.hi_line_vending_machine = npc.HiLineVendingMachine()
        self.item_bought = False
        super().__init__(x, y)

    def the_pitch(self, player):
        while True:
            print("""
                    Four packs of Red Bull for sale! Day Old French Baguettes
                    for sale! Rum and Cokes for sale! Aspirin for sale!
                    Monopoly Money, Chuck E Cheese Tokens, and Visa Gift Cards
                    accepted as payment. Enter P to purchase something you like,
                    or enter R to return to the previous room.
                    """)
            player_response = input()
            if player_response in ['R', 'r']:
                return
            elif player_response in ['P', 'p']:
                print("Here's the list of what I'm selling: ")
                self.the_sale(buyer=player, seller=self.hi_line_vending_machine)
            else:
                print("Incorrect choice entered.")

    def the_sale(self, buyer, seller):
        buyer.CreditTotal = buyer.monopoly_money
        buyer.CreditTotal = buyer.chuck_e_cheese_token
        buyer.CreditTotal = buyer.visa_gift_card

        for i, item in enumerate(seller.inventory, 1):
            print("{}. {] - {} CreditTotal".format(i, item.name, item.value))
            while True:
                player_response = input("Choose an item or press Q to exit: ")
                if player_response in ['R', 'r']:
                    return
                else:
                    try:
                        player_choice = int(player_response)
                        make_the_sale = seller.inventory[player_choice - 1]
                        self.make_the_sale(seller, buyer, make_the_sale)
                    except ValueError:
                        print("Incorrect choice entered.")

    def make_the_sale(self, seller, buyer, item):
        if item.value > buyer.CreditTotal:
            print("I don't have enough money.")
            return
        else:
            seller.inventory.remove(item)
            buyer.inventory.append(item)
            seller.CreditTotal = seller.CreditTotal + item.value
            buyer.CreditTotal = buyer.CreditTotal - item.value
            print("Thanks for using HiLine Vending. Have a nice day.")

    def intro_text(self):
        return """
        As you walk along the desolate road, you are drawn to light that
        beckons you. Thinking you must be hallucinating or seeing something
        like an oasis in a desert, you carefully approach the thing that is
        casting off so much light in an otherwise dimly lit atmosphere. You
        are surprised to come face to face with a HiLine Vending Machine,
        something you know all to well from your days in elementary and high
        school days. This vending machine isn't filled with the usual
        merchandise like candy bars and Gatorades. It offers you four items
        in multiple amounts. In its computerized voice, the machine asks
        you to make your selection, telling you it accepts any method of
        payment you might have. After the battles you just faced, this machine
        may just be your lifeline...
        """

    def hi_line_vending_machine_tile_modify_player(self, player):
        if not self.item_bought:
            self.item_bought = True
            player.CreditTotal = player.CreditTotal - self.item.value
            print("You purchased an item. The item you purchased has {} much credit value."
                  "You now have {} in total credit.".format(self.item.value, player.CreditTotal))



 class SpecialRoomTile(MapTile):
     def __init__(self, x, y):
         """Creates rewards for the player that are chosen based on the random
            number generator function once the player enters the special room.
            Built into the function are found/missing text statements that will
            populate if the reward has already been claimed if the player has
            visited the room.
            
           -Treasure"""

         r = random.random()
         if r < 0.60:
             self.reward = reward.ChuckECheeseToken()
             self.found_text = """
                 You found a chest of Chuck E. Cheese Tokens.
                 You can use these to buy much needed supplies!
                 """

             self.missing_text = """
                 An empty chest indicates someone beat you
                 this room."""

         elif r < 0.75:
             self.reward = reward.MonopolyMoney()
             self.found_text = """
                 You find a Monopoly game set overflowing with
                 Monopoly money, a Monopoly game board, and a
                 few game pieces. Congrats on your lucky find!
                 Use this Monopoly Money to buy supplies from
                 the vending machine.
                               """

             self.missing_text = """
                 You find a Monopoly game set containing a
                 Monopoly game board and a few game pieces
                 but all of the Monopoly money has been taken.
                 Better luck next time."""

         elif r < 0.85:
             self.reward = reward.VisaGiftCard()
             self.found_text = """
                 Lucky you, you stumbled across a wallet
                 containing a visa gift card. Use this visa
                 gift card to stock up on supplies at your
                 neighborhood vending machine.
                 """

             self.missing_text = """
                 You discover a wallet with a driver's
                 license, a photo of happy family, a Sam's
                 club membership card, and a Blockbuster
                 Video rental card. One slot in the wallet
                 is missing a rather valuable card.
                 """
         else:
             self.reward = reward.TwentyCasesOfRedBull()
             self.found_text = """
                 Upon clearing the cobwebs off a very dirty
                 set of bookshelves you discover, much to your
                 delight, twenty cases of Red Bull. Use these
                 to restore your strength between battles with
                 enemies.
                 """

             self.missing_text = """
                 Nearing a set of bookshelves that look
                 conspicously clean compared to the rest of
                 the room, you find a few empty cans of Red
                 Bull and the outline of what appears to
                 have been a stockpile of the delicious
                 drink. Sadly, it looks like someone beat
                 you to whatever was stockpiled there.
                 """

   def intro_text(self):
       text = self.found_text if self.reward.is_found() else self.missing_text
       return text

   def assigningRewardValues(self, player):
       if self.reward.is_found():
           if self.reward == monopoly_money:
               self.reward.value += monopoly_money
           elif self.reward == chuck_e_cheese_toker:
               self.reward.value += chuck_e_cheese_token
           elif self.reward == visa_gift_card:
               self.reward.value += visa_gift_card
           elif self.reward == twenty_case_red_bull:
               self.reward.value += twenty_cases_red_bull
           else:
               pass
       return self.reward.value

   def modify_player(self, player):
       if not self.reward.is_found:
           self.reward.is_found = True
           player.CreditTotal = player.CreditTotal + self.reward.value
           print("Congratulations! You have found a reward worth {} in credit."
                 "You now have {} in credit.".format(self.reward.value, player.CreditTotal))
           return player.CreditTotal


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

class SaveGameTile(MapTile):
    """
    When a player lands on the "SG" tile, the game will prompt to save.
    - Chadwick
    """
    def __init__(self, x, y):
        super().__init__(x, y)

    def intro_text(self):
        return """ 
            Insert save game text here
        """

    def modify_player(self, player):
        # 0 = Player name, 1 = map configuration information, 2 = current map / level, 3 = player coordinates, 4 = player inventory
        save_data = (self.name, player.world.map_information, player.world.current_map, (str(player.x) + ',' + str(player.y)), player.inventory)
        if os.path.isfile('gamesave.txt'):
            ask_question = input('A previous game save exists! Would you like to overwrite? [y/n] : ').lower()
            if ask_question == 'y':
                self.save_file(save_data)
            else:
                print("Game has not been saved...")
        else:
            self.save_file(save_data)

    def save_file(self, save_data):
        save_game = open('gamesave.txt', 'wb')
        pickle.dump(save_data, save_game)
        print("Game has been saved!")
        save_game.close()


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
        "BT": BossTile,
        "EG": EndGameTile,
        "EN": EnemyTile,
        "ST": StartTile,
        "FI": FindItem,
        "NL": NextLevel,
        "SG": SaveGameTile,
        "VM": HiLineVendingMachineTile,
        #"SR": SpecialRoomTile,
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


