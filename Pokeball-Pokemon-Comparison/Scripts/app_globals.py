import string # To access letters easily without having to type them myself in an array
from db_utils import get_last_poke_num, populate_db

# TODO: Have all functions utilize the start and to go after start denoters
# TODO: This could be put in a text file, So I don't even have to write this after each crash. Each new pokemon would rewrite the line of the file where it picked up
# This is so when I get kicked from the server I only have to write once where to pick up
POKE_NUM_START_FROM = 1
POKE_TO_GO_AFTER_START = 10000
LAST_POKE_NUM = -1
try: LAST_POKE_NUM = get_last_poke_num()
except:
    populate_db()
    LAST_POKE_NUM = get_last_poke_num()

if POKE_NUM_START_FROM < 1: POKE_NUM_START_FROM=1
if POKE_NUM_START_FROM > LAST_POKE_NUM: POKE_NUM_START_FROM = LAST_POKE_NUM
if POKE_TO_GO_AFTER_START < 1: POKE_TO_GO_AFTER_START=0
if POKE_NUM_START_FROM + POKE_TO_GO_AFTER_START > LAST_POKE_NUM: POKE_TO_GO_AFTER_START = LAST_POKE_NUM - POKE_NUM_START_FROM
POKE_NUM_END_AT = POKE_NUM_START_FROM + POKE_TO_GO_AFTER_START

# TODO: Should the following 3 sections really be here?

# These are for back generation differences to be able to loop through and concatonate game name to filename
# TODO: Make this a dict?
# TODO: Where is this used?
# gen1_games = ["Yellow", "Red-Green", "Red-Blue"]
# gen2_games = ["Silver", "Gold", "Crystal"]
# gen3_games = ["Ruby-Sapphire", "FireRed-LeafGreen", "Emerald"]
# gen4_games = ["Platinum", "HGSS", "Diamond-Pearl"]
# gen_1_thru_4_games = [gen1_games, gen2_games, gen3_games, gen4_games]

# TODO: Put into JSON and adjust scrape_bulba_translators.bulba_doesn't_have_this_form() if needed
# NOTE: Double check occasionally
no_bulba_forms = []
# Pikachu World Cap
no_bulba_forms.append("-Form-Cap-World")
# Cosplay Pikachu
no_bulba_forms.append("-Form-Cosplay")
# Overdrive Reshiram, Zekrom, and Kyurem
no_bulba_forms.append("Overdrive")
# Marshadow Zenith
no_bulba_forms.append("-Form-Zenith")
# Urshifu Forms
no_bulba_forms.extend(["-Form-Rapid_Strike", "-Form-Single_Strike"])
# Dada Zarude
no_bulba_forms.append("-Form-Dada")
# Calyrex Riders
no_bulba_forms.extend(["-Form-Shadow_Rider", "-Form-Ice_Rider"])

uppers = list(string.ascii_uppercase)
poke_types = ["Normal", "Fighting", "Flying", "Poison", "Ground", "Rock", "Bug", "Ghost", "Steel", "Fire", "Water", "Grass", "Electric", "Psychic", "Ice", "Dragon", "Dark", "Fairy", "Qmark"]
# Vanilla Cream is default, so no letter denoter
creams = [("Caramel_Swirl", "CaS"), ("Lemon_Cream", "LeC"), ("Matcha_Cream", "MaC"), ("Mint_Cream", "MiC"), ("Rainbow_Swirl", "RaS"), ("Ruby_Cream", "RaC"), ("Ruby_Swirl", "RuS"), ("Salted_Cream", "SaC"), ("Vanilla_Cream", "")]
# Strawberry Sweet is default, so no letter denoter
sweets = [("Berry_Sweet", "B"), ("Clover_Sweet", "C"), ("Flower_Sweet", "F"), ("Love_Sweet", "L"), ("Ribbon_Sweet", "R"), ("Star_Sweet", "S"), ("Strawberry_Sweet", "")]


save_path_starter = "C:\\Users\\ethan\\OneDrive\\Desktop\\Code\\Pokeball-Pokemon-Comparison\\Images\\Pokemon"
game_save_path = save_path_starter + "\\Game Sprites\\"
gen6_menu_sprite_save_path = save_path_starter + "\\Menu Sprites\\Gen6\\"
gen8_menu_sprite_save_path = save_path_starter + "\\Menu Sprites\\Gen8\\"
drawn_save_path = save_path_starter + "\\Drawn\\"
# TODO: This didn't download gen1-3 female back sprites (Are they different?)
gen1_thru_4_backs_save_path = game_save_path + "\\back_imgs_to_be_filtered\\"
