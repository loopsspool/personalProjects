from app_globals import pokedex
from spreadsheet_funcs import *

# Force, if true, will rewrite the JSON and missing images spreadsheet even if the pokedex has the same last pokemon as the poke_info spreadsheet
def check_pokedex_is_current(force=False):
    print("Confirming pokedex is up to date...")

    # TODO: Add a pokemon_info spreadsheet save datetime check? Save datetime of last spreadsheet save in a file and if when this function is run again it doesnt match, update pokedex
    if info_sheet_has_more_pokes_than_dex() or force:
        # TODO: For some reason both print statements activate
        if info_sheet_has_more_pokes_than_dex(): 
            print("Pokemon Information sheet more current than pokedex, preparing to update pokedex and relevant files...")
        if force:
            print("Forcing through...")
        generate_pokedex_from_spreadsheet()
        # Write new file checker file if one doesn't exist
        # If it does just add new rows for new pokes missing images
        # Append to missing images array for each
        # Find bulba archive link for each
        # Save to JSON
    else:
        print("Pokedex is current, moving on...")

def info_sheet_has_more_pokes_than_dex():
    # If the amount of pokemon in the pokedex is not equal 
    if len(pokedex) != cell_value(pokemon_info_sheet, poke_info_last_row, poke_info_num_col):
        return True