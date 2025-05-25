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

# Actual save paths
GAME_SPRITE_SAVE_PATH = os.path.join(PARENT_DIR, "Images\\Pokemon\\Game Sprites\\")
DRAWN_SAVE_PATH = os.path.join(PARENT_DIR, "Images\\Pokemon\\Drawn\\")
HOME_SAVE_PATH = os.path.join(PARENT_DIR, "Images\\Pokemon\\HOME Sprites\\")
HOME_MENU_SAVE_PATH = os.path.join(PARENT_DIR, "Images\\Pokemon\\Menu Sprites\\HOME\\")
POKEBALL_SAVE_PATH = os.path.join(PARENT_DIR, "Images\\Pokeballs\\")
# Staging/testing paths
GIF_SAVE_PATH = os.path.join(PARENT_DIR, "Images\\Pokemon\\Game Sprites\\gif\\")
WEBM_SAVE_PATH = os.path.join(PARENT_DIR, "Images\\Pokemon\\Game Sprites\\webm\\")
TEST_PATH = os.path.join(PARENT_DIR, "Images\\Pokemon\\Test\\")
STAGING_PATH = os.path.join(PARENT_DIR, "Images\\Pokemon\\Game Sprites\\staging\\")




#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~[     SETS OF SAVED IMG FILENAMES     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

ALL_SAVED_GAME_SPRITES = set(os.listdir(GAME_SPRITE_SAVE_PATH))
ALL_SAVED_HOME_SPRITES = set(os.listdir(HOME_SAVE_PATH))
ALL_SAVED_HOME_MENU_IMAGES = set(os.listdir(HOME_MENU_SAVE_PATH))
ALL_SAVED_DRAWN_IMAGES = set(os.listdir(DRAWN_SAVE_PATH))
ALL_SAVED_POKEBALL_IMAGES = set(os.listdir(POKEBALL_SAVE_PATH))