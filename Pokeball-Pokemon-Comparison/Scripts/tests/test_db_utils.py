import sys
import os
import sqlite3
import pytest

# TODO: To replace cursor arguments, in db_utils could pull game/form ids into a dict or something, then search that instead of the db
# TODO: Add sprite exclusions

# To go into parent directory to import db_utils
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from db_utils import DB_PATH, FORM_EXCLUSIONS, SHARED_SHINY_FORMS, is_form_obtainable, is_sprite_possible, should_skip_nonexistant_sprite, get_poke_form_records, get_poke_form_obtainability_records, get_game_records, get_form_id, get_game_id, get_sprite_types

# Setting up connection to db
connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()
# Getting necessary info for testing
default_form_id = get_form_id("Default")
poke_forms = get_poke_form_records(cursor)
games = get_game_records(cursor)
pfgo = get_poke_form_obtainability_records(cursor)
sprite_types = get_sprite_types(cursor)


@pytest.mark.parametrize("poke_form_id, game_id, expected", [
    # Species game availability
    ((152, default_form_id), get_game_id("LGPE"), False),
    ((1, default_form_id), get_game_id("LGPE"), True),
    ((13, default_form_id), get_game_id("SwSh"), False),
    ((1, default_form_id), get_game_id("SwSh"), True),
    ((494, default_form_id), get_game_id("BDSP"), False),
    ((1, default_form_id), get_game_id("BDSP"), True),
    ((1, default_form_id), get_game_id("LA"), False),
    ((25, default_form_id), get_game_id("LA"), True),
    ((10, default_form_id), get_game_id("SV"), False),
    ((1, default_form_id), get_game_id("SV"), True),

    # Universal rules
    ((152, default_form_id), 1, False),
    ((1025, default_form_id), 20, True),
    ((3, get_form_id("-f")), get_game_id("FRLG"), False),
    ((3, get_form_id("-f")), get_game_id("Diamond_Pearl"), True),
    ((493, get_form_id("-Form_Fairy")), get_game_id("BW_B2W2"), False),
    ((493, get_form_id("-Form_Fairy")), get_game_id("XY_ORAS"), True),
    ((6, get_form_id("-Mega_X")), get_game_id("BW_B2W2"), False),
    ((6, get_form_id("-Mega_X")), get_game_id("XY_ORAS"), True),
    ((6, get_form_id("-Mega_X")), get_game_id("LGPE"), False),
    ((6, get_form_id("-Mega_X")), get_game_id("SwSh"), False),
    ((3, get_form_id("-Mega")), get_game_id("BW_B2W2"), False),
    ((3, get_form_id("-Mega")), get_game_id("XY_ORAS"), True),
    ((3, get_form_id("-Mega")), get_game_id("LGPE"), False),
    ((3, get_form_id("-Mega")), get_game_id("SwSh"), False),
    ((3, get_form_id("-Gigantamax")), get_game_id("LA"), False),
    ((3, get_form_id("-Gigantamax")), get_game_id("SwSh"), True),
    ((19, get_form_id("-Region_Alola")), get_game_id("XY_ORAS"), False),
    ((19, get_form_id("-Region_Alola")), get_game_id("SM_USUM"), True),
    ((52, get_form_id("-Region_Galar")), get_game_id("LGPE"), False),
    ((52, get_form_id("-Region_Alola")), get_game_id("LGPE"), True),
    ((19, get_form_id("-Region_Alola")), get_game_id("BDSP"), False),
    ((19, default_form_id), get_game_id("BDSP"), True),
    ((52, get_form_id("-Region_Galar")), get_game_id("BW_B2W2"), False),
    ((52, get_form_id("-Region_Galar")), get_game_id("SwSh"), True),
    ((59, get_form_id("-Region_Hisui")), get_game_id("SwSh"), False),
    ((59, get_form_id("-Region_Hisui")), get_game_id("SV"), True),
    ((52, get_form_id("-Region_Galar")), get_game_id("LA"), False),
    ((19, get_form_id("-Region_Alola")), get_game_id("LA"), False),
    ((59, get_form_id("-Region_Hisui")), get_game_id("LA"), True),
    ((37, get_form_id("-Region_Alola")), get_game_id("LA"), True),
    ((38, get_form_id("-Region_Alola")), get_game_id("LA"), True),
    ((128, get_form_id("-Region_Paldea-Form_Blaze")), get_game_id("SwSh"), False),
    ((128, get_form_id("-Region_Paldea-Form_Blaze")), get_game_id("SV"), True),

    # Specific Pokemon
    ((25, get_form_id("-Form_Cosplay_Belle")), get_game_id("BW_B2W2"), False),
    ((25, get_form_id("-Form_Cosplay_Libre")), get_game_id("SM_USUM"), False),
    ((25, get_form_id("-Form_Cosplay_PhD")), get_game_id("XY_ORAS"), True),
    ((25, get_form_id("-Form_Cap_Hoenn")), get_game_id("XY_ORAS"), False),
    ((25, get_form_id("-Form_Cap_Alola")), get_game_id("LA"), False),
    ((25, get_form_id("-Form_Cap_Alola")), get_game_id("SM_USUM"), True),
    ((25, get_form_id("-Form_Cap_Unova")), get_game_id("SV"), True),
    ((25, get_form_id("-Form_Cap_World")), get_game_id("SM_USUM"), False),
    ((25, get_form_id("-Form_Cap_World")), get_game_id("LGPE"), False),
    ((25, get_form_id("-Form_Cap_World")), get_game_id("BDSP"), False),
    ((25, get_form_id("-Form_Cap_World")), get_game_id("LA"), False),
    ((25, get_form_id("-Form_Cap_World")), get_game_id("SwSh"), True),
    ((25, get_form_id("-Form_Cap_World")), get_game_id("SV"), True),
    ((133, get_form_id("-f")), get_game_id("SM_USUM"), False),
    ((133, get_form_id("-f")), get_game_id("SwSh"), True),
    ((172, get_form_id("-Form_Spiky_Eared")), get_game_id("Emerald"), False),
    ((172, get_form_id("-Form_Spiky_Eared")), get_game_id("Diamond_Pearl"), False),
    ((172, get_form_id("-Form_Spiky_Eared")), get_game_id("HGSS"), True),
    ((201, get_form_id("-Form_!")), get_game_id("Gold"), False),
    ((201, get_form_id("-Form_Qmark")), get_game_id("Crystal"), False),
    ((201, get_form_id("-Form_!")), get_game_id("Ruby_Sapphire"), True),
    ((201, get_form_id("-Form_Qmark")), get_game_id("FRLG"), True),
    ((382, get_form_id("-Form_Primal")), get_game_id("BW_B2W2"), False),
    ((383, get_form_id("-Form_Primal")), get_game_id("SwSh"), False),
    ((382, get_form_id("-Form_Primal")), get_game_id("XY_ORAS"), True),
    ((383, get_form_id("-Form_Primal")), get_game_id("SM_USUM"), True),
    ((479, get_form_id("-Form_Heat")), get_game_id("Diamond_Pearl"), False),
    ((479, get_form_id("-Form_Heat")), get_game_id("HGSS"), True),
    ((479, get_form_id("-Form_Wash")), get_game_id("Platinum"), True),
    ((483, get_form_id("-Form_Origin")), get_game_id("BDSP"), False),
    ((484, get_form_id("-Form_Origin")), get_game_id("SwSh"), False),
    ((483, get_form_id("-Form_Origin")), get_game_id("LA"), True),
    ((484, get_form_id("-Form_Origin")), get_game_id("SV"), True),
    ((487, get_form_id("-Form_Origin")), get_game_id("Diamond_Pearl"), False),
    ((487, get_form_id("-Form_Origin")), get_game_id("Platinum"), True),
    ((487, get_form_id("-Form_Origin")), get_game_id("BW_B2W2"), True),
    ((386, default_form_id), get_game_id("Ruby_Sapphire"), True),
    ((386, get_form_id("-Form_Attack")), get_game_id("Ruby_Sapphire"), False),
    ((386, get_form_id("-Form_Defense")), get_game_id("Ruby_Sapphire"), False),
    ((386, get_form_id("-Form_Speed")), get_game_id("Ruby_Sapphire"), False),
    ((386, default_form_id), get_game_id("Emerald"), True),
    ((386, get_form_id("-Form_Attack")), get_game_id("Emerald"), False),
    ((386, get_form_id("-Form_Defense")), get_game_id("Emerald"), False),
    ((386, get_form_id("-Form_Speed")), get_game_id("Emerald"), True),
    ((386, default_form_id), get_game_id("FRLG"), True),
    ((386, get_form_id("-Form_Attack")), get_game_id("FRLG"), True),
    ((386, get_form_id("-Form_Defense")), get_game_id("FRLG"), True),
    ((386, get_form_id("-Form_Speed")), get_game_id("FRLG"), False),
    ((492, get_form_id("-Form_Sky")), get_game_id("Diamond_Pearl"), False),
    ((492, get_form_id("-Form_Sky")), get_game_id("Platinum"), True),
    ((492, get_form_id("-Form_Sky")), get_game_id("BW_B2W2"), True),
    ((493, get_form_id("-Form_Qmark")), get_game_id("BW_B2W2"), False),
    ((493, get_form_id("-Form_Qmark")), get_game_id("Diamond_Pearl"), True),
    ((550, get_form_id("-Form_White_Striped")), get_game_id("BW_B2W2"), False),
    ((550, get_form_id("-Form_White_Striped")), get_game_id("SwSh"), False),
    ((550, get_form_id("-Form_White_Striped")), get_game_id("LA"), True),
    ((550, get_form_id("-Form_White_Striped")), get_game_id("SV"), True),
    ((658, get_form_id("-Form_Ash")), get_game_id("XY_ORAS"), False),
    ((658, get_form_id("-Form_Ash")), get_game_id("SV"), False),
    ((658, get_form_id("-Form_Ash")), get_game_id("SM_USUM"), True),
    ((718, get_form_id("-Form_10%")), get_game_id("XY_ORAS"), False),
    ((718, get_form_id("-Form_50%")), get_game_id("XY_ORAS"), True),
    ((718, get_form_id("-Form_Complete")), get_game_id("SM_USUM"), True),
    ((791, get_form_id("-Form_Radiant_Sun")), get_game_id("SwSh"), False),
    ((792, get_form_id("-Form_Full_Moon")), get_game_id("SV"), False),
    ((791, get_form_id("-Form_Radiant_Sun")), get_game_id("SM_USUM"), True),
    ((792, get_form_id("-Form_Full_Moon")), get_game_id("SM_USUM"), True),
    ((802, get_form_id("-Form_Zenith")), get_game_id("SwSh"), False),
    ((802, get_form_id("-Form_Zenith")), get_game_id("SM_USUM"), True),
    ((808, default_form_id), get_game_id("SM_USUM"), False),
    ((809, default_form_id), get_game_id("SM_USUM"), False),
    ((808, default_form_id), get_game_id("LGPE"), True),
    ((809, default_form_id), get_game_id("LGPE"), True),
    ((808, default_form_id), get_game_id("SwSh"), True)
])
def test_is_form_obtainable(poke_form_id, game_id, expected):
    # Getting the dict values that holds poke_form_info and game_info, respectively, to check obtainability
    assert is_form_obtainable(poke_forms[poke_form_id], games[game_id]) == expected


@pytest.mark.parametrize("pfgo_id, sprite_type, expected", [
    # Univeresal exclusions
    ((1, default_form_id, get_game_id("LA")), "-Shiny", False),
    ((494, default_form_id, get_game_id("Platinum")), "Default", False),
    ((494, default_form_id, get_game_id("BW_B2W2")), "Default", True),
    ((1, default_form_id, get_game_id("Yellow")), "-Shiny", False),
    ((6, default_form_id, get_game_id("Red_Blue")), "-Shiny-Back", False),
    ((6, default_form_id, get_game_id("Gold")), "-Shiny", True),
    ((150, default_form_id, get_game_id("Red_Green")), "-Animated", False),
    ((150, default_form_id, get_game_id("Crystal")), "-Animated", True),
    ((151, default_form_id, get_game_id("Emerald")), "-Shiny-Back-Animated", False),
    ((493, get_form_id("-Form_Steel"), get_game_id("Diamond_Pearl")), "-Back-Animated", False),
    ((493, get_form_id("-Form_Steel"), get_game_id("BW_B2W2")), "-Back-Animated", True),
    ((152, default_form_id, get_game_id("Gold")), "-Animated", False),
    ((152, default_form_id, get_game_id("Silver")), "-Animated", False),
    ((152, default_form_id, get_game_id("FRLG")), "-Animated", False),
    ((152, default_form_id, get_game_id("Ruby_Sapphire")), "-Animated", False)
])
def test_is_sprite_possible(pfgo_id, sprite_type, expected):
    assert is_sprite_possible(pfgo[pfgo_id], sprite_type) == expected

@pytest.mark.parametrize("poke_num, form_name, sprite_type, expected", [
    (25, "-Form_Cosplay_PhD", "-Shiny", True),
    (25, "-Form_Cosplay_Belle", "-Shiny-Back-Animated", True),
    (25, "-Form_Cosplay_Libre", "-Back-Animated", False),
    (25, "-Form_Cap_World", "-Shiny", True),
    (25, "-Form_Cap_Hoenn", "-Shiny-Back", True),
    (25, "-Form_Cap_Unova", "-Back", False),
    (774, "-Form_Orange_Core", "-Shiny", True),
    (774, "-Form_Red_Core", "-Shiny-Back", True),
    (774, "-Form_Blue_Core", "-Shiny-Back-Animated", True),
    (774, "-Form_Yellow_Core", "-Shiny-Animated", True),
    (774, "-Form_Core", "-Shiny", False),
    (774, "-Form_Core", "-Shiny-Back", False),
    (774, "-Form_Core", "-Shiny-Back-Animated", False),
    (774, "-Form_Core", "-Shiny-Animated", False),
    (774, "-Form_Core", "Default", True),
    (774, "-Form_Core", "-Back", True),
    (774, "-Form_Core", "-Back-Animated", True),
    (774, "-Form_Core", "-Animated", True),
    (774, "-Form_Orange_Core", "Default", False),
    (774, "-Form_Red_Core", "-Back", False),
    (774, "-Form_Blue_Core", "-Back-Animated", False),
    (774, "-Form_Yellow_Core", "-Animated", False),
    (869, "-Form_Mint_Cream_Berry_Sweet", "-Shiny-Back", True),
    (869, "-Form_Star_Sweet", "-Shiny-Back", False),
    (869, "-Form_Ribbon_Sweet", "-Animated", True),
    (869, "-Form_Matcha_Cream_Strawberry_Sweet", "-Back-Animated", False),
    (1, "Default", "-Show_Stamp", True),
    (151, "-Form_Mega_X", "-Show_Stamp", True),
    (555, "-Form_Zen", "-Show_Stamp", True),
    (854, "-Form_Antique", "-Show_Stamp", False),
    (855, "-Form_Phony", "-Show_Stamp", False),
    (1012, "-Form_Artisan", "-Show_Stamp", False),
    (1013, "-Form_Masterpiece", "-Show_Stamp", False)
])
def test_should_skip_nonexistant_sprite(poke_num, form_name, sprite_type, expected):
    assert should_skip_nonexistant_sprite(poke_num, form_name, sprite_type) == expected



connection.close()