import sys
import os
import sqlite3

# To go into parent directory to import db_utils
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from db_utils import DB_PATH, FORM_EXCLUSIONS, is_form_obtainable, get_poke_form_records, get_game_records

def test_is_form_obtainable():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    poke_forms = get_poke_form_records(cursor)
    games = get_game_records(cursor)
    connection.close()
    # TODO: Insert specific pokemon here that fulfill each check in FORM_EXCLUSIONS
    assert FORM_EXCLUSIONS["filtering_for_LGPE_dex_if_needed"](poke_forms[(152, 1)], games[16]) == True
    assert FORM_EXCLUSIONS["filtering_for_LGPE_dex_if_needed"](poke_forms[(1, 1)], games[16]) == False

    

