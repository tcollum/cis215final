class Reward:
    """Reward class will raise a NotImplementedError if the instance of the
       Reward class has not been previously created.

       Reward class returns the name of the reward.

       All instances of Rewards created from the Rewards class are assigned a
       value. They are used in the SpecialRoomTile where the Rewards are found
       and the player earns the values assigned to those Rewards, as well as
       with the MarketTile, which is where the HiLineVendingMachine and the
       AlienTrader are located. This is where the player will spend the values
       they have earned either by buying a consumable or by trading for it.

       Written by Treasure Collum
       11/22/19"""
    def __init__(self):
        raise NotImplementedError("Do not create raw Reward objects.")

    def __str__(self):
        return self.name

class ChuckECHeeseToken(Reward):
    def __init__(self):
        self.name = "Chuck E Cheese Token"
        self.value = 1

class MonopolyMoney(Reward):
    def __init__(self):
        self.name = "Monopoly Money"
        self.value = 5

class VisaGiftCard(Reward):
    def __init__(self):
        self.name = "Visa Gift Card"
        self.value = 25

class TwentyCasesOfRedBull(Reward):
    def __init__(self):
        self.name = "Twenty Cases of Red Bull"
        self.value = 75
