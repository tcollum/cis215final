import items

class SupportingCharacter():
    """SupportingCharacter class will raise a NotImplementedError if the
       SupportingCharacter has not been previously created.

       SupportingCharacter class returns the name of the SupportingCharacter.

       SupportingCharacter class will be called on two separate tiles: the
       Vending Machine Tile and the Trader Tile. Currently, there are two instances
       of this class: AlienTrader and HiLineVendingMachine.

       The AlienTrader only accepts and returns Monopoly Money as payment, however
       the AlienTrader does make trades with the player if the player has
       something the AlienTrader wants for their inventory. While the AlienTrader
       only accepts Monopoly Money as payment, it is stored as the variable
       creditTotal in the AlienTrader class. The variable creditTotal will increase
       and the AlienTrader's inventory will decrease as the game continues.

       The HiLineVendingMachine accepts Monopoly Money, Chuck E CHeese Tokens, or
       Visa Gift Cards as payments for purchases of an item in the vending machine's
       inventory. The HiLineVendingMachine does not make trades for the items
       in its inventory. While the HiLineVendingMachine accepts Monopoly Money,
       Chuck E Cheese Tokens, and Visa Gift Cards as payment, all three are stored
       as the variable creditTotal in the HiLineVendingMachine class. The variable
       creditTotal will increase and the HiLineVendingMachine's inventory will decrease
       as the game continues."""
       
    def __init__(self):
        raise NotImplementedError("Do not create raw NPC objects.")

    def __str__(self):
        return self.name


class AlienTrader(SupportingCharacter):
    def __init__(self):
        self.name = "Alien Trader"
        self.CreditTotal = 250 #create formula to reflect player trading for items in inventory (giving trader monopoly money)
        self.inventory = [items.DayOldFrenchBaguette(), #create formula to reflect player trading for items in inventory(taking items from trader's inventory)
                          items.DayOldFrenchBaguette(),
                          items.RumAndCoke(),
                          items.FourPackOfRedBull()]


class HiLineVendingMachine(SupportingCharacter):
    def __init__(self):
        self.name = "HiLine Vending Machine"
         #total used for Monopoly Money (create formula for Monopoly Money inserted into vending machine)
         #total used for Chuck E Cheese tokens (create formula for Chuck E Cheese tokens inserted into vending machine)
        self.CreditTotal = 740 #total used for Visa Gift Card (create formula for Visa Gift card that subtracts the amount for each consumable purchased from the vending machine)
        self.inventory = [items.DayOldFrenchBaguette(),     #create formula to reflect inventory being depleted  -- how do we keep track throughout the game?
                          items.DayOldFrenchBaguette(),
                          items.DayOldFrenchBaguette(),
                          items.DayOldFrenchBaguette(),
                          items.RumAndCoke(),
                          items.RumAndCoke(),
                          items.RumAndCoke(),
                          items.FourPackOfRedBull(),
                          items.FourPackOfRedBull()
                          items.FourPackOfRedBull(),
                          items.BottleOfAspirin(),
                          items.BottleOfAspirin()]
