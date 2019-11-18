"""
Project: Text Based Game - Final Project
Class: CIS 215
Institution: Coconino Community College
                -> Fall Semester, 2019.

Description: A python (3.7), text based game. Final project
            for CIS 215. ** Extend Description **


"""

from classes.game import Game
current_game = Game()

def main():
    print("\t Welcome to ** INSERT GAME NAME **")
    print("-" * 45)

    while not current_game.game_active:  # While game is not active, display main menu
        Main_Question()
    else:
        current_game.Play_Game()
        # Do game actions here



def Main_Question():
    """ Initialize the main menu questions new / load / etc ..."""
    command = None
    while not command and not current_game.game_active:
        print("[0] -> New Game")
        print("[1] -> Load Game")
        print("[2] -> About")
        print("[3] -> Exit")


        command = main_menu_options[input("-> ")]
        if command:
            command()

    print("\n")


def NewGame():
    """ Start a new game """
    current_game.New_Game()



def LoadGame():
    print("Sorry, this functionality is not yet implemented... ")

def About():
    print("\t ABOUT PROJECT ")
    print("-" * 40)
    print("Class: CIS 215")
    print("Institution: Coconino Community College")
    print("Project: Final Project")
    print("Description:  A text based adventure game written in Python 3.7!")

def ExitGame():
    print("Goodbye...")
    exit()



main_menu_options = {
    "0": NewGame,
    "1": LoadGame,
    "2": About,
    "3": ExitGame
}

if __name__ == "__main__":
    main()
