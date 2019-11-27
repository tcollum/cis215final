class Weapon:
    def __init__(self):
        raise NotImplementedError("Do not create raw Weapon objects.")

    def __str__(self):
        return self.name


class Rock(Weapon):
    def __init__(self):
        self.name = "Rock"
        self.description = "A fist-sized rock, suitable for bludgeoning."
        self.damage = 5
        self.value = 1


class Dagger(Weapon):
    def __init__(self):
        self.name = "Dagger"
        self.description = "A small dagger with some rust. " \
                           "Somewhat more dangerous than a rock."
        self.damage = 10
        self.value = 20


class RustySword(Weapon):
    def __init__(self):
        self.name = "Rusty sword"
        self.description = "This sword is showing its age, " \
                           "but still has some fight in it."
        self.damage = 20
        self.value = 100


class Ingestable:
    """Ingestable class will raise a NotImplementedError if Ingestable has not
       been previously created.

       Ingestable class will return both the name of the Ingestable and the
       healing value of the Ingestable.

       All instances of the Ingestable class have a value which is used when
       being purchased from the HiLineVendingMachine or the AlienTrader.

       All instances of the Ingestable class can be used to trade with the
       AlienTrader."""
    
    def __init__(self):
        raise NotImplementedError("Do not create raw ingestable objects.")

    def __str__(self):
        return "{} (+{} HP)".format(self.name, self.healing_value)

class DayOldFrenchBaguette(Ingestable):
    def __init_(self):
        self.name = "Day Old French Baguette"
        self.healing_value = 8
        self.value = 14

class RumAndCoke(Ingestable):
    def __init__(self):
        self.name = "Rum and Coke"
        self.healing_value = 25
        self.value = 30

class FourPackOfRedBull(Ingestable):
    def __init__(self):
        self.name = "Four Pack of Red Bull"
        self.healing_value = 35
        self.value = 40

class BottleOfAspirin(Ingestable):
    def __init__(self):
        self.name = "Bottle of Aspirin"
        self.healing_value = 65
        self.value = 75

