import os

from app_globals import DB_PATH, init_save_dir_files
from db_utils import populate_db, update_file_existence, get_last_poke_num
from spreadsheet_utils import create_file_checklist_spreadsheet, cell_value, POKEMON_INFO_SHEET, POKE_INFO_LAST_ROW, POKE_INFO_NUM_COL
from bulba_scraping_utils import bulba_scrape_pokemon, bulba_scrape_pokeballs
from wikidex_scraping_utils import wikidex_scrape_pokemon


################################ React Native TODOs ############################################
# TODO: Also in RN will have to visually change Qmark with ??? (Arceus) or ? (Unown)
    # Probably best to check all forms after RN implemented


################################# TODO: Complete all TODOs here and from all files before running... please ########################
# TODO: Add Scraping stats? % Complete, num downloaded, etc.

# Later TODOs (after scraping)
# TODO: Add a check function for files spreadsheet to see if generation is complete. If not, output missing imgs
# TODO: Run checks on existing images to find small sizes and check bulba for larger files
    # Wikidex most common file size (250x250? 180x180? Def small, Bulba has most gen 8 (all switch?) at 1024x1024)
# TODO: Check if there's any female backs missing where male backs are present... May only have visual difference in front and sprite is recycled for back
# TODO: Download meltan & Melmetal animated backs by hand (filtered out bc no other LGPE backs)
# TODO: Delete all alts and remove them from db processing. Favor with still frames of animated images
# TODO: Fix downloaded animated pokeballs if animation out of order (static I touched Fast Ball, Friend Ball, "Great Ball", "Heavy Ball", "Level Ball", "Love Ball", "Lure Ball", "Master Ball", "Moon Ball", "Nest Ball", "Poke Ball", "Premier Ball", "Repeat Ball", "Safari Ball", "Sport Ball", "Timer Ball", "Ultra Ball")
# TODO: Look at certain missing pokeballs for gen3 (like fast ball)s
# TODO: Check if any filenames are the same but file ext is different
# TODO: Both still and animated to webp format
# TODO: Look at imgs that have waaay smaller stills than animated (mostly wikidex gen 8-9, see charizard gen 9 static/animated)
    # TODO: But dont be fooled by whitespace -- see shiny charmander gen 8 swsh


def main():
    # NOTE: Can make this false and set poke start/stop nums to print to console missing imgs -- my filenames and translated URLs
    ALLOW_DOWNLOAD = True
    poke_num_start_from = 184
    poke_num_stop_at = 450

    valid_start_poke_num, valid_stop_poke_num = validate_context(poke_num_start_from, poke_num_stop_at, force_update=False)   # This will check downloads with missing imgs in database and update
    
    # for poke_num in range(valid_start_poke_num, valid_stop_poke_num + 1):
    #     bulba_scrape_pokemon(poke_num, allow_download=ALLOW_DOWNLOAD)     # NOTE: Always check Bulba first, they have higher quality images
    #     wikidex_scrape_pokemon(poke_num, allow_download=ALLOW_DOWNLOAD)
    
    #bulba_scrape_pokeballs(allow_download=ALLOW_DOWNLOAD)
    #create_file_checklist_spreadsheet()




#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[     HELPERS     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

def validate_context(start_num, num_after_start, force_update=False):
    init_save_dir_files()   # Initializes sets of existing files, db uses to check file existence

    if not os.path.exists(DB_PATH) or force_update or db_isnt_current():
        populate_db(force_update)   # Will always rewrite filename tables, so also checks if any files were downloaded. Only skips existing form game obtainabailitty records bc its slow, new records will still be added (even on old pokes)
    else:
        update_file_existence()     # Checks to see if any images were downloaded

    return verify_start_stop_poke_nums(start_num, num_after_start)


def db_isnt_current():
    print("Confirming database is up to date...")

    if info_sheet_has_more_pokes_than_db():
        print("Pokemon Information sheet more current than database, preparing to update database...")
        return True
    else:
        print("Pokedex database is current, moving on...")
        return False


def info_sheet_has_more_pokes_than_db():
    # highest poke num in db checked against highest num in poke info sheet
    if get_last_poke_num() != int(cell_value(POKEMON_INFO_SHEET, POKE_INFO_LAST_ROW, POKE_INFO_NUM_COL)): 
        return True
    return False
    

def verify_start_stop_poke_nums(start, stop):
    last_db_poke_num = get_last_poke_num()

    if start < 1: start=1
    if stop < 1: stop=1
    if start > last_db_poke_num: start = last_db_poke_num
    if stop > last_db_poke_num: stop = last_db_poke_num
    if start > stop: stop = start

    return start, stop




if __name__ == "__main__":
    main()