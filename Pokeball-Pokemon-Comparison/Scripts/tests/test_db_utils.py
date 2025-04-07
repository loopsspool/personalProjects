import sys
import os
import sqlite3
import pytest

# To go into parent directory to import db_utils
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from db_utils import DB_PATH, FORM_EXCLUSIONS, is_form_obtainable, get_poke_form_records, get_game_records, get_form_id, get_game_id

# Getting necessary info for testing
connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()
default_form_id = get_form_id("Default")
poke_forms = get_poke_form_records(cursor)
games = get_game_records(cursor)
connection.close()

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
    ((3, get_form_id("-f")), get_game_id("Diamond-Pearl"), True),
    ((493, get_form_id("-Form-Fairy")), get_game_id("BW-B2W2"), False),
    ((493, get_form_id("-Form-Fairy")), get_game_id("XY-ORAS"), True),
    ((6, get_form_id("-Mega_X")), get_game_id("BW-B2W2"), False),
    ((6, get_form_id("-Mega_X")), get_game_id("XY-ORAS"), True),
    ((6, get_form_id("-Mega_X")), get_game_id("LGPE"), False),
    ((6, get_form_id("-Mega_X")), get_game_id("SwSh"), False),
    ((3, get_form_id("-Mega")), get_game_id("BW-B2W2"), False),
    ((3, get_form_id("-Mega")), get_game_id("XY-ORAS"), True),
    ((3, get_form_id("-Mega")), get_game_id("LGPE"), False),
    ((3, get_form_id("-Mega")), get_game_id("SwSh"), False),
    ((3, get_form_id("-Gigantamax")), get_game_id("LA"), False)
    ((3, get_form_id("-Gigantamax")), get_game_id("SwSh"), True)
    ((19, get_form_id("-Region-Alola")), get_game_id("XY-ORAS"), False),
    ((19, get_form_id("-Region-Alola")), get_game_id("SM-USUM"), True),
    ((52, get_form_id("-Region-Galar")), get_game_id("LGPE"), False),
    ((52, get_form_id("-Region-Alola")), get_game_id("LGPE"), True),
    ((19, get_form_id("-Region-Alola")), get_game_id("BDSP"), False),
    ((19, default_form_id), get_game_id("BDSP"), True),
    ((52, get_form_id("-Region-Galar")), get_game_id("BW-B2W2"), False),
    ((52, get_form_id("-Region-Galar")), get_game_id("SwSh"), True)
    ((59, get_form_id("-Region-Hisui")), get_game_id("SwSh"), False),
    ((59, get_form_id("-Region-Hisui")), get_game_id("SV"), True),
    ((52, get_form_id("-Region-Galar")), get_game_id("LA"), False),
    ((19, get_form_id("-Region-Alola")), get_game_id("LA"), False),
    ((59, get_form_id("-Region-Hisui")), get_game_id("LA"), True),
    ((37, get_form_id("-Region-Alola")), get_game_id("LA"), True),
    ((38, get_form_id("-Region-Alola")), get_game_id("LA"), True),

    # Specific Pokemon
    ((25, get_form_id("-Form-Cosplay")), get_game_id("BW-B2W2"), False),
    ((25, get_form_id("-Form-Cosplay")), get_game_id("SM-USUM"), False),
    ((25, get_form_id("-Form-Cosplay")), get_game_id("XY-ORAS"), True),
    ((25, get_form_id("-Form-Cap-Alola")), get_game_id("XY-ORAS"), False),
    ((25, get_form_id("-Form-Cap-Alola")), get_game_id("LA"), False),
    ((25, get_form_id("-Form-Cap-Alola")), get_game_id("SM-USUM"), True),
    ((25, get_form_id("-Form-Cap-Alola")), get_game_id("SV"), True),
    ((25, get_form_id("-Form-Cap-World")), get_game_id("SM-USUM"), False),
    ((25, get_form_id("-Form-Cap-World")), get_game_id("SwSh"), True),
    ((25, get_form_id("-Form-Cap-World")), get_game_id("SV"), True),
    ((128, get_form_id("-Region-Paldea-Form-Blaze")), get_game_id("SwSh"), False),
    ((128, get_form_id("-Region-Paldea-Form-Blaze")), get_game_id("SV"), True),
    ((133, get_form_id("-f")), get_game_id("SM-USUM"), False),
    ((133, get_form_id("-f")), get_game_id("SwSh"), True),
    ((172, get_form_id("-Form-Spiky_Eared")), get_game_id("Emerald"), False),
    ((172, get_form_id("-Form-Spiky_Eared")), get_game_id("Diamond-Pearl"), True),
    ((201, get_form_id("-Form-!")), get_game_id("Gold"), False),
    ((201, get_form_id("-Form-Qmark")), get_game_id("Crystal"), False),
    ((201, get_form_id("-Form-!")), get_game_id("Ruby-Sapphire"), True),
    ((201, get_form_id("-Form-Qmark")), get_game_id("FRLG"), True),
    ((382, get_form_id("-Form-Primal")), get_game_id("BW-B2W2"), False),
    ((383, get_form_id("-Form-Primal")), get_game_id("SwSh"), False),
    ((382, get_form_id("-Form-Primal")), get_game_id("XY-ORAS"), True),
    ((383, get_form_id("-Form-Primal")), get_game_id("SM-USUM"), True)

])

def test_is_form_obtainable(poke_form_id, game_id, expected):
    # Getting the dict values that holds poke_form_info and game_info, respectively, to check obtainability
    assert is_form_obtainable(poke_forms[poke_form_id], games[game_id]) == expected
