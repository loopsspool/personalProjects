import os

PARENT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Actual save paths
GAME_SPRITE_SAVE_PATH = os.path.join(PARENT_DIR, "Images\\Pokemon\\Game Sprites\\")
DRAWN_SAVE_PATH = os.path.join(PARENT_DIR, "Images\\Pokemon\\Drawn\\")
HOME_SAVE_PATH = os.path.join(PARENT_DIR, "Images\\Pokemon\\HOME Sprites\\")
HOME_MENU_SAVE_PATH = os.path.join(PARENT_DIR, "Images\\Pokemon\\Menu Sprites\\HOME\\")
POKEBALL_SAVE_PATH = os.path.join(PARENT_DIR, "Images\\Pokeballs\\")
# Staging/testing paths
ANIMATED_PNGS_PRE_GIF_CONVERSION_PATH = os.path.join(PARENT_DIR, "Images\\Pokemon\\Game Sprites\\animated_pngs_for_gifs\\pngs\\Converted to gif\\")
GIFS_POST_CONVERSION_PATH = os.path.join(PARENT_DIR, "Images\\Pokemon\\Game Sprites\\animated_pngs_for_gifs\\gifs\\")
TEST_PATH = os.path.join(PARENT_DIR, "Images\\Pokemon\\Test\\")
STAGING_PATH = os.path.join(PARENT_DIR, "Images\\Pokemon\\Game Sprites\\staging\\")