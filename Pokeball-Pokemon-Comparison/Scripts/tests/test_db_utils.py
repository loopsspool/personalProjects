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

@pytest.mark.parametrize("form_id, game_id, expected", [
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
    ((3, get_form_id("-Mega")), get_game_id("SwSh"), False)
])

def test_is_form_obtainable(form_id, game_id, expected):
    # Getting the dict values that holds poke_form_info and game_info, respectively, to check obtainability
    assert is_form_obtainable(poke_forms[form_id], games[game_id]) == expected
