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
    # Species game availability
    assert FORM_EXCLUSIONS["filtering_for_LGPE_dex_if_needed"](poke_forms[(152, 1)], games[16]) == True
    assert FORM_EXCLUSIONS["filtering_for_LGPE_dex_if_needed"](poke_forms[(1, 1)], games[16]) == False
    assert FORM_EXCLUSIONS["filtering_for_SwSh_dex_if_needed"](poke_forms[(13, 1)], games[17]) == True
    assert FORM_EXCLUSIONS["filtering_for_SwSh_dex_if_needed"](poke_forms[(1, 1)], games[17]) == False
    assert FORM_EXCLUSIONS["filtering_for_BDSP_dex_if_needed"](poke_forms[(494, 1)], games[18]) == True
    assert FORM_EXCLUSIONS["filtering_for_BDSP_dex_if_needed"](poke_forms[(1, 1)], games[18]) == False
    assert FORM_EXCLUSIONS["filtering_for_LA_dex_if_needed"](poke_forms[(1, 1)], games[19]) == True
    assert FORM_EXCLUSIONS["filtering_for_LA_dex_if_needed"](poke_forms[(25, 1)], games[19]) == False
    assert FORM_EXCLUSIONS["filtering_for_SV_dex_if_needed"](poke_forms[(10, 1)], games[20]) == True
    assert FORM_EXCLUSIONS["filtering_for_SV_dex_if_needed"](poke_forms[(1, 1)], games[20]) == False

    # Universal rules
    assert FORM_EXCLUSIONS["no_pokemon_with_a_higher_generation_than_game_generation"](poke_forms[(152, 1)], games[1]) == True
    assert FORM_EXCLUSIONS["no_pokemon_with_a_higher_generation_than_game_generation"](poke_forms[(1025, 1)], games[20]) == False
    assert FORM_EXCLUSIONS["no_f_form_visual_differences_before_gen_4"](poke_forms[(3, 4)], games[9]) == True
    assert FORM_EXCLUSIONS["no_f_form_visual_differences_before_gen_4"](poke_forms[(3, 4)], games[10]) == False
    assert FORM_EXCLUSIONS["no_fairy_forms_before_gen_6"](poke_forms[(493, 759)], games[13]) == True
    assert FORM_EXCLUSIONS["no_fairy_forms_before_gen_6"](poke_forms[(493, 759)], games[14]) == False
    assert FORM_EXCLUSIONS["no_megas_outside_gen_6_and_7_excluding_LGPE"](poke_forms[(6, 11)], games[13]) == True
    assert FORM_EXCLUSIONS["no_megas_outside_gen_6_and_7_excluding_LGPE"](poke_forms[(6, 11)], games[14]) == False
    assert FORM_EXCLUSIONS["no_megas_outside_gen_6_and_7_excluding_LGPE"](poke_forms[(6, 11)], games[17]) == True
    assert FORM_EXCLUSIONS["no_megas_outside_gen_6_and_7_excluding_LGPE"](poke_forms[(3, 5)], games[13]) == True
    assert FORM_EXCLUSIONS["no_megas_outside_gen_6_and_7_excluding_LGPE"](poke_forms[(3, 5)], games[14]) == False
    assert FORM_EXCLUSIONS["no_megas_outside_gen_6_and_7_excluding_LGPE"](poke_forms[(3, 5)], games[17]) == True

