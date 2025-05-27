import os

#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[     GENERAL UTILITY     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

def get_file_ext(file):
    return f".{file.split(".")[-1]}"


def replace_e(str):
    return str.replace("e", "\u00e9")




#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[     FILEPATHS     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

PARENT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Database
DB_NAME = "pokedex.db"
DB_PATH = os.path.join(PARENT_DIR, DB_NAME)


SAVE_PATHS = {
    # Actual save paths
    "GAME_SPRITE" : os.path.join(PARENT_DIR, "Images\\Pokemon\\Game Sprites\\"),
    "HOME" : os.path.join(PARENT_DIR, "Images\\Pokemon\\HOME Sprites\\"),
    "HOME_MENU" : os.path.join(PARENT_DIR, "Images\\Pokemon\\Menu Sprites\\HOME\\"),
    "DRAWN" : os.path.join(PARENT_DIR, "Images\\Pokemon\\Drawn\\"),
    "POKEBALL" : os.path.join(PARENT_DIR, "Images\\Pokeballs\\"),
    # Staging/testing paths
    "GIF" : os.path.join(PARENT_DIR, "Images\\Pokemon\\Game Sprites\\gif\\"),
    "WEBM" : os.path.join(PARENT_DIR, "Images\\Pokemon\\Game Sprites\\webm\\"),
    "NEED_TRANSPARENCY" : os.path.join(PARENT_DIR, "Images\\Pokemon\\Game Sprites\\need_transparency\\"),    # Used for saving stills from webm
    "TEST" : os.path.join(PARENT_DIR, "Images\\Pokemon\\Test\\"),
    "STAGING" : os.path.join(PARENT_DIR, "Images\\Pokemon\\Game Sprites\\staging\\")
}




#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~[     SETS OF SAVED IMG FILENAMES     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|


# Staging/testing paths
ALL_SAVED_GIFS = set(os.listdir(SAVE_PATHS["GIF"]))
ALL_SAVED_WEBMS = set(os.listdir(SAVE_PATHS["WEBM"]))
ALL_SAVED_NEED_TRANSPARENCY_IMGS = set(os.listdir(SAVE_PATHS["NEED_TRANSPARENCY"]))
ALL_SAVED_TEST_IMGS = set(os.listdir(SAVE_PATHS["TEST_PATH"]))
ALL_SAVED_STAGING_IMGS = set(os.listdir(SAVE_PATHS["STAGING_PATH"]))
# Actual save paths
ALL_SAVED_GAME_SPRITES = set(os.listdir(SAVE_PATHS["GAME_SPRITE"]))
ALL_SAVED_GAME_SPRITES = ALL_SAVED_GAME_SPRITES | ALL_SAVED_NEED_TRANSPARENCY_IMGS   # This unions the two so db recognizes file existence and I don't download need transparency images every time I start a new scrape session. # TODO: Can remove once transparency issue resolved
ALL_SAVED_HOME_SPRITES = set(os.listdir(SAVE_PATHS["HOME"]))
ALL_SAVED_HOME_MENU_IMAGES = set(os.listdir(SAVE_PATHS["HOME_MENU"]))
ALL_SAVED_DRAWN_IMAGES = set(os.listdir(SAVE_PATHS["DRAWN"]))
ALL_SAVED_POKEBALL_IMAGES = set(os.listdir(SAVE_PATHS["POKEBALL"]))