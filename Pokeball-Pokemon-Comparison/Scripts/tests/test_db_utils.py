import sys
import os
import sqlite3
import pytest

# TODO: To replace cursor arguments, in db_utils could pull game/form ids into a dict or something, then search that instead of the db

# To go into parent directory to import db_utils
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from db_utils import DB_PATH, FORM_EXCLUSIONS, SHARED_SHINY_FORMS, is_form_obtainable, is_sprite_possible, should_skip_nonexistant_sprite, get_poke_form_records, get_poke_form_obtainability_records, get_game_records, get_form_id, get_game_id, get_sprite_types

# Setting up connection to db
connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()
# Getting necessary info for testing
default_form_id = get_form_id(cursor, "Default")
poke_forms = get_poke_form_records(cursor)
games = get_game_records(cursor)
pfgo = get_poke_form_obtainability_records(cursor)
sprite_types = get_sprite_types(cursor)

@pytest.mark.parametrize("poke_form_id, game_id, expected", [
    # Species game availability
    ((152, default_form_id), get_game_id(cursor, "LGPE"), False),
    ((1, default_form_id), get_game_id(cursor, "LGPE"), True),
    ((13, default_form_id), get_game_id(cursor, "SwSh"), False),
    ((1, default_form_id), get_game_id(cursor, "SwSh"), True),
    ((494, default_form_id), get_game_id(cursor, "BDSP"), False),
    ((1, default_form_id), get_game_id(cursor, "BDSP"), True),
    ((1, default_form_id), get_game_id(cursor, "LA"), False),
    ((25, default_form_id), get_game_id(cursor, "LA"), True),
    ((10, default_form_id), get_game_id(cursor, "SV"), False),
    ((1, default_form_id), get_game_id(cursor, "SV"), True),

    # Universal rules
    ((152, default_form_id), 1, False),
    ((1025, default_form_id), 20, True),
    ((3, get_form_id(cursor, "-f")), get_game_id(cursor, "FRLG"), False),
    ((3, get_form_id(cursor, "-f")), get_game_id(cursor, "Diamond-Pearl"), True),
    ((493, get_form_id(cursor, "-Form-Fairy")), get_game_id(cursor, "BW-B2W2"), False),
    ((493, get_form_id(cursor, "-Form-Fairy")), get_game_id(cursor, "XY-ORAS"), True),
    ((6, get_form_id(cursor, "-Mega_X")), get_game_id(cursor, "BW-B2W2"), False),
    ((6, get_form_id(cursor, "-Mega_X")), get_game_id(cursor, "XY-ORAS"), True),
    ((6, get_form_id(cursor, "-Mega_X")), get_game_id(cursor, "LGPE"), False),
    ((6, get_form_id(cursor, "-Mega_X")), get_game_id(cursor, "SwSh"), False),
    ((3, get_form_id(cursor, "-Mega")), get_game_id(cursor, "BW-B2W2"), False),
    ((3, get_form_id(cursor, "-Mega")), get_game_id(cursor, "XY-ORAS"), True),
    ((3, get_form_id(cursor, "-Mega")), get_game_id(cursor, "LGPE"), False),
    ((3, get_form_id(cursor, "-Mega")), get_game_id(cursor, "SwSh"), False),
    ((3, get_form_id(cursor, "-Gigantamax")), get_game_id(cursor, "LA"), False),
    ((3, get_form_id(cursor, "-Gigantamax")), get_game_id(cursor, "SwSh"), True),
    ((19, get_form_id(cursor, "-Region-Alola")), get_game_id(cursor, "XY-ORAS"), False),
    ((19, get_form_id(cursor, "-Region-Alola")), get_game_id(cursor, "SM-USUM"), True),
    ((52, get_form_id(cursor, "-Region-Galar")), get_game_id(cursor, "LGPE"), False),
    ((52, get_form_id(cursor, "-Region-Alola")), get_game_id(cursor, "LGPE"), True),
    ((19, get_form_id(cursor, "-Region-Alola")), get_game_id(cursor, "BDSP"), False),
    ((19, default_form_id), get_game_id(cursor, "BDSP"), True),
    ((52, get_form_id(cursor, "-Region-Galar")), get_game_id(cursor, "BW-B2W2"), False),
    ((52, get_form_id(cursor, "-Region-Galar")), get_game_id(cursor, "SwSh"), True),
    ((59, get_form_id(cursor, "-Region-Hisui")), get_game_id(cursor, "SwSh"), False),
    ((59, get_form_id(cursor, "-Region-Hisui")), get_game_id(cursor, "SV"), True),
    ((52, get_form_id(cursor, "-Region-Galar")), get_game_id(cursor, "LA"), False),
    ((19, get_form_id(cursor, "-Region-Alola")), get_game_id(cursor, "LA"), False),
    ((59, get_form_id(cursor, "-Region-Hisui")), get_game_id(cursor, "LA"), True),
    ((37, get_form_id(cursor, "-Region-Alola")), get_game_id(cursor, "LA"), True),
    ((38, get_form_id(cursor, "-Region-Alola")), get_game_id(cursor, "LA"), True),

    # Specific Pokemon
    ((25, get_form_id(cursor, "-Form-Cosplay-Belle")), get_game_id(cursor, "BW-B2W2"), False),
    ((25, get_form_id(cursor, "-Form-Cosplay-Libre")), get_game_id(cursor, "SM-USUM"), False),
    ((25, get_form_id(cursor, "-Form-Cosplay-PhD")), get_game_id(cursor, "XY-ORAS"), True),
    ((25, get_form_id(cursor, "-Form-Cap-Hoenn")), get_game_id(cursor, "XY-ORAS"), False),
    ((25, get_form_id(cursor, "-Form-Cap-Alola")), get_game_id(cursor, "LA"), False),
    ((25, get_form_id(cursor, "-Form-Cap-Alola")), get_game_id(cursor, "SM-USUM"), True),
    ((25, get_form_id(cursor, "-Form-Cap-Unova")), get_game_id(cursor, "SV"), True),
    ((25, get_form_id(cursor, "-Form-Cap-World")), get_game_id(cursor, "SM-USUM"), False),
    ((25, get_form_id(cursor, "-Form-Cap-World")), get_game_id(cursor, "SwSh"), True),
    ((25, get_form_id(cursor, "-Form-Cap-World")), get_game_id(cursor, "SV"), True),
    ((128, get_form_id(cursor, "-Region-Paldea-Form-Blaze")), get_game_id(cursor, "SwSh"), False),
    ((128, get_form_id(cursor, "-Region-Paldea-Form-Blaze")), get_game_id(cursor, "SV"), True),
    ((133, get_form_id(cursor, "-f")), get_game_id(cursor, "SM-USUM"), False),
    ((133, get_form_id(cursor, "-f")), get_game_id(cursor, "SwSh"), True),
    ((172, get_form_id(cursor, "-Form-Spiky_Eared")), get_game_id(cursor, "Emerald"), False),
    ((172, get_form_id(cursor, "-Form-Spiky_Eared")), get_game_id(cursor, "Diamond-Pearl"), True),
    ((201, get_form_id(cursor, "-Form-!")), get_game_id(cursor, "Gold"), False),
    ((201, get_form_id(cursor, "-Form-Qmark")), get_game_id(cursor, "Crystal"), False),
    ((201, get_form_id(cursor, "-Form-!")), get_game_id(cursor, "Ruby-Sapphire"), True),
    ((201, get_form_id(cursor, "-Form-Qmark")), get_game_id(cursor, "FRLG"), True),
    ((382, get_form_id(cursor, "-Form-Primal")), get_game_id(cursor, "BW-B2W2"), False),
    ((383, get_form_id(cursor, "-Form-Primal")), get_game_id(cursor, "SwSh"), False),
    ((382, get_form_id(cursor, "-Form-Primal")), get_game_id(cursor, "XY-ORAS"), True),
    ((383, get_form_id(cursor, "-Form-Primal")), get_game_id(cursor, "SM-USUM"), True),
    ((479, get_form_id(cursor, "-Form-Heat")), get_game_id(cursor, "Diamond-Pearl"), False),
    ((479, get_form_id(cursor, "-Form-Heat")), get_game_id(cursor, "HGSS"), True),
    ((479, get_form_id(cursor, "-Form-Wash")), get_game_id(cursor, "Platinum"), True),
    ((483, get_form_id(cursor, "-Form-Origin")), get_game_id(cursor, "BDSP"), False),
    ((484, get_form_id(cursor, "-Form-Origin")), get_game_id(cursor, "SwSh"), False),
    ((483, get_form_id(cursor, "-Form-Origin")), get_game_id(cursor, "LA"), True),
    ((484, get_form_id(cursor, "-Form-Origin")), get_game_id(cursor, "SV"), True),
    ((487, get_form_id(cursor, "-Form-Origin")), get_game_id(cursor, "Diamond-Pearl"), False),
    ((487, get_form_id(cursor, "-Form-Origin")), get_game_id(cursor, "Platinum"), True),
    ((487, get_form_id(cursor, "-Form-Origin")), get_game_id(cursor, "BW-B2W2"), True),
    ((492, get_form_id(cursor, "-Form-Sky")), get_game_id(cursor, "Diamond-Pearl"), False),
    ((492, get_form_id(cursor, "-Form-Sky")), get_game_id(cursor, "Platinum"), True),
    ((492, get_form_id(cursor, "-Form-Sky")), get_game_id(cursor, "BW-B2W2"), True),
    ((493, get_form_id(cursor, "-Form-Qmark")), get_game_id(cursor, "BW-B2W2"), False),
    ((493, get_form_id(cursor, "-Form-Qmark")), get_game_id(cursor, "Diamond-Pearl"), True),
    ((658, get_form_id(cursor, "-Form-Ash")), get_game_id(cursor, "XY-ORAS"), False),
    ((658, get_form_id(cursor, "-Form-Ash")), get_game_id(cursor, "SV"), False),
    ((658, get_form_id(cursor, "-Form-Ash")), get_game_id(cursor, "SM-USUM"), True),
    ((718, get_form_id(cursor, "-Form-10%")), get_game_id(cursor, "XY-ORAS"), False),
    ((718, get_form_id(cursor, "-Form-50%")), get_game_id(cursor, "XY-ORAS"), True),
    ((718, get_form_id(cursor, "-Form-Complete")), get_game_id(cursor, "SM-USUM"), True),
    ((791, get_form_id(cursor, "-Form-Radiant_Sun")), get_game_id(cursor, "SwSh"), False),
    ((792, get_form_id(cursor, "-Form-Full_Moon")), get_game_id(cursor, "SV"), False),
    ((791, get_form_id(cursor, "-Form-Radiant_Sun")), get_game_id(cursor, "SM-USUM"), True),
    ((792, get_form_id(cursor, "-Form-Full_Moon")), get_game_id(cursor, "SM-USUM"), True),
    ((802, get_form_id(cursor, "-Form-Zenith")), get_game_id(cursor, "SwSh"), False),
    ((802, get_form_id(cursor, "-Form-Zenith")), get_game_id(cursor, "SM-USUM"), True),
    ((808, default_form_id), get_game_id(cursor, "SM-USUM"), False),
    ((809, default_form_id), get_game_id(cursor, "SM-USUM"), False),
    ((808, default_form_id), get_game_id(cursor, "LGPE"), True),
    ((809, default_form_id), get_game_id(cursor, "LGPE"), True),
    ((808, default_form_id), get_game_id(cursor, "SwSh"), True)
])
def test_is_form_obtainable(poke_form_id, game_id, expected):
    # Getting the dict values that holds poke_form_info and game_info, respectively, to check obtainability
    assert is_form_obtainable(poke_forms[poke_form_id], games[game_id]) == expected


@pytest.mark.parametrize("pfgo_id, sprite_type, expected", [
    # Univeresal exclusions
    ((1, default_form_id, get_game_id(cursor, "LA")), "-Shiny", False),
    ((494, default_form_id, get_game_id(cursor, "Platinum")), "Default", False),
    ((494, default_form_id, get_game_id(cursor, "BW-B2W2")), "Default", True),
    ((1, default_form_id, get_game_id(cursor, "Yellow")), "-Shiny", False),
    ((6, default_form_id, get_game_id(cursor, "Red-Blue")), "-Shiny-Back", False),
    ((6, default_form_id, get_game_id(cursor, "Gold")), "-Shiny", True),
    ((150, default_form_id, get_game_id(cursor, "Red-Green")), "-Animated", False),
    ((150, default_form_id, get_game_id(cursor, "Crystal")), "-Animated", True),
    ((151, default_form_id, get_game_id(cursor, "Emerald")), "-Shiny-Back-Animated", False),
    ((493, get_form_id(cursor, "-Form-Steel"), get_game_id(cursor, "Diamond-Pearl")), "-Back-Animated", False),
    ((493, get_form_id(cursor, "-Form-Steel"), get_game_id(cursor, "BW-B2W2")), "-Back-Animated", True),
    ((152, default_form_id, get_game_id(cursor, "Gold")), "-Animated", False),
    ((152, default_form_id, get_game_id(cursor, "Silver")), "-Animated", False),
    ((152, default_form_id, get_game_id(cursor, "FRLG")), "-Animated", False),
    ((152, default_form_id, get_game_id(cursor, "Ruby-Sapphire")), "-Animated", False)
])
def test_is_sprite_possible(pfgo_id, sprite_type, expected):
    assert is_sprite_possible(pfgo[pfgo_id], sprite_type) == expected

@pytest.mark.parametrize("poke_num, form_name, sprite_type, expected", [
    (25, "-Form-Cosplay-PhD", "-Shiny", True),
    (25, "-Form-Cosplay-Belle", "-Shiny-Back-Animated", True),
    (25, "-Form-Cosplay-Libre", "-Back-Animated", False),
    (25, "-Form-Cap-World", "-Shiny", True),
    (25, "-Form-Cap-Hoenn", "-Shiny-Back", True),
    (25, "-Form-Cap-Unova", "-Back", False),
    (774, "-Form-Orange_Core", "-Shiny", True),
    (774, "-Form-Red_Core", "-Shiny-Back", True),
    (774, "-Form-Blue_Core", "-Shiny-Back-Animated", True),
    (774, "-Form-Yellow_Core", "-Shiny-Animated", True),
    (774, "-Form-Core", "-Shiny", False),
    (774, "-Form-Core", "-Shiny-Back", False),
    (774, "-Form-Core", "-Shiny-Back-Animated", False),
    (774, "-Form-Core", "-Shiny-Animated", False),
    (774, "-Form-Core", "Default", True),
    (774, "-Form-Core", "-Back", True),
    (774, "-Form-Core", "-Back-Animated", True),
    (774, "-Form-Core", "-Animated", True),
    (774, "-Form-Orange_Core", "Default", False),
    (774, "-Form-Red_Core", "-Back", False),
    (774, "-Form-Blue_Core", "-Back-Animated", False),
    (774, "-Form-Yellow_Core", "-Animated", False),
    (869, "-Form-Mint_Cream-Berry_Sweet", "-Shiny-Back", True),
    (869, "-Form-Star_Sweet", "-Shiny-Back", False),
    (869, "-Form-Ribbon_Sweet", "-Animated", True),
    (869, "-Form-Matcha_Cream-Strawberry_Sweet", "-Back-Animated", False),
    (1, "Default", "-Show_Stamp", True),
    (151, "-Form-Mega_X", "-Show_Stamp", True),
    (555, "-Form-Zen", "-Show_Stamp", True),
    (854, "-Form-Antique", "-Show_Stamp", False),
    (855, "-Form-Phony", "-Show_Stamp", False),
    (1012, "-Form-Artisan", "-Show_Stamp", False),
    (1013, "-Form-Masterpiece", "-Show_Stamp", False)
])
def test_should_skip_nonexistant_sprite(poke_num, form_name, sprite_type, expected):
    assert should_skip_nonexistant_sprite(poke_num, form_name, sprite_type) == expected



connection.close()